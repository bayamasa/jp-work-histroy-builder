# jp-tenshoku-docs-builder - 職務経歴書・履歴書 PDF Generator

YAMLファイルから日本語の職務経歴書・履歴書PDFを生成するCLIツールです。

## 必要環境

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (パッケージマネージャー)

## セットアップ

```bash
uv sync
```

## 使い方

### Make（サンプルPDF生成）

```bash
make sample-wh-standard   # 職務経歴書（標準） → output/work-history-standard.pdf
make sample-wh-star        # 職務経歴書（STAR法） → output/work-history-star.pdf
make sample-resume         # 履歴書 → output/resume.pdf
```

### Make（任意のYAMLを指定）

```bash
make build-wh-standard YAML=my_data.yaml CRED=.personal/credential.yaml OUTPUT=my_output.pdf
make build-wh-star YAML=my_data.yaml CRED=.personal/credential.yaml OUTPUT=my_output.pdf
make build-resume YAML=my_resume.yaml CRED=.personal/credential.yaml OUTPUT=my_resume.pdf
```

### CLI 直接実行

```bash
# 職務経歴書（標準）
uv run python -m jp_tenshoku_docs_builder sample/work_history_standard.yaml -c sample/credential.yaml -o output/work-history-standard.pdf

# 職務経歴書（STAR法）
uv run python -m jp_tenshoku_docs_builder sample/work_history_star.yaml -c sample/credential.yaml -o output/work-history-star.pdf --format star

# 履歴書
uv run python -m jp_tenshoku_docs_builder sample/resume.yaml -c sample/credential.yaml -o output/resume.pdf --type resume

# フォントディレクトリを指定
uv run python -m jp_tenshoku_docs_builder sample/work_history_standard.yaml -c sample/credential.yaml -o output/work-history-standard.pdf --font-dir ./fonts
```

### CLIオプション

| オプション | 説明 | デフォルト |
|---|---|---|
| `input` | 入力YAMLファイルパス（必須） | - |
| `-c, --credential` | 個人情報YAMLファイルパス（必須） | - |
| `-o, --output` | 出力PDFファイルパス | `output/output.pdf` |
| `--font-dir` | 日本語フォントファイルのディレクトリ | なし（自動検索） |
| `--type` | 文書タイプ (`work-history` / `resume`) | `work-history` |
| `--format` | 表示形式 (`standard` / `star`、職務経歴書のみ) | `standard` |

## YAMLデータ構造

個人情報（氏名・住所・電話番号等）は `credential.yaml` に分離しています。
`-c` オプションで指定すると、メインのYAMLにマージされます（credential側の値が優先）。

### credential.yaml（個人情報）

| フィールド | 説明 |
|---|---|
| `name` | 氏名 |
| `name_kana` | ふりがな（履歴書用） |
| `birth_day` | 生年月日（履歴書用） |
| `gender` | 性別 |
| `cell_phone` | 携帯電話番号 |
| `email` | メールアドレス |
| `address_kana` / `address` / `address_zip` | 現住所 |
| `tel` / `fax` | 電話・FAX |
| `address_kana2` / `address2` / `address_zip2` | 連絡先 |
| `tel2` / `fax2` | 連絡先電話・FAX |

実際の個人情報は `.personal/credential.yaml` に配置し、Git管理外としてください。
`sample/credential.yaml` にサンプルがあります。

### 職務経歴書

| セクション | 説明 |
|---|---|
| `date` | 作成日（必須） |
| `name` | 氏名（必須、credential.yamlから供給可） |
| `summary` | 職務要約 |
| `highlights` | 活かせる経験・知識・技術 |
| `experience` | 職務経歴 |
| `side_experience` | 副業・その他経歴 |
| `technical_skills` | テクニカルスキル |
| `qualifications` | 資格 |
| `self_pr` | 自己PR |

#### 表示形式

- **standard** - 概要・担当フェーズ・業務内容・実績をそのまま記載する標準形式
- **star** - Situation / Task / Action / Result で構造化して記載するSTAR法形式

### 履歴書

| セクション | 説明 |
|---|---|
| `date` | 作成日（必須） |
| `education` | 学歴（year, month, value のリスト） |
| `experience` | 職歴（year, month, value のリスト） |
| `licences` | 免許・資格（year, month, value のリスト） |
| `commuting_time` | 通勤時間 |
| `dependents` | 扶養家族数 |
| `spouse` | 配偶者の有無 |
| `supporting_spouse` | 配偶者の扶養義務 |
| `hobby` | 趣味・特技 |
| `motivation` | 志望動機 |
| `request` | 本人希望記入欄 |

個人情報フィールド（`name_kana`, `name`, `birth_day`, `gender`, `cell_phone`, `email`, `address_*`, `tel`, `fax` 等）は credential.yaml から供給されます。

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
├── src/jp_tenshoku_docs_builder/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py            # 共通CLIエントリポイント
│   ├── fonts.py           # 共通フォント検索・登録
│   ├── work_history/      # 職務経歴書
│   │   ├── models.py      # Pydantic データモデル
│   │   ├── loader.py      # YAML読み込み・バリデーション
│   │   ├── builder.py     # PDF生成 (ReportLab Platypus)
│   │   └── styles.py      # PDF スタイル定義
│   └── resume/            # 履歴書
│       ├── models.py      # Pydantic データモデル
│       ├── loader.py      # YAML読み込み・バリデーション
│       └── builder.py     # PDF生成 (ReportLab Canvas API)
├── sample/
│   ├── credential.yaml             # 個人情報サンプル
│   ├── work_history_standard.yaml  # 職務経歴書 標準フォーマットのサンプル
│   ├── work_history_star.yaml      # 職務経歴書 STAR法フォーマットのサンプル
│   └── resume.yaml                 # 履歴書サンプル（キャリア情報のみ）
├── .personal/             # 個人データ格納先（中身は.gitignore）
├── Makefile               # ビルド・テスト用コマンド
├── output/                # 生成PDF出力先（.gitignore）
├── fonts/                 # 日本語フォント配置先
├── tests/
│   ├── test_models.py
│   └── test_resume_models.py
└── pyproject.toml
```

## Docker

Python や uv をインストールせずに Docker 経由で実行できます。

```bash
# ビルド
docker build -t jp-tenshoku-docs-builder .

# 職務経歴書
docker run --rm -v "$(pwd)":/work jp-tenshoku-docs-builder /work/sample/work_history_standard.yaml -c /work/sample/credential.yaml -o /work/output/work-history-standard.pdf

# STAR法フォーマットで生成
docker run --rm -v "$(pwd)":/work jp-tenshoku-docs-builder /work/sample/work_history_star.yaml -c /work/sample/credential.yaml -o /work/output/work-history-star.pdf --format star

# 履歴書
docker run --rm -v "$(pwd)":/work jp-tenshoku-docs-builder /work/sample/resume.yaml -c /work/sample/credential.yaml -o /work/output/resume.pdf --type resume
```

> **Note:** `fonts/` ディレクトリに IPAex フォントが配置された状態でイメージをビルドしてください。コンテナ内にフォントがコピーされるため `--font-dir` の指定は不要です。

## テスト

```bash
uv run pytest tests/ -v
```

## ライセンス

Apache License 2.0

同封の IPA フォントは [IPA フォントライセンス v1.0](https://moji.or.jp/ipafont/license/) に従って再配布しています。
