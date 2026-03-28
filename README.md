# WeChat Article Analyzer

AI驱动的微信公众号文章分析工具

## ✨ 功能特性

- 🔍 **智能搜索** - 多关键词搜索，自动去重
- 🤖 **AI分析** - Claude直接分析，生成评分和摘要
- 📊 **双维评分** - 实战场景 + 技术前沿（0-10分）
- 📝 **高质量摘要** - 2-3句核心内容总结
- 📄 **多格式报告** - HTML/Markdown/JSON
- ✅ **数据验证** - 完整性验证机制
- 💾 **智能缓存** - 1小时缓存提升效率

## 🚀 快速开始

### 0. 安装依赖

```bash
cd ~/.claude/skills/wechat-article-analyzer
pip install -r requirements.txt
```

### 1. 安装 Skill

**方法一：通过 GitHub 安装**

在 Claude Code 中运行：

```bash
git clone https://github.com/yang202009/wechat-article-analyzer.git ~/.claude/skills/wechat-article-analyzer
```

**方法二：手动安装**

1. 下载本仓库
2. 将整个文件夹复制到 `~/.claude/skills/wechat-article-analyzer`
3. 重启 Claude Code

安装后，在 Claude Code 中输入 `/wechat-article-analyzer` 即可看到该 skill。

### 1. 获取 API Key

访问 [极致了数据](https://www.dajiala.com/) 注册账号并获取 API Key。

极致了数据是一个提供公众号API和视频号API的第三方平台，通过该平台可以获取微信公众号文章数据。

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
├── requirements.txt   # Python 依赖
├── .env               # 环境变量配置
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

## 🐛 故障排查

### 问题：ModuleNotFoundError: No module named 'dotenv'
**解决方案**：
```bash
pip install python-dotenv
```

### 问题：WECHAT_API_KEY not found in .env file
**解决方案**：
1. 确认 `.env` 文件存在于 skill 根目录
2. 检查文件内容格式：`WECHAT_API_KEY=your_key_here`
3. 确保没有多余空格

### 问题：API request failed
**解决方案**：
1. 检查网络连接
2. 验证 API Key 是否有效
3. 查看 API 配额是否用尽

### 问题：JSON 格式错误
**解决方案**：
- 已在 v1.2 中修复，更新到最新版本

## 📝 版本历史

### v1.2 (2026-03-28)
- ✅ 添加 python-dotenv 支持
- ✅ 增强错误处理和超时机制
- ✅ API URL 可配置化
- ✅ 添加 requirements.txt
- ✅ 完善故障排查文档

### v1.1 (2026-03-28)
- ✅ 修复数据错位问题
- ✅ 添加完整验证机制
- ✅ 优化引号字符处理
- ✅ 通过10篇文章测试

### v1.0
- 初始版本

## 📄 许可证

MIT License
