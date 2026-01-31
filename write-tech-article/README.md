# Write Tech Article Skill

这个 skill 能够从已经爬取的网页内容（技术文章、HN 讨论等）生成结构化的中文技术博客文章，输出自然流畅、没有 AI 味的专业内容。

## 功能特点

- 🎯 按照预定义结构生成完整文章
- ✍️ 输出自然的中文写作，避免 AI 风格
- 🔧 支持自定义配置（输出路径、分类等）
- 📊 包含技术深度分析和代码示例
- 🔗 自动生成元数据和标签

## 使用方法

### 基本用法

```
帮我把 文件1.md的内容 整理成文章
```

### 多个文件

```
帮我把 文件1.md 和 文件2.md的内容 整理成文章
```

### 自定义输出位置

首次使用时，skill 会提示你配置 PREFERENCE.md 文件，设置：
- 输出目录
- 默认分类
- 作者信息等

## 生成的文章结构

1. **YAML Frontmatter**: 标题、日期、标签、分类等元数据
2. **文章摘要**: 3-5 句话概括核心内容
3. **背景与问题**: 建立上下文和问题陈述
4. **核心内容解析**: 
   - 核心观点提取
   - 技术深度分析
   - 实践应用场景
5. **深度分析与思考**:
   - 文章价值与意义
   - 对读者的实际应用价值
   - 个人观点与思考
6. **技术栈/工具清单**: 相关技术和工具列表
7. **相关资源**: 延伸阅读链接

## 文件结构

```
write-tech-article/
├── SKILL.md                        # 主技能文档（AI 加载）
├── PREFERENCE.md                   # 用户配置（可自定义）
├── PREFERENCE_TEMPLATE.md          # 配置模板
├── references/                     # 参考文档（按需加载）
│   ├── ARTICLE_STRUCTURE.md       # 文章结构详细说明
│   └── WRITING_STYLE.md           # 写作风格指南
└── README.md                       # 本文件（仅供人类阅读）
```

## 配置示例

编辑 `PREFERENCE.md`:

```markdown
# Write Tech Article Preferences

- **output_directory**: ~/blog/content/posts
- **default_category**: tech-insights
- **author**: Your Name
- **language**: zh-CN
- **tags_auto_generate**: true
- **max_tags**: 8
```

## 写作风格要点

这个 skill 特别注重**自然的中文写作**，避免常见的 AI 风格问题：

### ❌ 避免
- "让我们一起探索..."
- "值得注意的是..."
- "在...的背景下"
- "随着...的不断发展"

### ✅ 提倡
- 直接、清晰的陈述
- 具体的例子和数据
- 多样化的句式
- 对话式的语气

详见 [references/WRITING_STYLE.md](references/WRITING_STYLE.md)

## 依赖

这个 skill 需要：
- 文件系统写入权限

## 示例输出

参考 [/home/robin/sources/skills/post-to-blogs/Sample.md](../post-to-blogs/Sample.md) 查看生成的文章样例。

## 故障排除

### 找不到 PREFERENCE.md
首次使用时会自动提示创建。

### 生成的文章太短
检查源内容是否足够丰富，必要时手动补充更多背景信息。

### 文章有 AI 味
这是质量控制的重点。如果发现这个问题，请参考 WRITING_STYLE.md 的指导原则，并重新生成。

## 许可证

参见根目录 LICENSE 文件。
