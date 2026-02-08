# jb-workhistory - 職務経歴書・履歴書 PDF Generator

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
make sample-wh-standard   # 職務経歴書（標準） → work-history-standard.pdf
make sample-wh-star        # 職務経歴書（STAR法） → work-history-star.pdf
make sample-resume         # 履歴書 → resume.pdf
```

### Make（任意のYAMLを指定）

```bash
make build-wh-standard YAML=my_data.yaml OUTPUT=my_output.pdf
make build-wh-star YAML=my_data.yaml OUTPUT=my_output.pdf
make build-resume YAML=my_resume.yaml OUTPUT=my_resume.pdf
```

### CLI 直接実行

```bash
# 職務経歴書（標準）
uv run python -m jb_workhistory sample/work_history_standard.yaml -o work-history-standard.pdf

# 職務経歴書（STAR法）
uv run python -m jb_workhistory sample/work_history_star.yaml -o work-history-star.pdf --format star

# 履歴書
uv run python -m jb_workhistory sample/resume.yaml -o resume.pdf --type resume

# フォントディレクトリを指定
uv run python -m jb_workhistory sample/work_history_standard.yaml -o work-history-standard.pdf --font-dir ./fonts
```

### CLIオプション

| オプション | 説明 | デフォルト |
|---|---|---|
| `input` | 入力YAMLファイルパス（必須） | - |
| `-o, --output` | 出力PDFファイルパス | `output.pdf` |
| `--font-dir` | 日本語フォントファイルのディレクトリ | なし（自動検索） |
| `--type` | 文書タイプ (`work-history` / `resume`) | `work-history` |
| `--format` | 表示形式 (`standard` / `star`、職務経歴書のみ) | `standard` |

## YAMLデータ構造

### 職務経歴書

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

#### 表示形式

- **standard** - 概要・担当フェーズ・業務内容・実績をそのまま記載する標準形式
- **star** - Situation / Task / Action / Result で構造化して記載するSTAR法形式

### 履歴書

| セクション | 説明 |
|---|---|
| `date` | 作成日（必須） |
| `name_kana` | ふりがな（必須） |
| `name` | 氏名（必須） |
| `birth_day` | 生年月日（必須） |
| `gender` | 性別 |
| `cell_phone` | 携帯電話番号 |
| `email` | メールアドレス |
| `address_kana` / `address` / `address_zip` | 現住所（ふりがな・住所・郵便番号） |
| `tel` / `fax` | 電話・FAX |
| `address_kana2` / `address2` / `address_zip2` | 連絡先 |
| `tel2` / `fax2` | 連絡先電話・FAX |
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
├── src/jb_workhistory/
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
│   ├── work_history_standard.yaml  # 職務経歴書 標準フォーマットのサンプル
│   ├── work_history_star.yaml     # 職務経歴書 STAR法フォーマットのサンプル
│   └── resume.yaml        # 履歴書サンプル
├── Makefile               # ビルド・テスト用コマンド
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
docker build -t jb-workhistory .

# 職務経歴書
docker run --rm -v "$(pwd)":/work jb-workhistory /work/sample/work_history_standard.yaml -o /work/work-history-standard.pdf

# STAR法フォーマットで生成
docker run --rm -v "$(pwd)":/work jb-workhistory /work/sample/work_history_star.yaml -o /work/work-history-star.pdf --format star

# 履歴書
docker run --rm -v "$(pwd)":/work jb-workhistory /work/sample/resume.yaml -o /work/resume.pdf --type resume
```

> **Note:** `fonts/` ディレクトリに IPAex フォントが配置された状態でイメージをビルドしてください。コンテナ内にフォントがコピーされるため `--font-dir` の指定は不要です。

## テスト

```bash
uv run pytest tests/ -v
```

## ライセンス

Apache License 2.0

同封の IPA フォントは [IPA フォントライセンス v1.0](https://moji.or.jp/ipafont/license/) に従って再配布しています。
