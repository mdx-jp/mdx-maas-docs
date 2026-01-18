# Chat Completions API ドキュメント

# 概要

Chat Completions APIは、OpenAI互換のチャット完了エンドポイントを提供します。複数のLLMモデルに対して統一されたインターフェースでアクセスできます。

**エンドポイント**: `POST /v1/chat/completions`

**ベースURL**: [https://api.maas.mdx1.jp](https://api.maas.mdx1.jp)

## 認証

すべてのリクエストには、APIキーによる認証が必要です。APIキーはHTTPヘッダーの`Authorization`フィールドにBearer Token形式で指定します。

```
Authorization: Bearer <your-api-key>
```

### APIキーの取得方法

APIキーは管理者から提供されます。APIキーが無効または期限切れの場合、`401 Unauthorized`エラーが返されます。

## リクエストパラメータ

### 必須パラメータ

- **model** (string): 使用するLLMモデルの名前
    - 例: `"openai/gpt-oss-20b"`, `"llm-jp/llm-jp-3.1-13b-instruct4"`
- **messages** (array): チャットメッセージの配列
    - 各メッセージは以下の形式:
        
        ```json
        {
          "role": "user" | "assistant" | "system",
          "content": "メッセージ内容"
        }
        ```
        

### オプションパラメータ

- **temperature** (float, デフォルト: 0.7): 生成テキストのランダム性を制御（0.0～2.0）
- **max_tokens** (integer, デフォルト: null): 生成する最大トークン数
- **stream** (boolean, デフォルト: false): ストリーミングレスポンスを使用するかどうか

### その他のパラメータ

OpenAI互換のその他のパラメータ（`top_p`, `frequency_penalty`, `presence_penalty`など）もサポートされています。

## レスポンス形式

### 非ストリーミングレスポンス

`stream=false`の場合、通常のJSONレスポンスが返されます。

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "openai/gpt-oss-20b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "こんにちは！どのようにお手伝いできますか？"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

### ストリーミングレスポンス

`stream=true`の場合、Server-Sent Events (SSE)形式でストリーミングレスポンスが返されます。

各チャンクは以下の形式:

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"openai/gpt-oss-20b","choices":[{"index":0,"delta":{"content":"こ"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"openai/gpt-oss-20b","choices":[{"index":0,"delta":{"content":"ん"},"finish_reason":null}]}

data: [DONE]
```

## 使用例

### 必要なライブラリのインストール

PythonでAPIを呼び出すには、OpenAIライブラリが必要です。以下のコマンドでインストールできます:

```bash
pip install openai
```

### 1. 非ストリーミング呼び出し（Python）

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.maas.mdx1.jp/v1",
    api_key="your-api-key-here",
)

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "user", "content": "こんにちは、自己紹介をお願いします。"}
    ],
    temperature=0.7,
    max_tokens=100,
    stream=False,
)

# アシスタントの返答を取得
print(completion.choices[0].message.content)

# トークン使用量
if completion.usage:
    print(f"\nトークン使用量:")
    print(f"  プロンプト:{completion.usage.prompt_tokens}")
    print(f"  生成:{completion.usage.completion_tokens}")
    print(f"  合計:{completion.usage.total_tokens}")
```

**出力例:**

```
こんにちは！私はAIアシスタントです。自然言語処理や質問応答などのタスクをお手伝いできます。何かお手伝いできることはありますか？

トークン使用量:
  プロンプト: 15
  生成: 45
  合計: 60
```

### 2. 非ストリーミング呼び出し（curl）

```bash
curl -X POST "https://api.maas.mdx1.jp/v1/chat/completions" \
  -H "Authorization: Bearer your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "messages": [
      {
        "role": "user",
        "content": "こんにちは、自己紹介をお願いします。"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 100,
    "stream": false
  }'
```

**出力例:**

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "openai/gpt-oss-20b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "こんにちは！私はAIアシスタントです。自然言語処理や質問応答などのタスクをお手伝いできます。何かお手伝いできることはありますか？"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 45,
    "total_tokens": 60
  }
}
```

### 3. ストリーミング呼び出し（Python）

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.maas.mdx1.jp/v1",
    api_key="your-api-key-here",
)

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "user", "content": "こんにちは、自己紹介をお願いします。"}
    ],
    temperature=0.7,
    max_tokens=100,
    stream=True,
)

for chunk in completion:
    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
```

**出力例:**

```
こんにちは！私はAIアシスタントです。自然言語処理や質問応答などのタスクをお手伝いできます。何かお手伝いできることはありますか？
```

**注意**: ストリーミングレスポンスでは、各チャンクが順次到着するため、リアルタイムでテキストが表示されます。

### 4. より高度な使用例（会話履歴を含む）

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.maas.mdx1.jp/v1",
    api_key="your-api-key-here",
)

completion = client.chat.completions.create(
    model="llm-jp/llm-jp-3.1-13b-instruct4",
    messages=[
        {
            "role": "system",
            "content": "あなたは親切で知識豊富なアシスタントです。"
        },
        {
            "role": "user",
            "content": "Pythonでリストをソートする方法を教えてください。"
        },
        {
            "role": "assistant",
            "content": "Pythonでリストをソートするには、`sorted()`関数または`list.sort()`メソッドを使用します。"
        },
        {
            "role": "user",
            "content": "降順にするにはどうすればいいですか？"
        }
    ],
    temperature=0.7,
    stream=False,
)

print(completion.choices[0].message.content)
```

## エラーハンドリング

APIは以下のHTTPステータスコードを返す可能性があります:

### 400 Bad Request

- **原因**: リクエストパラメータが不正、または指定されたモデルが存在しない
- **レスポンス例**:
    
    ```json
    {
      "detail": "Model openai/invalid-model not found"
    }
    ```
    

### 401 Unauthorized

- **原因**: APIキーが無効、または認証ヘッダーが正しくない
- **レスポンス例**:
    
    ```json
    {
      "detail": "Invalid API key"
    }
    ```
    
- **対処法**:
    - APIキーが正しく設定されているか確認
    - `Authorization: Bearer <api-key>`形式であることを確認

### 429 Too Many Requests

- **原因**: 1時間あたりのトークン制限を超えた、または同時リクエスト数が上限を超えた
- **レスポンス例**:
    
    ```json
    {
      "detail": "Hourly token limit exceeded. Current usage: 100000, Limit: 50000"
    }
    ```
    
    または
    
    ```json
    {
      "detail": "Too many concurrent requests. Please try again later."
    }
    ```
    
- **対処法**:
    - しばらく待ってから再試行

### 500 Internal Server Error

- **原因**: サーバー内部エラー
- **レスポンス例**:
    
    ```json
    {
      "detail": "Internal server error"
    }
    ```
    
- **対処法**:
    - しばらく待ってから再試行
    - 問題が続く場合は管理者に連絡

### エラーハンドリングの実装例

```python
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError

client = OpenAI(
    base_url="https://api.maas.mdx1.jp/v1",
    api_key="your-api-key-here",
)

try:
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": "こんにちは"}
        ],
        stream=False,
    )
    print(completion.choices[0].message.content)

except APIError as e:
    if e.status_code == 401:
        print("認証エラー: APIキーを確認してください")
    elif e.status_code == 429:
        print("レート制限エラー: しばらく待ってから再試行してください")
    elif e.status_code == 400:
        print(f"リクエストエラー:{e.message}")
    else:
        print(f"APIエラー{e.status_code}:{e.message}")

except APIConnectionError as e:
    print(f"接続エラー:{e}")

except APITimeoutError as e:
    print("タイムアウトエラー: リクエストがタイムアウトしました")

except Exception as e:
    print(f"予期しないエラー:{e}")
```

## 制限事項

- **タイムアウト**: リクエストのタイムアウトは1800秒（30分）
- **トークン制限**: APIキーごとに1時間あたりのトークン制限が設定されている場合があります

## ベストプラクティス

1. **エラーハンドリング**: すべてのAPI呼び出しで適切なエラーハンドリングを実装してください
2. **タイムアウト設定**: 長時間実行される可能性があるため、適切なタイムアウトを設定してください
3. **ストリーミングの使用**: 長いレスポンスが期待される場合は、ストリーミングモードを使用してユーザー体験を向上させてください
4. **リトライロジック**: 429エラーや一時的なエラーに対しては、指数バックオフを使用したリトライロジックを実装することを推奨します