# Article Structure Reference

This document defines the standard structure for generated tech blog articles. The structure ensures comprehensive coverage while maintaining natural flow.

## Frontmatter (YAML Metadata)

```yaml
---
title: "Article Title - Clear and Specific"
date: YYYY-MM-DD
tags:
  - "Tag 1"
  - "Tag 2"
  - "Tag 3-5 more relevant tags"
categories:
  - "Primary Category"
draft: false
description: "Concise 50-200 word summary that captures the essence of the article"
slug: "url-friendly-article-identifier"
---
```

## Article Body Structure

### 1. 文章摘要 (Article Summary)

**Purpose**: Provide a standalone overview that readers can understand without reading the full article.

**Content**:
- 3-5 sentence summary (150-250 words)
- Main topic and context
- Key problem or opportunity discussed
- Primary insights or takeaways
- Intended audience or use cases

**Style**: Direct, informative, conversational. Hook the reader without hype.

### 2. 背景与问题 (Background and Problem)

**Purpose**: Establish context and articulate the problem being addressed.

**Sections**:
- **Current situation**: What's happening in the field/industry
- **Specific challenge**: The problem, gap, or opportunity
- **Why it matters**: Real-world impact and implications
- **Stakeholders**: Who is affected and how

**Style**: Start broad, narrow to specific. Use concrete examples. Avoid jargon unless explained.

### 3. 核心内容解析 (Core Content Analysis)

**Purpose**: Deep dive into the main subject matter with structured analysis.

**Subsections**:

#### 3.1 核心观点提取 (Core Insights)
- Extract 5-7 key points from the source material
- Each point should be specific and actionable
- Support with evidence or examples
- Number or bullet format for clarity

#### 3.2 技术深度分析 (Technical Deep Dive)
- Architecture or system design (if applicable)
- Implementation details
- Code examples with explanations
- Technical trade-offs and decisions
- Performance considerations

**Code Block Format**:
```language
# Clear comments explaining what the code does
code_example_here()

# Why this approach was chosen
more_code()
```

#### 3.3 实践应用场景 (Practical Applications)
- How to apply the concepts
- Use cases and scenarios
- Step-by-step guides where relevant
- Common pitfalls and how to avoid them

**Style**: Technical but accessible. Explain complex concepts with analogies. Use diagrams/examples.

### 4. 深度分析与思考 (Deep Analysis and Reflection)

**Purpose**: Provide original analysis, critical thinking, and broader implications.

**Subsections**:

#### 4.1 文章价值与意义 (Value and Significance)
- Why this topic is important
- How it advances the field
- Unique contributions or perspectives
- Long-term implications

#### 4.2 对读者的实际应用价值 (Practical Value for Readers)
- Segment by reader persona:
  - Developers/Engineers
  - Technical Leaders/Architects
  - Product Managers/Decision Makers
  - Students/Learners
- Actionable takeaways for each group

#### 4.3 可能的实践场景 (Potential Practice Scenarios)
- Real-world implementation examples
- Case studies or hypothetical scenarios
- Integration with existing workflows
- Scaling considerations

#### 4.4 个人观点与思考 (Personal Perspective)
- Critical analysis (not just summary)
- Alternative viewpoints
- Limitations or concerns
- Future directions
- Open questions

**Style**: Analytical but accessible. Balance optimism with realism. Show independent thinking.

### 5. 技术栈/工具清单 (Tech Stack / Tools List)

**Purpose**: Catalog technologies, tools, and resources mentioned.

**Format by category**:
- **Core Technologies**: Main frameworks, languages, platforms
- **Supporting Tools**: Libraries, utilities, services
- **Development Tools**: IDEs, testing frameworks, CI/CD
- **Monitoring/Operations**: Logging, metrics, deployment
- **Version Information**: Specific versions if critical

**Example**:
```markdown
**Core Framework**:
- Python 3.11+
- FastAPI 0.104.1
- PostgreSQL 15

**Supporting Libraries**:
- pydantic: Data validation
- sqlalchemy: ORM
- alembic: Database migrations

**Development Tools**:
- pytest: Testing framework
- black: Code formatting
- mypy: Type checking
```

### 6. 相关资源与延伸阅读 (Related Resources)

**Purpose**: Provide pathways for further learning and official sources.

**Sections**:
- **Official Documentation**: Primary sources, API docs
- **Original Articles**: Source material with context
- **Community Discussions**: HN, Reddit, forums with specific threads
- **Academic Papers**: Research papers if relevant
- **Video Resources**: Talks, tutorials (with timestamps)
- **Code Examples**: GitHub repos, code samples
- **Alternative Perspectives**: Contrasting views or approaches

**Format**:
```markdown
- [Clear Link Text](URL) - Brief description of what reader will find
```

## Writing Style Guidelines

### Natural Chinese Writing

**Characteristics**:
- Varied sentence structure and length
- Concrete before abstract
- Active voice preferred
- Minimal transition words
- Direct, clear expression

**Avoid**:
- Formulaic AI phrases ("值得注意的是", "让我们", "在...的背景下")
- Excessive hedging ("可能", "也许", "某种程度上")
- Generic openings ("在当今快速发展...")
- Overly formal academic tone

**Good opening example**:
> PostgreSQL 15 引入了一个容易被忽视的特性：MERGE 语句。这个 SQL 标准命令能用一条语句完成之前需要多次往返数据库的操作。但它真的比传统的 INSERT...ON CONFLICT 更快吗？

**Bad opening example**:
> 在当今数据库技术快速发展的背景下，PostgreSQL 作为一款优秀的开源数据库，在其最新版本中引入了诸多令人瞩目的新特性。其中，值得我们关注的是 MERGE 语句的实现。让我们一起深入探讨这个特性的价值和意义。

### Technical Precision

- Use exact technical terms (don't simplify incorrectly)
- Provide English terms in parentheses for ambiguous translations
- Include version numbers for APIs and tools
- Link to official documentation
- Cite sources with inline links

### Code Examples

- Always include context (what problem does this solve?)
- Add comments explaining non-obvious parts
- Show both setup and usage
- Include error handling if relevant
- Use realistic, production-quality code

## Section Length Guidelines

| Section | Typical Length |
|---------|---------------|
| Frontmatter | Fixed format |
| 文章摘要 | 150-250 words |
| 背景与问题 | 500-800 words |
| 核心内容解析 | 1500-2500 words |
| 深度分析与思考 | 1000-1500 words |
| 技术栈/工具清单 | 200-400 words |
| 相关资源 | 10-20 links with descriptions |

**Total article length**: 3500-5500 words typically

## Metadata Guidelines

### Title
- 15-25 characters (Chinese) / 40-70 characters (English)
- Specific, not generic
- Include key technology or concept
- Avoid clickbait or hype

**Good**: "PostgreSQL MERGE 语句性能分析：比 UPSERT 快 3 倍的秘密"
**Bad**: "数据库新特性深度解析：你绝对不能错过的重大更新"

### Tags
- 5-8 tags typically
- Mix of:
  - Technology names (e.g., "PostgreSQL", "Python")
  - Concepts (e.g., "Performance", "Database Design")
  - Audience (e.g., "Backend", "DevOps")
- Use established tags (check existing articles)
- Avoid overly broad tags ("Technology", "Programming")

### Description (slug)
- URL-friendly
- Use hyphens not underscores
- Include main keywords
- 3-8 words
- All lowercase

**Good**: `postgresql-merge-performance-analysis`
**Bad**: `New_Database_Feature_123`

### Category
- Single primary category
- Examples: `database`, `ai-ml`, `devops`, `web-development`
- Match site's existing category taxonomy

## Quality Verification Checklist

Before finalizing, verify:

- [ ] Title is specific and accurate
- [ ] Description summarizes key value
- [ ] All sections are present and complete
- [ ] Code examples are tested and functional
- [ ] No AI-style clichés or formulaic language
- [ ] Technical terms are accurate
- [ ] Sources are properly cited
- [ ] Links are valid and specific
- [ ] Frontmatter is complete and valid YAML
- [ ] Article provides unique insight, not just summary
- [ ] Natural flow between sections
- [ ] Practical value is clear
