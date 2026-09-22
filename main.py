from langchain_core.messages import HumanMessage

from agent import research_agent


print("=" * 60)
print("AI RESEARCH AGENT")
print("Groq + LangChain + LangGraph + LangSmith")
print("=" * 60)


while True:

    question = input(
        "\nWhat would you like me to research?\n> "
    )

    if question.lower() in [
        "exit",
        "quit",
        "q"
    ]:
        print("Goodbye!")
        break

    try:

        result = research_agent.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=question
                    )
                ]
            },
            config={
                "recursion_limit": 15
            }
        )

        final_message = result["messages"][-1]

        print("\n")
        print("=" * 60)
        print("RESEARCH RESULT")
        print("=" * 60)
        print(final_message.content)

    except Exception as e:

        print(
            f"\nError: {str(e)}"
        )