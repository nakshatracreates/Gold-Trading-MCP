
import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()

async def main():

    client = MultiServerMCPClient(
        {
            "gold_trading": {
                "transport": "stdio",
                "command": "python",
                "args": ["server.py"],
            }
        }
    )

   
    tools = await client.get_tools()

    print("Connected MCP tools:")
    for tool in tools:
        print("-", tool.name)

    
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    
    agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=(
        "You are a Gold Trading Research Assistant. "
        "Use available MCP tools for risk calculations, "
        "trading journal operations, market data and backtest analysis. "
        "Never invent market prices or trading results. "
        "Do not execute live trades."
    ),
)

    # Test the agent
    # Continuous AI conversation
    conversation = []

    print("\nGold Trading AI Assistant")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("AI session ended.")
            break

        if not user_input:
            continue

        conversation.append({
            "role": "user",
            "content": user_input
        })

        response = await agent.ainvoke({
            "messages": conversation
        })

        conversation = response["messages"]

        print("\nAI:", conversation[-1].content)
        print()


if __name__ == "__main__":
    asyncio.run(main())


