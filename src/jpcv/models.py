"""Pydantic models for 職務経歴書 data."""

from __future__ import annotations

from pydantic import BaseModel


class Environment(BaseModel):
    """開発環境."""

    languages: list[str] = []
    os: list[str] = []
    db: list[str] = []
    frameworks: list[str] = []
    tools: list[str] = []
    other: list[str] = []


class Project(BaseModel):
    """プロジェクト."""

    period: str
    industry: str = ""
    name: str
    overview: str = ""
    phases: str = ""
    responsibilities: list[str] = []
    achievements: list[str] = []
    environment: Environment = Environment()
    team_size: str = ""
    role: str = ""


class Company(BaseModel):
    """会社経歴."""

    company: str
    period: str
    business: str = ""
    capital: str = ""
    revenue: str = ""
    employees: str = ""
    listing: str = ""
    employment_type: str = ""
    projects: list[Project] = []


class SkillItem(BaseModel):
    """スキル項目."""

    name: str
    period: str = ""
    level: str = ""


class SkillCategory(BaseModel):
    """スキルカテゴリ."""

    category: str
    items: list[SkillItem]


class Qualification(BaseModel):
    """資格."""

    name: str
    date: str = ""


class SelfPRSection(BaseModel):
    """自己PRセクション."""

    title: str
    content: str


class WorkHistory(BaseModel):
    """職務経歴書全体."""

    date: str
    name: str
    summary: str = ""
    highlights: list[str] = []
    experience: list[Company] = []
    technical_skills: list[SkillCategory] = []
    qualifications: list[Qualification] = []
    self_pr: list[SelfPRSection] = []
