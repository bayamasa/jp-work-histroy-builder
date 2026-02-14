# /resume スキル

対話形式で履歴書のYAMLデータを作成し、PDFを生成するスキル。

## トリガー

- 「履歴書を作成」「resume作成」
- `/resume`

## ワークフロー

### Step 1: credential.yaml の確認

`AskUserQuestion` でユーザーに `.personal/credential.yaml` の準備状況を確認する。ファイルの存在チェックは行わない。

**質問: credential.yaml は準備できていますか？**

- **ある** → Step 2 へ進む
- **ない（今作成する）** → 作成手順を案内して **スキルを中断** する
- **あとで作成する** → credential.yaml なしで Step 2 へ進む（PDF生成時にエラーになる旨を伝える）

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

**重要**: credential.yaml には氏名・住所・電話番号等の個人情報が含まれる。セキュリティ上、対話形式での聞き取り、ファイルの読み取り、存在チェックは **絶対に行わない**。ユーザー自身がファイルを直接編集する運用とする。

### Step 2: 対話形式でのデータ聞き取り

`AskUserQuestion` を活用して履歴書YAMLデータの各項目を聞き取る。
各項目の詳細スキーマは `references/yaml-schema.md` を参照。

#### 聞き取りの原則

- **関連項目はまとめて聞く**: `AskUserQuestion` の `questions` パラメータで複数質問を同時に提示し、やり取り回数を減らす
- **スキップを常に選択肢に含める**: 任意項目は「スキップ」オプションを用意する
- **Webソースの活用**: ユーザーがWantedly・LinkedIn等のURLを提示した場合は `WebFetch` で情報を取得し、職歴データとして整理する
- **日付の逆算**: 学歴は最終卒業年と浪人・留学等の年数から高校入学まで逆算できる。ユーザーに全日付を入力させず、最小限の情報から計算する
- **確認を挟む**: 逆算・推定した内容は `AskUserQuestion` でユーザーに確認を取ってから次へ進む
- **既存ファイルの活用**: `.personal/` に既存のYAMLファイルがある場合はそれを読み込み、修正ベースで進める

#### 聞き取りフロー

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

### Step 3: YAML 確認・保存

聞き取ったデータの完全なYAMLをコードブロックでユーザーに表示し、`AskUserQuestion` で「保存する」「修正あり」を確認する。

確認後、`.personal/resume.yaml` に保存する。

### Step 4: PDF 生成・表示

Makefileのターゲットを使ってPDFを生成し、`open` コマンドで表示する。

```bash
make build-resume YAML=.personal/resume.yaml CRED=.personal/credential.yaml OUTPUT=output/resume.pdf
```

生成後、`open output/resume.pdf` でPDFビューアを開く。

### Step 5: 確認・修正ループ

PDF表示後、ユーザーのフィードバックに応じて対応する:

- **問題なし** → 完了
- **YAMLデータの修正** → `.personal/resume.yaml` を編集して再生成
- **credential.yaml の修正** → ユーザーが直接編集後、再生成コマンドのみ実行
- **レイアウト・表示の問題** → `src/jp_tenshoku_docs_builder/resume/builder.py` のビルダーコードを修正して再生成

## ファイル構成

```text
.personal/
  credential.yaml    # 個人情報（手動編集、対話で聞き取り禁止）
  resume.yaml        # 履歴書データ（スキルで生成）
output/
  resume.pdf         # 生成された履歴書PDF
```

## リファレンス

- YAMLスキーマ詳細: `references/yaml-schema.md`
- サンプルデータ: `sample/resume.yaml`
- Pydanticモデル: `src/jp_tenshoku_docs_builder/resume/models.py`
