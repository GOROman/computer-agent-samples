# Computer-Using Agent サンプル
【CUA】 - Computer-Using Agent - OpenAIのコンピュータ操作エージェントを触ってみた！人間不要時代の到来か！？

## 概要

このリポジトリはOpenAIのComputer-Using Agent (CUA)のサンプル実装を含んでいます。CUAはスクリーンショットを見て、クリック、タイピング、スクロールなどのアクションを実行することでコンピュータインターフェースと対話できる強力なAIエージェントです。

## 特徴

- コンピュータ環境を定義するための基本的な `Computer` 抽象クラス
- ブラウザ自動化のための `LocalPlaywright` 実装
- OpenAIのCUA APIと対話するための `Agent` クラス
- 簡単な対話のためのコマンドラインインターフェース
- 一般的なタスクのサンプルスクリプト：
  - 天気確認
  - Web検索と情報抽出
  - フォーム入力

## セットアップ

1. 必要な依存関係をインストールします：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. OpenAI APIキーを設定します：

```bash
export OPENAI_API_KEY="your-api-key"
```

または、`.env`ファイルを作成して以下のように記述します：

```
OPENAI_API_KEY=your-api-key
```

## 使用方法

### 基本的なCLI

エージェントと対話するためにCLIを実行します：

```bash
python cli.py --show
```

### サンプルスクリプト

特定の場所の天気を確認します：

```bash
python weather_example.py --location "東京" --show
```

Web検索を実行して情報を抽出します：

```bash
python search_example.py --query "最新のAIニュース" --show
```

Webサイトのフォームに入力します：

```bash
python form_example.py --show
```

## ファイル構成

- `computer.py`: コンピュータ環境のための基本クラス
- `local_playwright.py`: Playwrightを使用したComputerクラスの実装
- `agent.py`: OpenAI CUAエージェントの実装
- `cli.py`: エージェントと対話するためのコマンドラインインターフェース
- `weather_example.py`: 天気確認のサンプルスクリプト
- `search_example.py`: Web検索のサンプルスクリプト
- `form_example.py`: フォーム入力のサンプルスクリプト

## 参考資料

- [OpenAI Computer-Using Agent](https://openai.com/index/computer-using-agent/)
- [OpenAI CUA Sample App](https://github.com/openai/openai-cua-sample-app)
