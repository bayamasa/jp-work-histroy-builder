# jpcv - 職務経歴書 PDF Generator

YAMLファイルから日本語の職務経歴書PDFを生成するCLIツールです。

## 必要環境

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (パッケージマネージャー)

## セットアップ

```bash
uv sync
```

## 使い方

```bash
# 標準フォーマットで生成
uv run python -m jpcv sample/standard.yaml -o output.pdf

# STAR法フォーマットで生成
uv run python -m jpcv sample/star.yaml -o output.pdf --format star

# フォントディレクトリを指定
uv run python -m jpcv sample/standard.yaml -o output.pdf --font-dir ./fonts
```

### CLIオプション

| オプション | 説明 | デフォルト |
|---|---|---|
| `input` | 入力YAMLファイルパス（必須） | - |
| `-o, --output` | 出力PDFファイルパス | `output.pdf` |
| `--font-dir` | 日本語フォントファイルのディレクトリ | なし（自動検索） |
| `--format` | 表示形式 (`standard` / `star`) | `standard` |

## YAMLデータ構造

### 共通セクション

| セクション | 説明 |
|---|---|
| `date` | 作成日（必須） |
| `name` | 氏名（必須） |
| `summary` | 職務要約 |
| `highlights` | 活かせる経験・知識・技術 |
| `experience` | 職務経歴 |
| `side_experience` | 副業・その他経歴 |
| `technical_skills` | テクニカルスキル |
| `qualifications` | 資格 |
| `self_pr` | 自己PR |

### 表示形式

- **standard** - 概要・担当フェーズ・業務内容・実績をそのまま記載する標準形式
- **star** - Situation / Task / Action / Result で構造化して記載するSTAR法形式

### PDFセクション配置順

1. ヘッダー（タイトル・日付・氏名）
2. 職務要約
3. 活かせる経験・知識・技術
4. 職務経歴
5. 副業・その他経歴
6. テクニカルスキル
7. 資格
8. 自己PR

サンプルYAMLは `sample/` ディレクトリを参照してください。

## フォント

日本語フォントの検索順序:

1. `--font-dir` で指定したディレクトリ
2. プロジェクト直下の `fonts/` ディレクトリ
3. OS のシステムフォントディレクトリ

対応フォント（優先順）:

| 種類 | フォント |
|---|---|
| ゴシック体 | IPAexゴシック > Noto Sans JP > AppleGothic (macOS) |
| 明朝体 | IPAex明朝 > Noto Serif JP > AppleMyungjo (macOS) |

`fonts/` ディレクトリに IPAex フォント (`ipaexg.ttf`, `ipaexm.ttf`) を配置するのが最も簡単です。

## プロジェクト構成

```
├── src/jpcv/
│   ├── models.py    # Pydantic データモデル
│   ├── loader.py    # YAML読み込み・バリデーション
│   ├── builder.py   # PDF生成 (ReportLab Platypus)
│   ├── styles.py    # PDF スタイル定義
│   ├── fonts.py     # フォント検索・登録
│   └── cli.py       # CLIエントリポイント
├── sample/
│   ├── standard.yaml  # 標準フォーマットのサンプル
│   └── star.yaml      # STAR法フォーマットのサンプル
├── fonts/             # 日本語フォント配置先
├── tests/
│   └── test_models.py
└── pyproject.toml
```

## Docker

Python や uv をインストールせずに Docker 経由で実行できます。

```bash
# ビルド
docker build -t jpcv .

# 実行（カレントディレクトリの YAML を入力、PDF を出力）
docker run --rm -v "$(pwd)":/work jpcv /work/sample/standard.yaml -o /work/output.pdf

# STAR法フォーマットで生成
docker run --rm -v "$(pwd)":/work jpcv /work/sample/star.yaml -o /work/output.pdf --format star
```

> **Note:** `fonts/` ディレクトリに IPAex フォントが配置された状態でイメージをビルドしてください。コンテナ内にフォントがコピーされるため `--font-dir` の指定は不要です。

## テスト

```bash
uv run pytest tests/ -v
```

## ライセンス

Apache License 2.0

同封の IPA フォントは [IPA フォントライセンス v1.0](https://moji.or.jp/ipafont/license/) に従って再配布しています。
