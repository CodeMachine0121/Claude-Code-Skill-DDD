# Strategic Design 輸出文件模板

## 目錄結構

```
ddd-docs/
├── README.md
├── ubiquitous-language.md
└── contexts/
    └── {context-name}/
        ├── overview.md
        └── aggregates/
            └── {aggregate}.md
```

---

## README.md

```markdown
# {專案名稱}

## 專案概述
{專案描述}

## 業務背景
{業務背景}

## 核心問題
- {問題1}

## Bounded Contexts
- [{Context名稱}](contexts/{context-slug}/overview.md)

## 文件結構
{目錄樹}
```

---

## ubiquitous-language.md

```markdown
# 通用語言 (Ubiquitous Language)

| 術語 | 定義 | 所屬 Context |
|------|------|--------------|
| {術語} | {定義} | {Context} |
```

---

## contexts/{context-name}/overview.md

```markdown
# {Context 名稱}

## 概述
{Context 描述}

## 類型
Core Domain / Supporting / Generic

## Aggregates
- [{Aggregate名稱}](aggregates/{aggregate-slug}.md)

## 與其他 Contexts 的關係
| Context | 關係類型 | 說明 |
|---------|----------|------|
| {Context} | Customer-Supplier / Shared Kernel / ACL | {說明} |
```

---

## contexts/{context-name}/aggregates/{aggregate}.md

```markdown
# {Aggregate 名稱}

## 概述
{描述}

## 業務規則 (Invariants)
- {規則1}

## 聚合根: {Entity 名稱}
- **識別欄位**: `{identifier}`
- **屬性**: {屬性列表}

### Value Objects
- **{VO名稱}**: {描述}
  - 屬性: {屬性列表}

## 其他 Entities
### {Entity 名稱}
- **識別欄位**: `{identifier}`
- **屬性**: {屬性列表}
```
