from typing import Any
from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("Binance MCP")


def get_symbol_from_name(name: str) -> str:
    if name.lower() in ["bitcoin", "btc"]:
        return "BTCUSDT"
    elif name.lower() in ["ethereum", "eth"]:
        return "ETHUSDT"
    else:
        return name.upper()

# mcp toolとしてのアノテーション
# toolとして登録した場合、Docstringを記述して、関数の目的や引数、戻り値を記載する。LLMが関数を適切に利用するため。
@mcp.tool()
def get_price(symbol: str) -> Any:
    """
    Get the current price of a crypto asset from Binance

    Args:
        symbol (str): The symbol of the crypto asset to get the price of

    Returns
        Any: The current price od the crypto asset
    """
    symbol = get_symbol_from_name(symbol)
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("Starting Binance MCP")
    mcp.run()
