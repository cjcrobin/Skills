# Writing Style Guide - Natural Chinese Without AI Flavor

This guide provides concrete examples of natural vs. AI-style writing to help generate articles that read like human writing.

## Core Principles

### 1. Direct Communication
Start with the point, not buildup. Readers are busy.

❌ **AI Style**:
> 在深入探讨这个话题之前，我们首先需要理解其背景。在当今快速发展的技术环境中，云计算已经成为企业数字化转型的重要基石。那么，让我们来看看...

✅ **Natural Style**:
> AWS 刚推出的新定价模型会让中小企业的云成本降低 40%。但有个隐藏的坑：流量费用没变。

### 2. Concrete Before Abstract
Show, don't just tell.

❌ **AI Style**:
> 性能优化是一个复杂的过程，需要考虑多个维度和因素，包括但不限于系统架构、代码质量、以及资源配置等方面。

✅ **Natural Style**:
> 把这段代码从 2 秒优化到 200 毫秒，我们做了三件事：缓存查询结果、批量处理请求、升级到 Redis 6。

### 3. Varied Rhythm
Mix short and long sentences. Avoid repetitive patterns.

❌ **AI Style**:
> 这个功能很重要。这个特性很有用。这个方法很高效。这个设计很合理。

✅ **Natural Style**:
> 这个功能解决了实际问题。不仅如此，它的实现方式也很优雅——只用了 50 行代码，却比原来快了 10 倍。

## Common AI Phrases to Avoid

### Opening Clichés

| ❌ Avoid | ✅ Use Instead |
|---------|---------------|
| 在当今快速发展的... | [直接说主题] |
| 随着...的不断发展 | [直接说现状] |
| 众所周知... | [给出具体事实] |
| 让我们一起探索... | [直接进入主题] |
| 值得注意的是... | [直接说重点] |

### Transition Overuse

| ❌ Avoid | ✅ Use Instead |
|---------|---------------|
| 首先...其次...再次...最后... | 用数字或直接叙述 |
| 与此同时... | 同时/另一方面 (少用) |
| 综上所述... | 所以/总结来说 |
| 不难发现... | [直接说发现] |

### Hedging Words

| ❌ Overused | ✅ More Confident |
|------------|-------------------|
| 可能会... | 会/能 (确定时) |
| 在某种程度上... | [具体程度] |
| 相对来说... | [给出对比] |
| 基本上... | [删除或具体化] |

## Good Examples from Technical Writing

### Example 1: Problem Statement

❌ **AI Style**:
> 在现代软件开发过程中，我们经常会遇到各种各样的挑战。其中一个值得关注的问题是，当我们的应用规模不断扩大时，性能问题就会逐渐显现出来。这个问题如果不能得到及时的解决，将会严重影响用户体验。

✅ **Natural Style**:
> 你的网站从 1000 个用户涨到 10 万，响应时间从 100ms 飙到了 3 秒。用户在流失，老板在催。这时候你需要的不是重写代码，而是这三个针对性的优化策略。

### Example 2: Technical Explanation

❌ **AI Style**:
> 这个算法的工作原理相对复杂，需要我们从多个角度来理解。简单来说，它主要通过一系列的步骤来实现目标。首先，系统会进行数据的预处理。然后，会执行核心的计算逻辑。最后，输出处理后的结果。

✅ **Natural Style**:
> 这个算法分三步：先清洗脏数据（去掉重复和异常值），再用哈希表快速查找匹配项，最后按权重排序输出。整个过程时间复杂度是 O(n)，比暴力搜索快 100 倍。

### Example 3: Introducing Code

❌ **AI Style**:
> 下面让我们通过一个代码示例来更好地理解这个概念。这段代码展示了如何实现我们前面讨论的功能。请仔细阅读代码中的注释，它们会帮助你更好地理解每一步的作用。

✅ **Natural Style**:
> 看代码更直接：

```python
# 批量查询用户数据，避免 N+1 问题
users = User.objects.select_related('profile').filter(active=True)

# 用 prefetch_related 预加载关联对象
users = users.prefetch_related('orders__items')
```

> 两行代码，查询次数从 1000+ 降到 3 次。

### Example 4: Analysis

❌ **AI Style**:
> 通过对这个技术的深入分析，我们可以发现它具有多方面的优势。首先，它在性能方面表现优异。其次，它的可维护性也很好。此外，它还具有良好的扩展性。当然，我们也需要注意到，它也存在一些局限性，需要在实际使用中加以注意。

✅ **Natural Style**:
> 这个技术有三个明显优势：比 REST 快 2 倍、代码量减少 30%、自动生成 TypeScript 类型。但它也有代价——学习曲线陡，生态工具少，团队可能需要两周适应期。值不值得切换，取决于你的项目规模。

## Sentence Pattern Variety

### Pattern 1: Simple Statement
> Redis 7 增加了函数功能。

### Pattern 2: Compound Sentence
> Redis 7 增加了函数功能，但还不支持 TypeScript。

### Pattern 3: Question + Answer
> 为什么选 PostgreSQL 而不是 MySQL？三个字：JSON 支持。

### Pattern 4: Contrast
> SQLite 适合原型开发。到了生产环境？换成 PostgreSQL。

### Pattern 5: Numeric Emphasis
> 三个配置参数，性能提升 10 倍。

### Pattern 6: Metaphor/Analogy
> GraphQL 就像点菜，你要什么服务器就给什么。REST 是套餐，给你一堆可能不需要的东西。

## Paragraph Structure

### Good Paragraph Example

> **Topic sentence**: Vercel 的 Edge Functions 解决了冷启动问题。
> 
> **Elaboration**: 传统 Lambda 函数第一次调用可能需要 2-3 秒初始化，Edge Functions 始终保持在 50ms 以内。
> 
> **Evidence**: 我们测试了 1000 次冷启动，平均响应时间 38ms。
> 
> **Implication**: 这意味着你的 API 可以部署在全球 100+ 个节点，用户体验不会有任何波动。

### Bad Paragraph Example

> Edge Functions 是一个非常有趣的技术。它在很多方面都表现出色。首先，它的性能很好。其次，它的部署很简单。此外，它的可扩展性也很强。总的来说，这是一个值得考虑的技术方案。

## Technical Term Handling

### Rule 1: English in Parentheses
First mention of ambiguous terms:

> Vercel 使用边缘函数（Edge Functions）处理请求，而不是传统的服务器端渲染（SSR）。

### Rule 2: Don't Over-Explain Basics
If target audience is developers:

❌ "JavaScript 是一种编程语言，主要用于 Web 开发..."
✅ "用 TypeScript 代替 JavaScript"

### Rule 3: Use Code for Precision

Instead of: "使用 async 关键字可以让函数异步执行"
Better: "在函数前加 `async` 就能用 `await`"

## Tone Examples

### Informative (Facts-First)

> PostgreSQL 15 的 MERGE 命令相比 15 之前的版本快了 3 倍。测试环境：100 万行表，50% 更新 50% 插入，单核 CPU。

### Conversational (Engaging)

> 你可能没注意到，PostgreSQL 15 悄悄加了个 MERGE 命令。这玩意儿有多快？我们跑了个测试：100 万行数据，一半更新一半插入，比原来快 3 倍。

### Critical/Analytical (Balanced)

> PostgreSQL 15 的 MERGE 命令性能提升明显，但代价是语法复杂度。对于简单场景，INSERT...ON CONFLICT 仍然是更好的选择。只有在需要同时处理更新、插入、删除时，MERGE 的优势才能体现。

### Instructional (How-To)

> 三步开启 PostgreSQL MERGE：
> 1. 升级到 15+
> 2. 把 INSERT...ON CONFLICT 改成 MERGE INTO
> 3. 加上 WHEN NOT MATCHED 子句
> 
> 完成。性能提升不用改业务逻辑。

## Common Mistakes

### Mistake 1: Over-Qualification
❌ "这个方法在大多数情况下通常能够解决问题"
✅ "这个方法能解决问题" 或 "这个方法适用于 80% 的场景"

### Mistake 2: Passive Voice Overuse
❌ "这个bug被发现于上周，并且已经被修复了"
✅ "我们上周发现并修复了这个bug"

### Mistake 3: Nominalizations
❌ "进行代码的优化" (optimization of code)
✅ "优化代码" (optimize code)

### Mistake 4: Redundant Pairs
❌ "各种各样的", "不同类型的", "多种多样的"
✅ Just use "多个", "不同", or be specific

### Mistake 5: Filler Phrases
❌ "实际上", "事实上", "基本上", "总体而言"
✅ Delete them or replace with specific data

## Self-Editing Checklist

Before finalizing any article, check:

- [ ] First paragraph grabs attention with specifics
- [ ] No "让我们" or "值得注意的是"
- [ ] Sentence length varies (mix 5-30 characters)
- [ ] Each paragraph has one clear point
- [ ] Technical terms are precise
- [ ] Code examples have context
- [ ] Numbers and data replace vague claims
- [ ] No hedging unless genuinely uncertain
- [ ] Active voice dominates
- [ ] Reads naturally when spoken aloud

## Read-Aloud Test

The final test: Read the article aloud. If it sounds like:
- A presentation ❌
- A textbook ❌
- A conversation with a knowledgeable colleague ✅

Then you've nailed the natural style.
