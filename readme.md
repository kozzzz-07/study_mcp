## setup
- command
  - python -m venv .venv
  - . ./.venv/bin/activate
  - pip install -r requirements.txt 
- apikey
  - https://aistudio.google.com/apikey
  - set your GEMINI_API_KEY and GOOGLE_API_KEY


## docs
- https://github.com/modelcontextprotocol/python-sdk
- https://github.com/langchain-ai/langchain-mcp-adapters
- https://developers.cloudflare.com/agents/guides/remote-mcp-server/


## debug
- stdio
  - macの場合
    - pythonのファイルパスの取得
        - 例：VSCODEの `/binance_mcp/binance_mcp.py` で右クリック、Copy Path
    - Pythonの実行ファイルパスの取得
        - (.venv) の状態で `which python`
    - `npx @modelcontextprotocol/inspector [Pythonの実行ファイルパス] [pythonのファイルパス]`
  - mcp コマンド
    - `mcp dev [pythonのファイルパス]`
- sse / streamable-http
  - `cd mcp_server/binance_mpc_remote`
  - `python binance_mcp.py`
  - 別のターミナルで、`npx @modelcontextprotocol/inspector`
  - streamable-http/url: `http://127.0.0.1:8897/mcp`
  - sse/url: `http://127.0.0.1:8897/sse`

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

- ts_mcp_server
- `which bun`
- claudeと cursor
```json
"binance-ts-mcp": {
  "command": "/your-path/.bun/bin/bun",
  "args": ["/your-path/learn-mcp/ts_mcp_server/src/binance_mcp.ts"]
}
```

- cursorだと以下でも上手くいった
```json
"binance-ts-mcp": {
  "command": "bun",
  "args": [
    "run",
    "/your-path/learn-mcp/ts_mcp_server/src/binance_mcp.ts"
  ]
}
````
