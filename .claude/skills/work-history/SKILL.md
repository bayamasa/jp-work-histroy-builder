# /work-history スキル

対話形式で職務経歴書のYAMLデータを作成し、PDFを生成するスキル。

## トリガー

- 「職務経歴書を作成」「work-history作成」
- `/work-history`
- 「職務経歴書を更新してプレビュー」「PDFを再生成」→ **Step 6 へ直接ジャンプ**

## ワークフロー

### Step 1: 形式の確認

`AskUserQuestion` を使って職務経歴書の形式を確認する。

- **標準形式** (standard) - overview / phases / responsibilities / achievements
- **STAR法形式** (star) - situation / task / action / result

### Step 2: credential.yaml の確認

`AskUserQuestion` でユーザーに `.personal/credential.yaml` の準備状況を確認する。ファイルの存在チェックは行わない。

**質問: credential.yaml は準備できていますか？**

- **ある** → Step 3 へ進む
- **ない（今作成する）** → 作成手順を案内して **スキルを中断** する
- **あとで作成する** → credential.yaml なしで Step 3 へ進む（PDF生成時にエラーになる旨を伝える）

**「ない（今作成する）」の場合の案内**:

credential.yaml は `sample/credential.yaml` をテンプレートとしてコピーし、個人情報を編集して作成する。

```text
以下の手順で準備してください:

1. テンプレートをコピー:
   cp sample/credential.yaml .personal/credential.yaml

2. .personal/credential.yaml を直接編集して個人情報を入力してください。
   （氏名・住所・電話番号・メールアドレス等）

3. 準備ができたら再度 /work-history を実行してください。

※ sample/credential.yaml にサンプル値が記載されているので参考にしてください。
```

**重要**: credential.yaml には氏名・住所・電話番号等の個人情報が含まれる。セキュリティ上、対話形式での聞き取り、ファイルの読み取り、存在チェックは **絶対に行わない**。ユーザー自身がファイルを直接編集する運用とする。

### Step 3: 雛形の作成

まず既存データ（`.personal/resume.yaml`、Wantedly等のURL）から職歴情報を収集し、**会社・期間・プロジェクト名・使用技術・役割**など事実ベースの雛形YAMLを作成する。

STAR法のsituation / task / action / result や職務要約・ハイライト・自己PRなど **文章で表現が揺れる部分は空欄（プレースホルダー）** にしておく。

#### 聞き取りの原則

- **関連項目はまとめて聞く**: `AskUserQuestion` の `questions` パラメータで複数質問を同時に提示し、やり取り回数を減らす
- **スキップを常に選択肢に含める**: 任意項目は「スキップ」オプションを用意する
- **Webソースの活用**: ユーザーがWantedly・LinkedIn等のURLを提示した場合は `WebFetch` で情報を取得し、職歴データとして整理する
- **既存ファイルの活用**: `.personal/` に既存のYAMLファイルがある場合はそれを読み込み、修正ベースで進める
- **確認を挟む**: 推定した内容は `AskUserQuestion` でユーザーに確認を取ってから次へ進む

#### `abbreviate_env` の自動判定

同一会社内で `environment` の内容が同一のプロジェクトが複数ある場合、最初のプロジェクトを基準とし、2つ目以降に `abbreviate_env: true` を自動で付与する。ユーザーに確認を取ってから適用する。

#### 雛形作成フロー

各項目の詳細スキーマは `references/yaml-schema.md` を参照。

**Round 1**: 作成日 (`date`) + 情報ソース

- `AskUserQuestion` で以下を同時に聞く:
  - 作成日（デフォルト選択肢に本日の日付を含める）
  - 職歴情報のソース（Wantedly等のURLがあれば提示してもらう）

**Round 2**: 職務経歴 (`experience`) の事実確認

- 既存データ/Webソースから会社・期間・プロジェクト名・使用技術・役割を整理して表で表示
- `AskUserQuestion` で確認を取る

**Round 3**: 副業・その他経歴 (`side_experience`)

- 該当する場合のみ

**Round 4**: テクニカルスキル (`technical_skills`)

- カテゴリ別 (OS, 言語, DB, FW等)

**Round 5**: 資格 (`qualifications`)

- 既存の履歴書データがあればそこから転記

### Step 4: 雛形の保存

雛形YAMLをコードブロックでユーザーに表示し、`AskUserQuestion` で「保存する」「修正あり」を確認する。

確認後、`.personal/work_history.yaml` に保存する。

以下の項目はプレースホルダーのまま保存される:

- `summary` (職務要約)
- `highlights` (ハイライト)
- `situation` / `task` / `action` / `result` (STAR法の場合)
- `self_pr` (自己PR)

### Step 5: 文章部分の対話的な作成

保存した雛形をベースに、プレースホルダー部分を対話形式で埋めていく。

**Round 1**: 職務要約 (`summary`) + ハイライト (`highlights`)

- ユーザーの経歴全体を踏まえてドラフトを提案 → 修正

**Round 2**: 各プロジェクトのSTAR（プロジェクト単位で順番に）

- `situation` / `task` / `action` / `result` をプロジェクトごとに聞き取り
- ユーザーが箇条書きで答えたら文章に整形して確認

**Round 3**: 自己PR (`self_pr`)

- タイトルと本文のペア

各Roundで `.personal/work_history.yaml` を更新する。

### Step 6: PDF 生成・表示

Makefileのターゲットを使ってPDFを生成し、`open` コマンドで表示する。

**標準形式**:

```bash
make build-wh-standard YAML=.personal/work_history.yaml CRED=.personal/credential.yaml OUTPUT=output/work-history.pdf
```

**STAR法形式**:

```bash
make build-wh-star YAML=.personal/work_history.yaml CRED=.personal/credential.yaml OUTPUT=output/work-history.pdf
```

生成後、`open output/work-history.pdf` でPDFビューアを開く。

### Step 7: 確認・修正ループ

PDF表示後、ユーザーのフィードバックに応じて対応する:

- **問題なし** → 完了
- **YAMLデータの修正** → `.personal/work_history.yaml` を編集して再生成
- **credential.yaml の修正** → ユーザーが直接編集後、再生成コマンドのみ実行
- **レイアウト・表示の問題** → `src/jp_tenshoku_docs_builder/work_history/builder.py` のビルダーコードを修正して再生成
- **開発環境の重複** → 同一会社内で環境が同じプロジェクトには `abbreviate_env: true` を提案し、「同環境のため省略」表示にする

## ファイル構成

```text
.personal/
  credential.yaml    # 個人情報（手動編集、対話で聞き取り禁止）
  work_history.yaml  # 職務経歴書データ（スキルで生成）
output/
  work-history.pdf   # 生成された職務経歴書PDF
```

## リファレンス

- YAMLスキーマ詳細: `references/yaml-schema.md`
- サンプルデータ: `sample/work_history_star.yaml`, `sample/work_history_standard.yaml`
- Pydanticモデル: `src/jp_tenshoku_docs_builder/work_history/models.py`
