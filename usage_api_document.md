# 使用量確認 API ドキュメント

## 概要

使用量確認 API は、認証 API キーの現在のトークン使用量・上限・残量を取得するためのエンドポイントである。Chat Completions API と Batch 推論 API のそれぞれについて、短期ウィンドウ（直近 N 時間）と長期ウィンドウ（直近 N 日）のスライディング合計を返す。

**エンドポイント**: `GET /v1/usage`

**ベース URL**: [https://api.maas.mdx1.jp](https://api.maas.mdx1.jp)

### ユースケース

- レートリミット（429 Too Many Requests）に達する前に、現在の使用量を確認して投入ペースを調整する
- ダッシュボードやモニタリングツールで API キーごとの利用状況を可視化する
- バッチ投入前に「長期ウィンドウに余裕があるか」を確認する

---

## 認証

すべてのリクエストには API キーによる認証が必要である。HTTP ヘッダーに Bearer トークン形式で指定する。

```
Authorization: Bearer <your-api-key>
```

返ってくる使用量は、**そのリクエストで認証された API キー単独の集計**である。他の API キーの使用量は取得できない。

---

## リクエスト

リクエストパラメータはなく、認証ヘッダーのみで呼び出す。

```http
GET /v1/usage HTTP/1.1
Host: api.maas.mdx1.jp
Authorization: Bearer <your-api-key>
```

---

## レスポンス形式

レスポンスは JSON 形式で、`chat`（Chat Completions API の使用量）と `batch`（Batch 推論 API の使用量）の 2 つのセクションに分かれる。それぞれが「短期ウィンドウ」と「長期ウィンドウ」を持つ。

### レスポンス例（上限が設定されているケース）

```json
{
  "api_key_id": 1,
  "chat": {
    "short_window": {
      "window_hours": 3,
      "used_tokens": 12345,
      "limit_tokens": 100000,
      "remaining_tokens": 87655
    },
    "long_window": {
      "window_days": 7,
      "used_tokens": 234567,
      "limit_tokens": 1000000,
      "remaining_tokens": 765433
    }
  },
  "batch": {
    "short_window": {
      "window_hours": 3,
      "used_tokens": 50000,
      "limit_tokens": 200000,
      "remaining_tokens": 150000
    },
    "long_window": {
      "window_days": 7,
      "used_tokens": 500000,
      "limit_tokens": 2000000,
      "remaining_tokens": 1500000
    }
  }
}
```

### レスポンス例（上限が未設定のケース）

上限が設定されていない（無制限）ウィンドウでは、`limit_tokens` と `remaining_tokens` が `null` として返る。使用量 `used_tokens` は上限の有無に関わらず常に集計値を返す。

```json
{
  "api_key_id": 1,
  "chat": {
    "short_window": {
      "window_hours": 3,
      "used_tokens": 12345,
      "limit_tokens": null,
      "remaining_tokens": null
    },
    "long_window": {
      "window_days": 7,
      "used_tokens": 234567,
      "limit_tokens": null,
      "remaining_tokens": null
    }
  },
  "batch": {
    "short_window": {
      "window_hours": 3,
      "used_tokens": 0,
      "limit_tokens": null,
      "remaining_tokens": null
    },
    "long_window": {
      "window_days": 7,
      "used_tokens": 0,
      "limit_tokens": null,
      "remaining_tokens": null
    }
  }
}
```

### フィールド説明

| フィールド | 型 | 説明 |
|------------|------|------|
| `api_key_id` | integer | 認証 API キーの内部 ID |
| `chat.short_window` | object | Chat の短期ウィンドウ集計 |
| `chat.long_window` | object | Chat の長期ウィンドウ集計 |
| `batch.short_window` | object | Batch 推論の短期ウィンドウ集計 |
| `batch.long_window` | object | Batch 推論の長期ウィンドウ集計 |

各 `*_window` オブジェクトの中身:

| フィールド | 型 | 説明 |
|------------|------|------|
| `window_hours` | integer | 短期ウィンドウの長さ（時間単位、`short_window` のみ） |
| `window_days` | integer | 長期ウィンドウの長さ（日数単位、`long_window` のみ） |
| `used_tokens` | integer | このウィンドウ内で消費された合計トークン数（input + output） |
| `limit_tokens` | integer \| null | このウィンドウの上限トークン数。`null` は無制限 |
| `remaining_tokens` | integer \| null | 残量（`limit_tokens - used_tokens`、最小 0）。`limit_tokens` が `null` の場合は `null` |

### ウィンドウの仕様

- **スライディングウィンドウ**: 「ちょうど直近 N 時間 / N 日」を基準とした移動集計である。固定の暦時間（毎日 0 時リセット等）ではない。
- **集計値**: Chat Completions API および Batch 推論 API の応答に含まれた `total_tokens`（input + output）の合計値。
- **Chat / Batch の分離**: Chat 用のウィンドウ集計には Chat の使用量のみ、Batch 用のウィンドウ集計には Batch の使用量のみが含まれる。両者は独立に上限判定される。
- **ウィンドウ幅の既定値**: 短期 3 時間、長期 7 日。実際の値はレスポンスの `window_hours` / `window_days` を参照すること（管理者の設定により変わる可能性がある）。

---

## 使用例

### curl

```bash
curl -s -H "Authorization: Bearer ${API_KEY}" \
  https://api.maas.mdx1.jp/v1/usage | jq .
```

### Python

```python
import os
import httpx

API_KEY = os.environ["API_KEY"]
BASE_URL = "https://api.maas.mdx1.jp"

resp = httpx.get(
    f"{BASE_URL}/v1/usage",
    headers={"Authorization": f"Bearer {API_KEY}"},
    timeout=10.0,
)
resp.raise_for_status()
data = resp.json()

chat_short = data["chat"]["short_window"]
print(
    f"Chat short ({chat_short['window_hours']}h): "
    f"{chat_short['used_tokens']} / {chat_short['limit_tokens']}"
)

batch_long = data["batch"]["long_window"]
print(
    f"Batch long ({batch_long['window_days']}d): "
    f"{batch_long['used_tokens']} / {batch_long['limit_tokens']}"
)
```

### バッチ投入前のチェック例

長期ウィンドウの残量が一定以上ある場合のみバッチを投入する、といった制御に利用できる。

```python
data = httpx.get(f"{BASE_URL}/v1/usage", headers=headers).json()
remaining = data["batch"]["long_window"]["remaining_tokens"]

# 上限が無制限（None）の場合は常に投入可
if remaining is None or remaining >= 500_000:
    # バッチを投入する
    ...
else:
    print(f"Batch の長期ウィンドウ残量が不足: {remaining}")
```

---

## エラーレスポンス

### 401 Unauthorized

- **原因**: API キーが未指定、形式不正、または無効
- **レスポンス例**:

    ```json
    {
      "detail": "Invalid API key"
    }
    ```

- **対処法**:
    - `Authorization: Bearer <api-key>` ヘッダーが指定されているか確認する
    - API キーが有効か管理者に確認する

---

## 制限事項・注意事項

- **取得できるのは自分の API キーの使用量のみ**。他ユーザーの使用量は取得できない。
- **集計はリアルタイム**だが、Chat の使用量はリクエスト完了後に記録される。ストリーミング応答の場合、ストリーム終了後に集計に反映される。
- **`used_tokens` の単位**: モデルごとの tokenizer で算出された値である。クライアント側で再計算した値とは多少ずれる可能性がある。
- **レートリミット超過時の挙動**: `/v1/usage` 自体にはレートリミットはかからない（軽量な参照 API のため）。ただし、Chat / Batch 側のレートリミット超過時は 429 が返る点に注意。詳細は以下を参照。

---

## 関連ドキュメント

- [chat_completions_api_document.md](chat_completions_api_document.md) - Chat Completions API（Chat 用ウィンドウ上限超過時の挙動）
- [batch_inference_api_document.md](batch_inference_api_document.md) - バッチ推論 API（Batch 用ウィンドウ上限超過時の挙動）
