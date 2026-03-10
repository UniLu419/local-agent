from app.agent.graph import agent_graph


def main():

    print("Agent started. Ctrl+C to exit.\n")

    while True:

        user_input = input("You: ")

        result = agent_graph.invoke(
            {
                "input": user_input,
                "messages": [],
                "session_id": "default",
            }
        )

        print("Agent:", result["output"])
