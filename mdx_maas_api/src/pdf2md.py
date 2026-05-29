from pathlib import Path

from markitdown import MarkItDown

# 入出力ファイルの指定
INPUT_FILE = "./data/31_266.pdf"
OUTPUT_FILE = f"./data/{Path(INPUT_FILE).stem}.md"

# PDFをMarkdownに変換
md = MarkItDown(enable_plugins=False)
result = md.convert(INPUT_FILE)
print(f"{len(result.text_content)=}")  # 文字数を表示

# 結果をファイルに保存
with open(OUTPUT_FILE, "w") as f:
    f.write(result.text_content)
