"""LangGraph agent graph — ReAct loop with RAG retrieval and tool calling.

Graph topology
--------------

  [retrieve] ──► [agent] ──► (tools_condition)
                    ▲               │
                    │    "tools"    ▼
                    └────────── [tools]
                         "__end__" ──► END

1. ``retrieve``  – Fetches relevant context from the vector DB and adds the
                   user's HumanMessage to the shared message list.
2. ``agent``     – Prepends a SystemMessage with the RAG context, then invokes
                   the LLM (which has tools bound).  If the model emits tool
                   calls the graph routes to ``tools``; otherwise it ends.
3. ``tools``     – Executes every tool call in the last AIMessage via
                   ``ToolNode`` and returns ToolMessages.
4. Loop          – After ``tools`` the graph returns to ``agent`` so the model
                   can incorporate the tool results and either call more tools
                   or produce the final answer.

Multi-user / multi-session
--------------------------
The graph is compiled with a ``MemorySaver`` checkpointer.  Pass a per-user
config when invoking::

    agent_graph.invoke(
        {"input": text, "session_id": session_id},
        config={"configurable": {"thread_id": session_id}},
    )

Each unique ``thread_id`` gets its own isolated conversation history.
"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.model import get_llm
from app.agent.state import AgentState
from app.rag.retriever import search
from app.tools.registry import get_tools

# ---------------------------------------------------------------------------
# Initialise LLM and bind all registered tools
# ---------------------------------------------------------------------------

_llm = get_llm()
_tools = get_tools()
_llm_with_tools = _llm.bind_tools(_tools)


# ---------------------------------------------------------------------------
# Node definitions
# ---------------------------------------------------------------------------


def retrieve_node(state: AgentState) -> dict:
    """Query the vector DB for context and enqueue the user's HumanMessage.

    Returning a HumanMessage here lets the ``add_messages`` reducer append it
    to the running conversation history automatically.
    """
    query = state["input"]
    context = search(query)
    return {
        "context": context,
        # add_messages will append this to the existing history
        "messages": [HumanMessage(content=query)],
    }


def agent_node(state: AgentState) -> dict:
    """Invoke the LLM (with tools bound) over the full conversation history.

    The system message is rebuilt on every call so the RAG context is always
    fresh.  The LLM response is appended to ``messages``; if it contains tool
    calls the graph will route to ``tools``, otherwise it terminates.
    """
    context = state.get("context") or ""

    system_content = (
        "You are a helpful assistant with access to tools.\n"
        "Use the available tools whenever they can help answer the question.\n"
        "Think step-by-step and use multiple tools if needed."
    )
    if context.strip():
        system_content += (
            "\n\nUse the following retrieved context if it is relevant to the question:\n"
            f"{context}"
        )

    # Prepend a fresh SystemMessage to the accumulated history
    messages = [SystemMessage(content=system_content)] + list(state["messages"])

    response: AIMessage = _llm_with_tools.invoke(messages)

    # Extract text output; may be empty when the model only emits tool calls
    output = response.content if isinstance(response.content, str) else ""

    return {
        "messages": [response],  # add_messages appends this
        "output": output,
    }


# ---------------------------------------------------------------------------
# Graph assembly
# ---------------------------------------------------------------------------

_graph = StateGraph(AgentState)

_graph.add_node("retrieve", retrieve_node)
_graph.add_node("agent", agent_node)
_graph.add_node("tools", ToolNode(_tools))

_graph.set_entry_point("retrieve")

# retrieve → agent (always)
_graph.add_edge("retrieve", "agent")

# agent → tools  (if the model produced tool calls)
# agent → END    (if the model produced a final text answer)
_graph.add_conditional_edges("agent", tools_condition)

# tools → agent  (loop: let the model process the tool results)
_graph.add_edge("tools", "agent")

# Compile with an in-process memory checkpointer for multi-session support.
# Swap MemorySaver for SqliteSaver / RedisSaver for persistence across restarts.
_checkpointer = MemorySaver()
agent_graph = _graph.compile(checkpointer=_checkpointer)
