# DDD Skills

一套 Claude Code skills，透過對話式問答引導您完成 Domain-Driven Design 專案設計。包含兩個專業 skills：

- **strategic-design** - DDD 戰略設計專家，引導完成 Bounded Context 識別與 Aggregate 切分
- **event-storming** - Event Storming 引導專家，帶領完成 Event Storming 工作坊

## 安裝

使用 `uvx` 安裝：

```bash
# 互動式選擇（會提示選擇全域或本地）
uvx --from Claude-Code-Skill-DDD ddd-skill install

# 安裝到全域 (~/.claude/skills/)，所有專案皆可使用
uvx --from Claude-Code-Skill-DDD ddd-skill install -g

# 安裝到當前專案 (./.claude/skills/)，僅限此專案使用
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

安裝後，在 Claude Code 中可以使用以下兩個 skills：

### DDD 戰略設計

```
/strategic-design
```

引導流程：
1. **領域探索** - 了解業務背景與核心問題
2. **Bounded Context 識別** - 劃分子領域邊界
3. **Aggregate 設計** - 定義聚合根與業務規則
4. **Entity / Value Object** - 設計實體與值物件
5. **通用語言** - 建立領域術語表

### Event Storming 工作坊

```
/event-storming
```

引導流程：
1. **選擇業務流程** - 確定要探索的核心業務流程
2. **事件風暴** - 列出所有 Domain Events
3. **時間線排序** - 將事件按時間順序排列
4. **追溯原因** - 識別 Commands 與 Actors
5. **識別 Aggregates** - 找出處理 Commands 的聚合
6. **外部系統與 Read Models** - 識別系統邊界與查詢需求
7. **Hotspots 討論** - 標記待解決的問題

## 輸出

### DDD 戰略設計輸出

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

### Event Storming 輸出

完成工作坊後，生成以下文件結構：

```
ddd-docs/
└── event-storming/
    ├── README.md              # Event Storming 總覽
    └── flows/
        └── {flow-name}.md     # 各業務流程的結果
```

## 專案結構

```
ddd-agent/
├── pyproject.toml
├── README.md
├── LICENSE
├── .github/
└── src/
    └── ddd_skill/
        ├── __init__.py
        ├── cli.py
        └── skills/
            ├── strategic-design/
            │   └── SKILL.md
            └── event-storming/
                └── SKILL.md
```
