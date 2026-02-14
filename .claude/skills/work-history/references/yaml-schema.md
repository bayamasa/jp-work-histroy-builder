# 職務経歴書 YAML スキーマリファレンス

フィールド定義とテンプレート例。Pydanticモデル定義に準拠。

---

## 共通事項

### `abbreviate_env` の使い方

同一会社内で複数プロジェクトの開発環境が同じ場合、最初のプロジェクト以外に `abbreviate_env: true` を付けると、PDF上で「同環境のため省略」と表示される。

```yaml
projects:
  - name: "プロジェクトA"
    environment:          # ← こちらに環境詳細を記載（基準）
      languages: ["Java"]
      frameworks: ["Spring Boot"]
  - name: "プロジェクトB"
    abbreviate_env: true  # ← 「同環境のため省略」と表示
    environment:
      languages: ["Java"]
      frameworks: ["Spring Boot"]
```

---

## 標準形式

ファイル: `.personal/work_history.yaml`
モデル: `StandardWorkHistory` (`src/jp_tenshoku_docs_builder/work_history/models.py`)

### トップレベル

STAR法形式と共通。下記「STAR法形式 > トップレベル」を参照。

### StandardCompany

STAR法形式の StarCompany と同一構造。`projects` の型のみ異なる。

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `projects` | list[StandardProject] | No | プロジェクト一覧 |

その他のフィールドは StarCompany と共通。

### StandardProject

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `period` | str | Yes | 期間 (例: "2022年4月～現在") |
| `industry` | str | No | 業界 (例: "保険業界") |
| `name` | str | Yes | プロジェクト名 |
| `overview` | str | No | プロジェクト概要 |
| `phases` | str | No | 担当フェーズ (例: "要件定義、基本設計、詳細設計、実装") |
| `responsibilities` | list[str] | No | 業務内容 (箇条書き) |
| `achievements` | list[str] | No | 実績・取り組み (箇条書き) |
| `environment` | Environment | No | 開発環境 |
| `abbreviate_env` | bool | No | `true` にすると開発環境欄に「同環境のため省略」と表示 |
| `team_size` | str | No | チーム規模 (例: "全15名") |
| `role` | str | No | 役割 (例: "リーダー") |

### 標準形式テンプレート

```yaml
date: "2025年1月1日現在"

summary: |
  ここに職務要約を記載。

highlights:
  - "主な実績・強み1"

experience:
  - company: "株式会社○○"
    period: "20xx年xx月～現在"
    business: "事業内容"
    employment_type: "正社員として勤務"
    projects:
      - period: "20xx年xx月～現在"
        industry: "業界名"
        name: "プロジェクト名"
        overview: |
          プロジェクトの概要。
        phases: "要件定義、基本設計、詳細設計、実装、テスト"
        responsibilities:
          - "業務内容1"
          - "業務内容2"
        achievements:
          - "実績1"
        environment:
          languages: ["Java"]
          frameworks: ["Spring Boot"]
          db: ["Oracle"]
          aws: ["EC2", "S3"]
          tools: ["Git", "Jenkins"]
        team_size: "全15名"
        role: "リーダー"
      - period: "20xx年xx月～20xx年xx月"
        name: "2つ目のプロジェクト"
        abbreviate_env: true
        overview: |
          同じ環境で別のプロジェクト。
        environment:
          languages: ["Java"]
          frameworks: ["Spring Boot"]
        team_size: "全10名"
        role: "メンバー"
```

---

## STAR法形式

ファイル: `.personal/work_history.yaml`
モデル: `StarWorkHistory` (`src/jp_tenshoku_docs_builder/work_history/models.py`)

### トップレベル

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `date` | str | Yes | 作成日 (例: "2025年1月1日現在") |
| `summary` | str | No | 職務要約 |
| `highlights` | list[str] | No | 主な実績・強みの箇条書き |
| `experience` | list[StarCompany] | No | 職務経歴 (会社単位) |
| `side_experience` | list[SideCompany] | No | 副業・その他経歴 |
| `technical_skills` | list[SkillCategory] | No | テクニカルスキル |
| `qualifications` | list[Qualification] | No | 資格 |
| `self_pr` | list[SelfPRSection] | No | 自己PR |

**注意**: `name` フィールドはモデル上存在するが、credential.yaml から自動マージされるため、work_history.yaml には記載不要。

### StarCompany

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `company` | str | Yes | 会社名 |
| `period` | str | Yes | 在籍期間 (例: "2020年4月～現在") |
| `business` | str | No | 事業内容 |
| `capital` | str | No | 資本金 |
| `revenue` | str | No | 売上高 |
| `employees` | str | No | 従業員数 |
| `listing` | str | No | 上場区分 (例: "東証プライム", "未上場") |
| `employment_type` | str | No | 雇用形態 (例: "正社員として勤務") |
| `projects` | list[StarProject] | No | プロジェクト一覧 |

### StarProject

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `period` | str | Yes | 期間 (例: "2022年4月～現在") |
| `industry` | str | No | 業界 (例: "保険業界") |
| `name` | str | Yes | プロジェクト名 |
| `situation` | str | Yes | **Situation** - 状況・背景 |
| `task` | str | Yes | **Task** - 課題・目標 |
| `action` | list[str] | Yes | **Action** - 具体的な行動 (箇条書き) |
| `result` | list[str] | Yes | **Result** - 成果・結果 (箇条書き) |
| `environment` | Environment | No | 開発環境 |
| `abbreviate_env` | bool | No | `true` にすると開発環境欄に「同環境のため省略」と表示。同一会社内で前のプロジェクトと環境が同じ場合に使用 |
| `team_size` | str | No | チーム規模 (例: "全15名") |
| `role` | str | No | 役割 (例: "リーダー") |

### Environment

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `languages` | list[str] | No | プログラミング言語 |
| `os` | list[str] | No | OS |
| `db` | list[str] | No | データベース |
| `frameworks` | list[str] | No | フレームワーク |
| `aws` | list[str] | No | AWSサービス |
| `azure` | list[str] | No | Azureサービス |
| `gcp` | list[str] | No | GCPサービス |
| `tools` | list[str] | No | ツール |
| `other` | list[str] | No | その他 |

### SideCompany

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `company` | str | Yes | 会社名/屋号 |
| `period` | str | Yes | 期間 |
| `employment_type` | str | No | 雇用形態 |
| `projects` | list[SideProject] | No | プロジェクト一覧 |

### SideProject

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `period` | str | Yes | 期間 |
| `name` | str | Yes | プロジェクト名 |
| `description` | str | No | 説明 |
| `environment` | Environment | No | 開発環境 |
| `abbreviate_env` | bool | No | `true` にすると開発環境欄に「同環境のため省略」と表示 |
| `team_size` | str | No | チーム規模 |
| `role` | str | No | 役割 |

### SkillCategory

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `category` | str | Yes | カテゴリ名 (例: "OS", "言語", "DB", "FW") |
| `items` | list[SkillItem] | Yes | スキル項目一覧 |

### SkillItem

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `name` | str | Yes | スキル名 |
| `period` | str | No | 経験期間 (例: "5年0カ月") |
| `level` | str | No | スキルレベル (例: "環境設計・構築が可能") |

### Qualification

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `name` | str | Yes | 資格名 |
| `date` | str | No | 取得日 (例: "2020年6月取得") |

### SelfPRSection

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `title` | str | Yes | PRタイトル |
| `content` | str | Yes | PR本文 |

### テンプレート

```yaml
date: "2025年1月1日現在"

summary: |
  ここに職務要約を記載。これまでの経歴の概要を3-5行程度で。

highlights:
  - "主な実績・強み1"
  - "主な実績・強み2"
  - "主な実績・強み3"

experience:
  - company: "株式会社○○"
    period: "20xx年xx月～現在"
    business: "事業内容"
    capital: ""
    revenue: ""
    employees: ""
    listing: ""
    employment_type: "正社員として勤務"
    projects:
      - period: "20xx年xx月～現在"
        industry: "業界名"
        name: "プロジェクト名"
        situation: |
          どのような状況・背景があったか。
        task: |
          何を達成する必要があったか。
        action:
          - "具体的に行った行動1"
          - "具体的に行った行動2"
        result:
          - "得られた成果・結果1"
          - "得られた成果・結果2"
        environment:
          languages: ["Python", "TypeScript"]
          os: ["Linux"]
          db: ["PostgreSQL"]
          frameworks: ["FastAPI", "React"]
          aws: ["ECS", "S3", "RDS"]
          tools: ["Docker", "GitHub Actions"]
        team_size: "全5名"
        role: "リーダー"

side_experience:
  - company: "フリーランス"
    period: "20xx年xx月～現在"
    employment_type: "業務委託"
    projects:
      - period: "20xx年xx月～現在"
        name: "プロジェクト名"
        description: |
          プロジェクトの説明。
        environment:
          languages: ["TypeScript"]
          frameworks: ["Next.js"]
        team_size: "1名"
        role: "個人開発"

technical_skills:
  - category: "OS"
    items:
      - name: "Linux"
        period: "5年0カ月"
        level: "環境設計・構築が可能"
  - category: "言語"
    items:
      - name: "Python"
        period: "3年0カ月"
        level: "最適なコード記述が可能"
  - category: "DB"
    items:
      - name: "PostgreSQL"
        period: "3年0カ月"
        level: "環境設計・構築が可能"
  - category: "FW"
    items:
      - name: "FastAPI"
        period: "2年0カ月"
        level: "実務での開発経験あり"

qualifications:
  - name: "普通自動車第一種運転免許"
    date: "20xx年xx月取得"
  - name: "基本情報技術者試験"
    date: "20xx年xx月合格"

self_pr:
  - title: "PRのタイトル"
    content: |
      自己PRの本文をここに記載。
      具体的なエピソードを交えて記載する。
```
