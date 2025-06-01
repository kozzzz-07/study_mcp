## setup
- command
  - python -m venv .venv
  - . ./.venv/bin/activate
  - pip install -r requirements.txt 
- apikey
  - https://aistudio.google.com/apikey
  - set GEMINI_API_KEY


## docs
- https://github.com/modelcontextprotocol/python-sdk


## debug
- macの場合
  - pythonのファイルパスの取得
      - 例：VSCODEの `/binance_mcp/binance_mcp.py` で右クリック、Copy Path
  - Pythonの実行ファイルパスの取得
      - (.venv) の状態で `which python`
  - `npx @modelcontextprotocol/inspector [Pythonの実行ファイルパス] [pythonのファイルパス]`
- mcp コマンド
  - `mcp dev [pythonのファイルパス]`

## command
- mcp サーバー実行
  - mcp run --transport [stdio|sse|streamable-http]

## mcp settings
```json
{
  "mcpServers":{
    "binance-mcp": {
      "command": "[Pythonの実行ファイルパス]",
      "args": [
        "[pythonのファイルパス]"
      ]
    }
  }
}
```