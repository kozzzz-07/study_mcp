import asyncio
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient


load_dotenv()

# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)


ROOT_FOLDER = Path(__file__).parent.parent.absolute()
MCP_PATH = str(ROOT_FOLDER / "mcp_server" / "binance_mcp" / "binance_mcp.py")


# claudeとかに読み込ませるやつと同じもの
mcp_config = {
    "binance": {
        "command": "python",
        "args": [MCP_PATH],
        "transport": "stdio",
    }
}


async def get_crypto_prices():
    client = MultiServerMCPClient(mcp_config)
    tools = await client.get_tools()
    agent = create_react_agent(model, tools)
    query = "What are the current prices of Bitcoin and Ethereum?"
    message = HumanMessage(content=query)
    response = await agent.ainvoke({"messages": [message]})
    answer = response["messages"][-1].content
    return answer


if __name__ == "__main__":
    response = asyncio.run(get_crypto_prices())
    print(response)
