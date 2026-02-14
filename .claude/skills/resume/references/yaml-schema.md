# 履歴書 YAML スキーマリファレンス

フィールド定義とテンプレート例。Pydanticモデル定義に準拠。

---

ファイル: `.personal/resume.yaml`
モデル: `Resume` (`src/jp_tenshoku_docs_builder/resume/models.py`)

**注意**: 履歴書モデルには `name`, `name_kana`, `birth_day` 等の個人情報フィールドが定義されているが、これらは credential.yaml から自動マージされる。resume.yaml には記載不要。

### フィールド定義

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `date` | str | Yes | 作成日 (例: "2025年1月1日現在") |
| `education` | list[HistoryEntry] | No | 学歴 |
| `experience` | list[HistoryEntry] | No | 職歴 |
| `licences` | list[HistoryEntry] | No | 免許・資格 |
| `commuting_time` | str | No | 通勤時間 (例: "1時間10分") |
| `dependents` | str | No | 扶養家族数 (例: "0人") |
| `spouse` | str | No | 配偶者の有無 (例: "有" / "無") |
| `supporting_spouse` | str | No | 配偶者の扶養義務 (例: "有" / "無") |
| `hobby` | str | No | 趣味・特技 |
| `motivation` | str | No | 志望動機 |
| `request` | str | No | 本人希望記入欄 |

### HistoryEntry

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `year` | str | No | 年 (例: "2020") |
| `month` | str | No | 月 (例: "4") |
| `value` | str | Yes | 内容 (例: "○○大学 工学部 入学") |

**注意**: 年月が不要な行（例: 「現在に至る」や部署配属の補足行）は `year` と `month` を空文字列にする。

### テンプレート

```yaml
date: "2025年1月1日現在"

# 学歴
education:
  - year: "20xx"
    month: "4"
    value: "○○高等学校 入学"
  - year: "20xx"
    month: "3"
    value: "○○高等学校 卒業"
  - year: "20xx"
    month: "4"
    value: "○○大学 ○○学部 ○○学科 入学"
  - year: "20xx"
    month: "3"
    value: "○○大学 ○○学部 ○○学科 卒業"

# 職歴
experience:
  - year: "20xx"
    month: "4"
    value: "株式会社○○ 入社"
  - year: ""
    month: ""
    value: "○○部に配属、○○業務に従事"
  - year: ""
    month: ""
    value: "現在に至る"

# 免許・資格
licences:
  - year: "20xx"
    month: "xx"
    value: "普通自動車第一種運転免許"
  - year: "20xx"
    month: "xx"
    value: "基本情報技術者試験 合格"

# 通勤時間
commuting_time: "1時間10分"

# 扶養家族数(配偶者を除く)
dependents: "0人"

# 配偶者の有無
spouse: "無"

# 配偶者の扶養義務
supporting_spouse: "無"

# 趣味・特技
hobby: |
  趣味・特技を記載。

# 志望動機
motivation: |
  志望動機を記載。

# 本人希望記入欄
request: |
  勤務地や入社時期等の希望を記載。
```
