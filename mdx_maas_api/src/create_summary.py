from pathlib import Path

from openai import OpenAI

from settings import MAAS_API_BASE_URL, MAAS_API_KEY

INPUT_FILE = "./data/31_266.md"

if __name__ == "__main__":
    # 入力ファイルの内容を読み込む
    with open(INPUT_FILE, "r") as f:
        text = f.read()

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
                "content": "あなたは優秀な編集者です。ユーザーのリクエストに対応してください。",
            },
            # ユーザープロンプト
            {"role": "user", "content": "次の内容を要約してください。\n\n" + text},
        ],
        temperature=0,  # 再現性を高めるために0に設定
    )

    # 回答を出力
    with open(f"./data/{Path(INPUT_FILE).stem}_summary.md", "w") as f:
        f.write(completion.choices[0].message.content)
