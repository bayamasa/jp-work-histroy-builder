"""Pydantic models for 履歴書 (JIS standard resume) data."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class HistoryEntry(BaseModel):
    """学歴・職歴・資格の1行エントリ."""

    model_config = ConfigDict(extra="forbid")

    year: str = ""
    month: str = ""
    value: str


class Resume(BaseModel):
    """履歴書データモデル (JIS標準フォーマット準拠)."""

    model_config = ConfigDict(extra="forbid")

    # 基本情報（必須）
    date: str
    name_kana: str
    name: str
    birth_day: str

    # 基本情報（任意）
    gender: str = ""
    cell_phone: str = ""
    email: str = ""
    photo: str = ""

    # 現住所
    address_kana: str = ""
    address: str = ""
    address_zip: str = ""
    tel: str = ""
    fax: str = ""

    # 連絡先
    address_kana2: str = ""
    address2: str = ""
    address_zip2: str = ""
    tel2: str = ""
    fax2: str = ""

    # 学歴・職歴・免許資格
    education: list[HistoryEntry] = []
    experience: list[HistoryEntry] = []
    licences: list[HistoryEntry] = []

    # 通勤・扶養
    commuting_time: str = ""
    dependents: str = ""
    spouse: str = ""
    supporting_spouse: str = ""

    # 自由記述
    hobby: str = ""
    motivation: str = ""
    request: str = ""
