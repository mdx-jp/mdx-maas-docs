from openai import OpenAI

from settings import MAAS_API_BASE_URL, MAAS_API_KEY

# APIを呼び出すインスタンスを作成
client = OpenAI(
    base_url=MAAS_API_BASE_URL,
    api_key=MAAS_API_KEY,
)

# APIを呼び出す
completion = client.chat.completions.create(
    model="llm-jp/llm-jp-4-32b-a3b-thinking",
    messages=[{"role": "user", "content": "こんにちは！"}],
)

# 回答を表示
print(completion.choices[0].message.content)
