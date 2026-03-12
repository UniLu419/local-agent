"""Interactive CLI agent.

Usage:
    poetry run agent

Each conversation turn is sent to the compiled LangGraph agent.  A fixed
``thread_id`` is used so the full chat history is preserved across turns
within a single process run (backed by the in-memory MemorySaver).

To start a fresh session without restarting the process, type ``/new`` at
the prompt.
"""

import uuid

from langchain_core.messages import AIMessage

from app.agent.graph import agent_graph


def _extract_output(result: dict) -> str:
    """Return the agent's final text answer from the graph result dict.

    ``result["output"]`` is set by agent_node on every turn.  As a fallback
    we scan the message list in reverse for the last non-empty AIMessage.
    """
    output = result.get("output", "").strip()
    if output:
        return output

    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
            return msg.content.strip()

    return "(no response)"


def main() -> None:
    print("Agent started. Type /new to reset the session, Ctrl+C to exit.\n")

    session_id = "default"

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "/new":
            session_id = str(uuid.uuid4())
            print(f"[New session started: {session_id[:8]}...]\n")
            continue

        config = {"configurable": {"thread_id": session_id}}

        result = agent_graph.invoke(
            {"input": user_input, "session_id": session_id},
            config=config,
        )

        print(f"Agent: {_extract_output(result)}\n")
