import datetime
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP
import requests

THIS_FOLDER = Path(__file__).parent.absolute()
ACTIVITY_LOG_FILE = THIS_FOLDER / "activity.log"

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

    if response.status_code != 200:
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(
                f"Error getting price change for {symbol}: {response.status_code} {response.text}\n"
            )
        raise Exception(
            f"Error getting price change for {symbol}: {response.status_code} {response.text}"
        )
    else:
        price = response.json()["price"]
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(
                f"Successfully got price change for {symbol}. Current price is {price}. Current time is {datetime.datetime.now(datetime.UTC)}\n"
            )

    return f"The current price of {symbol} is {price}"

# Resources
# mcp.resourceアノテーションでリソースとして公開し、LLMがこのログにアクセスできるようになる
# リソースの内容を、バイトストリームにして返す
# HTTPプロトコルは現在MCPクライアントでは適切にサポートされていないため、fileやresourceを使用することを推奨
@mcp.resource("file://activity.log")
def activity_log() -> str:
    with open(ACTIVITY_LOG_FILE, "r") as f:
        return f.read()

# Resource Templates
# パラメーター化されたリソースを公開
# symbolをパラメーターとして受け取り、価格をリソースとして返す
# Resource TemplatesはMCPクライアント（claudeなど）が対応していない場合あり
@mcp.resource("resource://crypto_price/{symbol}")
def get_crypto_price(symbol: str) -> str:
    return get_price(symbol)


@mcp.tool()
def get_price_price_change(symbol: str) -> Any:
    """
    Get the price change of the last 24 hours of a crypto asset from Binance

    Args:
        symbol (str): The symbol of the crypto asset to get the price change of

    Returns:
        Any: The price change of the crypto asset in the last 24 hours
    """
    symbol = get_symbol_from_name(symbol)
    url = f"https://data-api.binance.vision/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("Starting Binance MCP")
    if not Path(ACTIVITY_LOG_FILE).exists():
        Path(ACTIVITY_LOG_FILE).touch()
    mcp.run()
