from typing import Annotated, NotRequired, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Shared state threaded through every node in the agent graph.

    Fields
    ------
    session_id:
        Caller-supplied identifier; mirrors the LangGraph ``thread_id`` so
        nodes can reference it without touching the config object.
    input:
        The raw user text for the current turn.
    messages:
        Full conversation history.  The ``add_messages`` reducer means each
        node only needs to *return* the new messages it produces — LangGraph
        will append them to the existing list automatically.
    context:
        Retrieved RAG context for the current turn (set by retrieve_node).
    output:
        Final text answer for the current turn (set by the last agent_node
        invocation, after all tool calls have been resolved).
    """

    session_id: str
    input: str
    messages: Annotated[list[BaseMessage], add_messages]
    context: NotRequired[str]
    output: NotRequired[str]
