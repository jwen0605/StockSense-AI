import os
from dotenv import load_dotenv
from llm import generate_insight

load_dotenv()


def main():
    if not os.getenv("SERPER_API_KEY"):
        print("Error: Please set SERPER_API_KEY in your .env file")
        exit(1)
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: Please set ANTHROPIC_API_KEY in your .env file")
        exit(1)

    user_query = "What is NVIDIA's stock price today?"
    print(f"User: {user_query}\n")

    response = generate_insight(user_query)
    print(f"\n[Claude] Final Answer:\n{response}")


if __name__ == "__main__":
    main()
