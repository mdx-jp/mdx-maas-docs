# mdx-MaaS API ドキュメント

学術機関向けの生成 AI 推論基盤 **mdx-MaaS (Model as a Service)** の API ドキュメントです。

**🌐 ユーザーポータル（利用申請・利用可能モデル・FAQ）: [https://maas.mdx1.jp/](https://maas.mdx1.jp/)**

## mdx-MaaS とは

mdx-MaaS は、データ活用社会創成プラットフォーム [mdx](https://mdx.jp/mdx1/) 上で運用している、学術機関が生成 AI モデル（LLM）を安全かつ効率的に活用するための推論基盤です。

研究・開発で柔軟に使える **OpenAI 互換の API エンドポイント** を主軸に提供しています。GUI が必要な用途向けには、チャットサービスも利用できます。

現在は **β 版テストユーザーを募集中（無料）** です。利用申請は [ユーザーポータル](https://maas.mdx1.jp/) から行えます。

## ドキュメント

| ドキュメント | 内容 |
| --- | --- |
| [即時応答 API（Chat Completions）](chat_completions_api_document.md) | リクエストに対して推論結果をリアルタイムに返す API。対話的な用途やリアルタイム処理向け |
| [Batch API](batch_inference_api_document.md) | 複数のリクエストをファイルでまとめて投入し、非同期に処理する API。大量テキストの分類・翻訳・要約向け |
| [Usage API](usage_api_document.md) | 利用状況を確認する API |

## クイックスタート

1. [ユーザーポータル](https://maas.mdx1.jp/) の申請フォームから利用を申請します
2. 事務局での確認後、API キーがメールで届きます
3. OpenAI 互換のクライアントから利用できます

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.maas.mdx1.jp/v1",
    api_key="your-api-key-here",
    timeout=1800,  # 30 分
)
```

> [!NOTE]
> 計算資源を有効に使うため、アクセスがないときはモデルを停止しています。しばらく利用がなかったモデルへの最初のリクエストは、応答までに 15〜20 分程度かかることがあります。クライアント側のタイムアウトは 30 分程度に設定してください。

利用できるモデルは、[ユーザーポータル](https://maas.mdx1.jp/) の「現在利用可能なモデル」を参照してください。

## 関連リンク

- [mdx-MaaS ユーザーポータル](https://maas.mdx1.jp/)
- [チャットサービス利用案内](https://maas.mdx1.jp/chat.html)
- [アップデート履歴](https://maas.mdx1.jp/updates.html)
- 解説記事（Zenn）: [mdx MaaSのAPIでLLM-jp-4を使う 第0回：準備](https://zenn.dev/suzumura_lab/articles/d56a1805bd7efd)
- 解説記事（Zenn）: [mdx MaaSのAPIでLLM-jp-4を使う 第1回：APIの呼び出しと回答の取り出し](https://zenn.dev/suzumura_lab/articles/50b62687aa9205)
- [AXIES2025](https://axies.secretari.jp/conf2025/) 発表資料

## 問い合わせ

- アカウント発行済みの方: Slack ワークスペースからお問い合わせください
- アカウント未発行の方: [mdx-maas-support@mail.mdx.jp](mailto:mdx-maas-support@mail.mdx.jp)

詳しくは [ユーザーポータル](https://maas.mdx1.jp/) をご覧ください。
