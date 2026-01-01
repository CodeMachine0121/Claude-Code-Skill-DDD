# DDD Skill

一個 Claude Code skill，透過對話式問答引導您完成 Domain-Driven Design 專案設計。

## 安裝

使用 `uvx` 安裝：

```bash
# 互動式選擇（會提示選擇全域或本地）
uvx --from Claude-Code-Skill-DDD ddd-skill install

# 安裝到全域 (~/.claude/skills/ddd/)，所有專案皆可使用
uvx --from Claude-Code-Skill-DDD ddd-skill install -g

# 安裝到當前專案 (./.claude/skills/ddd/)，僅限此專案使用
uvx --from Claude-Code-Skill-DDD ddd-skill install -l
```

移除：

```bash
# 互動式選擇
uvx --from Claude-Code-Skill-DDD ddd-skill uninstall

# 移除全域安裝
uvx --from Claude-Code-Skill-DDD ddd-skill uninstall -g

# 移除本地安裝
uvx --from Claude-Code-Skill-DDD ddd-skill uninstall -l
```

## 使用方式

安裝後，在 Claude Code 中執行：

```
/ddd
```

## 引導流程

1. **領域探索** - 了解業務背景與核心問題
2. **Bounded Context 識別** - 劃分子領域邊界
3. **Aggregate 設計** - 定義聚合根與業務規則
4. **Entity / Value Object** - 設計實體與值物件
5. **通用語言** - 建立領域術語表

## 輸出

完成問答後，自動生成以下 Markdown 文件結構：

```
ddd-docs/
├── README.md                 # 專案概覽
├── ubiquitous-language.md    # 通用語言術語表
└── contexts/
    └── {context-name}/
        ├── overview.md       # Context 概覽
        └── aggregates/
            └── {aggregate}.md
```

## 專案結構

```
ddd-skill/
├── pyproject.toml
├── README.md
├── .claude/
│   └── skills/
│       └── ddd/
│           └── SKILL.md
└── src/
    └── ddd_skill/
        ├── __init__.py
        └── cli.py
```
