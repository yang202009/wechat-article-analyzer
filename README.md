# WeChat Article Analyzer

AI驱动的微信公众号文章分析工具 - 商业级质量保证

## ✨ 功能特性

- 🔍 **智能搜索** - 多关键词搜索，自动去重
- 🤖 **AI分析** - Claude直接分析，生成评分和摘要
- 📊 **双维评分** - 实战场景 + 技术前沿（0-10分）
- 📝 **高质量摘要** - 2-3句核心内容总结
- 📄 **多格式报告** - HTML/Markdown/JSON
- ✅ **数据验证** - 完整性验证机制
- 💾 **智能缓存** - 1小时缓存提升效率

## 🚀 快速开始

### 1. 获取 API Key

访问 [大家啦](https://www.dajiala.com/) 注册账号并获取 API Key。

大家啦是一个提供公众号API和视频号API的第三方平台，通过该平台可以获取微信公众号文章数据。

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的 API Key：

```bash
cp .env.example .env
# 编辑 .env 文件，设置 WECHAT_API_KEY=你的密钥
```

### 3. 使用

在Claude Code中直接使用：

```
帮我查下"AI Agent"相关的微信公众号文章
```

## 📋 参数说明

## 📋 参数说明

- `keyword`: 搜索关键词（必需）
- `period`: 时间范围（7/15/30/60/90天，默认30）
- `pages`: 抓取页数（1-5，默认1，每页20篇）
- `threshold`: 最低评分（0-10，默认6）
- `format`: 输出格式（html/markdown/json，默认html）
- `sort_by`: 排序方式（score/read/praise/time，默认score）
- `weights`: 评分权重（"实战:技术"，默认"5:5"）

## 📊 评分标准

### 实战场景（0-5分）
- **5分**：详细实现方案，包含代码/架构
- **3分**：一般场景描述
- **1分**：仅提及用例
- **0分**：无实战内容

### 技术前沿（0-5分）
- **5分**：前沿技术（2025-2026）
- **3分**：近期实践（2023-2024）
- **1分**：成熟技术
- **0分**：过时内容

**相关性检查**：分析前验证文章是否匹配关键词，不相关文章评0分。

## 📦 输出示例

```
✅ 分析完成！
- 关键词：AI Agent
- 时间范围：30天
- 抓取文章：20篇
- 符合标准：8篇
- 输出目录：./wechat_analysis_20260328_120000/
- 报告文件：./wechat_analysis_20260328_120000/wechat_report.html
```

## ✅ 测试验证

已通过完整测试：
- ✅ 3篇文章小规模测试
- ✅ 10篇文章中等规模测试
- ✅ 数据完整性验证100%通过
- ✅ 成功识别不相关文章

## 🔧 技术架构

### 项目结构
```
wechat-article-analyzer/
├── scripts/           # 核心脚本
│   ├── fetch_articles.py      # 文章抓取（支持缓存）
│   ├── generate_report.py     # 报告生成
│   └── cleanup.py             # 临时文件清理
├── tests/             # 测试脚本（可选）
│   ├── validate_data.py       # 数据完整性验证
│   ├── test_workflow.py       # 工作流测试
│   └── e2e_test.py            # 端到端测试
├── skill.md           # Claude Code skill 定义
├── .env.example       # 环境变量模板
└── .gitignore         # Git 忽略规则
```

### 工作流程
```
1. fetch_articles.py → 抓取文章，保存为 article_*.txt + meta_*.json
2. Claude 直接分析 → 读取文件，生成 scores.json（AI评分+摘要）
3. generate_report.py → 根据 scores.json 生成 HTML/Markdown/JSON 报告
4. cleanup.py → 删除临时文件
```

## 📝 版本历史

### v1.1 (2026-03-28) - 商业级质量
- ✅ 修复数据错位问题
- ✅ 添加完整验证机制
- ✅ 优化引号字符处理
- ✅ 通过10篇文章测试

### v1.0
- 初始版本

## 📄 许可证

MIT License
