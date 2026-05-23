from openai import OpenAI

from settings import MAAS_API_BASE_URL, MAAS_API_KEY

STREAMING = True

if __name__ == "__main__":
    # APIを呼び出すインスタンスを作成
    client = OpenAI(
        base_url=MAAS_API_BASE_URL,
        api_key=MAAS_API_KEY,
    )

    # APIを呼び出す
    completion = client.chat.completions.create(
        model="llm-jp/llm-jp-4-32b-a3b-thinking",  # モデル名
        messages=[
            # システムプロンプト
            {
                "role": "system",
                "content": "あなたは優秀な漫才師です。ユーザーの質問に答えてください。",
            },
            # ユーザープロンプト
            {"role": "user", "content": "フーリエ変換について教えてください。"},
        ],
        temperature=0.5,
        stream=STREAMING,
    )

    # 回答を表示
    if STREAMING:
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta:
                text = chunk.choices[0].delta.content
                if text:
                    print(text, flush=True, end="")
    else:
        print(completion.choices[0].message.content)
