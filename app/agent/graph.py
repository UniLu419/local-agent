from typing import TypedDict, List, NotRequired
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from app.agent.model import get_llm
from app.rag.retriever import search


llm = get_llm()


class AgentState(TypedDict):

    session_id: str
    input: str

    messages: List[BaseMessage]

    context: NotRequired[str]

    output: NotRequired[str]


def retrieve_node(state: AgentState):

    query = state["input"]

    context = search(query)

    return {"context": context}


def agent_node(state: AgentState):

    history = state["messages"]

    context = state.get("context", "")

    query = state["input"]

    prompt = f"""
You are a helpful assistant.

Use the following context if relevant.

Context:
{context}
"""

    messages = [SystemMessage(content=prompt)] + history + [HumanMessage(content=query)]

    resp = llm.invoke(messages)

    return {
        "output": resp.content,
        "messages": history + [HumanMessage(content=query), resp],
    }


from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState)

graph.add_node("retrieve", retrieve_node)
graph.add_node("agent", agent_node)

graph.set_entry_point("retrieve")

graph.add_edge("retrieve", "agent")
graph.add_edge("agent", END)

agent_graph = graph.compile()
