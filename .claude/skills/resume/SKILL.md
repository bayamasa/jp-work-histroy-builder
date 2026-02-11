# /resume スキル

対話形式で職務経歴書・履歴書のYAMLデータを作成し、PDFを生成するスキル。

## トリガー

- 「職務経歴書を作成」「履歴書を作成」「resume作成」
- `/resume`

## ワークフロー

### Step 1: 文書タイプの確認

`AskUserQuestion` を使ってユーザーに作成する文書タイプを確認する。

**質問1: 文書タイプ**

- **職務経歴書** (work-history)
- **履歴書** (resume)
- **両方**

**質問2: 職務経歴書の形式** (職務経歴書を含む場合のみ)

- **標準形式** (standard) - overview / phases / responsibilities / achievements
- **STAR法形式** (star) - situation / task / action / result

2つの質問は `AskUserQuestion` の `questions` パラメータで同時に提示する（職務経歴書を含まない場合は質問1のみ）。

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

3. 準備ができたら再度 /resume を実行してください。

※ sample/credential.yaml にサンプル値が記載されているので参考にしてください。
```

**重要**: credential.yaml には氏名・住所・電話番号等の個人情報が含まれる。セキュリティ上、対話形式での聞き取りは **絶対に行わない**。ユーザー自身がファイルを直接編集する運用とする。

### Step 3: 対話形式でのデータ聞き取り

選択された文書タイプに応じて、`AskUserQuestion` を活用してYAMLデータの各項目を聞き取る。

#### 聞き取りの原則

- **関連項目はまとめて聞く**: `AskUserQuestion` の `questions` パラメータで複数質問を同時に提示し、やり取り回数を減らす
- **スキップを常に選択肢に含める**: 任意項目は「スキップ」オプションを用意する
- **Webソースの活用**: ユーザーがWantedly・LinkedIn等のURLを提示した場合は `WebFetch` で情報を取得し、職歴データとして整理する
- **日付の逆算**: 学歴は最終卒業年と浪人・留学等の年数から高校入学まで逆算できる。ユーザーに全日付を入力させず、最小限の情報から計算する
- **確認を挟む**: 逆算・推定した内容は `AskUserQuestion` でユーザーに確認を取ってから次へ進む
- **既存ファイルの活用**: `.personal/` に既存のYAMLファイルがある場合はそれを読み込み、修正ベースで進める

#### 履歴書の聞き取りフロー

各項目の詳細スキーマは `references/yaml-schema.md` の「履歴書」セクションを参照。

**Round 1**: 作成日

- `AskUserQuestion` で作成日を聞く（デフォルト選択肢に本日の日付を含める）

**Round 2**: 学歴 (`education`)

- 大学の卒業年月を聞く。浪人・留学等があれば年数を聞き、高校入学まで逆算する
- 学校名・学部を `AskUserQuestion` で聞く（複数質問を同時に提示）
- 逆算結果を表で表示し、確認を取る

**Round 3**: 職歴 (`experience`)

- `AskUserQuestion` で職歴を聞く。URLの提示があれば `WebFetch` で取得する
- 入社・配属・退職を時系列で整理し、確認を取る

**Round 4**: 免許・資格 (`licences`)

- `AskUserQuestion` で「年, 月, 資格名」形式で聞く

**Round 5**: 通勤時間 + 扶養情報 + 趣味（まとめて聞く）

- `AskUserQuestion` の `questions` で以下を同時に提示:
  - 通勤時間 (`commuting_time`)
  - 扶養情報 (`dependents`, `spouse`, `supporting_spouse`) - よくあるパターンを選択肢に
  - 趣味・特技 (`hobby`)

**Round 6**: 志望動機 + 希望欄（まとめて聞く）

- `AskUserQuestion` の `questions` で以下を同時に提示:
  - 志望動機 (`motivation`)
  - 本人希望記入欄 (`request`)

#### 職務経歴書の聞き取りフロー

各項目の詳細スキーマは `references/yaml-schema.md` の「職務経歴書」セクションを参照。

**Round 1**: 作成日 (`date`)

**Round 2**: 職務要約 + ハイライト

- `AskUserQuestion` で以下を同時に聞く:
  - 職務要約 (`summary`) - これまでの経歴の概要
  - ハイライト (`highlights`) - 主な実績・強みを箇条書き

**Round 3**: 職務経歴 (`experience`)

- 会社ごとに聞き取り。WebソースのURL提示があれば活用する
- 会社情報 (company, period, business, capital, revenue, employees, listing, employment_type)
- プロジェクト: 選択された形式（標準/STAR法）に応じた項目を聞く

**Round 4**: 副業・その他経歴 (`side_experience`)

- 該当する場合のみ

**Round 5**: テクニカルスキル (`technical_skills`)

- カテゴリ別 (OS, 言語, DB, FW等)

**Round 6**: 資格 + 自己PR（まとめて聞く）

- 資格 (`qualifications`)
- 自己PR (`self_pr`) - タイトルと本文のペア

### Step 4: YAML 確認・保存

聞き取ったデータの完全なYAMLをコードブロックでユーザーに表示し、`AskUserQuestion` で「保存する」「修正あり」を確認する。

確認後、`.personal/` ディレクトリに保存する:

- 職務経歴書: `.personal/work_history.yaml`
- 履歴書: `.personal/resume.yaml`

### Step 5: PDF 生成・表示

Makefileのターゲットを使ってPDFを生成し、`open` コマンドで表示する。

**職務経歴書 (標準)**:

```bash
make build-wh-standard YAML=.personal/work_history.yaml CRED=.personal/credential.yaml OUTPUT=output/work-history.pdf
```

**職務経歴書 (STAR法)**:

```bash
make build-wh-star YAML=.personal/work_history.yaml CRED=.personal/credential.yaml OUTPUT=output/work-history.pdf
```

**履歴書**:

```bash
make build-resume YAML=.personal/resume.yaml CRED=.personal/credential.yaml OUTPUT=output/resume.pdf
```

生成後、`open output/<file>.pdf` でPDFビューアを開く。

### Step 6: 確認・修正ループ

PDF表示後、ユーザーのフィードバックに応じて対応する:

- **問題なし** → 完了
- **YAMLデータの修正** → `.personal/` のYAMLを編集して再生成
- **credential.yaml の修正** → ユーザーが直接編集後、再生成コマンドのみ実行
- **レイアウト・表示の問題** → `src/jp_tenshoku_docs_builder/resume/builder.py` 等のビルダーコードを修正して再生成

## ファイル構成

```text
.personal/
  credential.yaml    # 個人情報（手動編集、対話で聞き取り禁止）
  work_history.yaml  # 職務経歴書データ（スキルで生成）
  resume.yaml        # 履歴書データ（スキルで生成）
output/
  work-history.pdf   # 生成された職務経歴書PDF
  resume.pdf         # 生成された履歴書PDF
```

## リファレンス

- YAMLスキーマ詳細: `references/yaml-schema.md`
- サンプルデータ: `sample/` ディレクトリ
- Pydanticモデル: `src/jp_tenshoku_docs_builder/work_history/models.py`, `src/jp_tenshoku_docs_builder/resume/models.py`
