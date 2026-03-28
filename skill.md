---
name: wechat-article-analyzer
description: Search WeChat articles by keyword, analyze with AI scoring, generate HTML/Markdown/JSON reports with summaries | 搜索微信公众号文章，AI智能评分分析，生成HTML/Markdown/JSON报告
trigger: Use when user wants to search and analyze WeChat articles
---

# WeChat Article Analyzer

Search WeChat articles, AI-powered content analysis, scored reports with article summaries.

## Workflow

1. **Confirm Parameters** - Suggest related keywords and confirm with user
2. **Fetch Articles** - Run `fetch_articles.py` to get articles from API
   - Supports multiple keywords, auto-deduplication
   - Creates output folder: `./wechat_analysis_{timestamp}/`
   - Saves as `article_*.txt` + `meta_*.json`
3. **AI Analysis** - Claude directly reads files and analyzes each article
   - Relevance check (matches keyword intent)
   - Score (0-10) based on practical scenarios + tech novelty
   - 2-3 sentence summary (not just excerpt)
   - Detailed reasoning
   - Saves to `scores.json`
4. **Generate Report** - Run `generate_report.py` to create HTML/Markdown/JSON
5. **Cleanup** - Run `cleanup.py` to remove temporary files

## Configuration

**API Endpoint**: `https://www.dajiala.com/fbmain/monitor/v3/kw_search`
**API Key**: Set via environment variable `WECHAT_API_KEY`

**User Parameters**:
- `keyword`: Search keyword (required)
- `period`: Time range in days (7/15/30/60/90, default: 30)
- `pages`: Number of pages to fetch (1-5, default: 1, 20 articles per page)
- `threshold`: Minimum score to include (0-10, default: 6)
- `format`: Output format (html/markdown/json, default: html)
- `sort_by`: Sort results by (score/read/praise/time, default: score)
- `weights`: Scoring weights as "practical:tech" (default: "5:5")

**Cache**: Results cached for 1 hour in `.wechat_cache/`

## Scoring Criteria

Rate each article 0-10 based on configurable weights:

**Practical Scenarios (default 5 points)**
- 5: Detailed implementation with code/architecture
- 3: General scenario description
- 1: Only mentions use case
- 0: No practical content

**Latest Tech (default 5 points)**
- 5: Cutting-edge tech (2025-2026)
- 3: Recent practices (2023-2024)
- 1: Established tech
- 0: Outdated content

**Content Relevance Check**: Before scoring, verify article matches keyword intent. If irrelevant, score 0 and mark as "不相关".

## Execution Steps

### Step 1: Suggest Keywords & Confirm Parameters
**IMPORTANT**: Use AskUserQuestion tool with options, NOT plain text.

Analyze user's keyword and suggest 2-3 related terms:
- Variations: "AI Agent" → "AI智能体", "LLM Agent"
- Technical: "大模型Agent", "RAG"
- Domains: "客服Agent", "营销自动化"

Use AskUserQuestion with:
- Question 1: "Which keywords to search?"
  - Option 1: "Original only" (just user's keyword)
  - Option 2: "Multiple keywords (Recommended)" (original + 2-3 suggestions)
  - Option 3: "Custom" (let user specify)
- Question 2: "How many pages per keyword?" (default: 2)
- Question 3: "Output format?" (html/markdown/json, default: html)
- Question 4: "Score threshold?" (default: 6)

### Step 3: Fetch & Merge Articles
For multiple keywords:
1. Fetch from API or cache (`.wechat_cache/{keyword}_{period}_{timestamp}.json`)
2. Merge results and remove duplicates by URL
3. Save to output folder as `article_{i}.txt` + `meta_{i}.json`

### Step 4: AI Analysis (Direct Analysis)
**CRITICAL**: You (Claude) must analyze EACH article individually to ensure data consistency.

**Analysis Process (per article):**
1. Read `meta_{i}.json` to get title, URL, metadata
2. Read `article_{i}.txt` (first 2000 chars) for content
3. Analyze and score:
   - Relevance check: Does content match keyword intent?
   - Practical scenarios (0-5): Implementation details, code, architecture
   - Tech novelty (0-5): Latest tech (2025-2026), cutting-edge
   - Generate 2-3 sentence summary based on ACTUAL content
4. Create score entry with ALL metadata:
```json
{
  "title": "actual article title from meta",
  "url": "actual url from meta",
  "score": 8,
  "reasoning": "实战场景4分：详细案例；技术前沿4分：2026最新",
  "summary": "基于实际内容的摘要...",
  "publish_time": 1234567890,
  "wx_name": "公众号名称",
  "read": 10000,
  "praise": 100
}
```
5. Append to `scores.json` (not overwrite)
6. Show progress: `[5/80] 文章标题... Score: 8`

**Quality Checks:**
- Title in score MUST match title in meta
- Summary MUST describe actual article content
- Score MUST reflect actual analysis
- Process in small batches (5-10) to avoid errors

### Step 5: Generate Report
Run: `python scripts/generate_report.py --format html --threshold 6 --sort_by score --output_dir "..."`

### Step 6: Cleanup
Run: `python scripts/cleanup.py "OUTPUT_DIR"` (removes article_*.txt, meta_*.json)

## Output Format

Tell user:
```
✅ 分析完成！
- 关键词：{keyword}
- 时间范围：{period}天
- 抓取文章：{total}篇
- 符合标准：{qualified}篇
- 输出目录：{output_folder}
- 报告文件：{output_folder}/wechat_report.{format}
```

## Scripts Location

**Core scripts** (in `scripts/`):
- `fetch_articles.py` - Fetch articles from API with caching
- `generate_report.py` - Generate HTML/Markdown/JSON reports
- `cleanup.py` - Clean temporary files

**Test scripts** (in `tests/`, optional):
- `validate_data.py` - Validate data integrity
- `test_workflow.py` - Test workflow
- `e2e_test.py` - End-to-end testing

## Complete Workflow

```
1. fetch_articles.py → 抓取文章，保存为 article_*.txt + meta_*.json
2. Claude 直接分析 → 读取文件，生成 scores.json
3. generate_report.py → 根据 scores.json 生成报告
4. cleanup.py → 删除临时文件
```

## Important Notes

**AI Analysis Method**:
- ✅ Claude directly analyzes articles (recommended, accurate summaries)
- ❌ Do NOT use `analyze_articles.py` (simple keyword matching, poor quality)
- ❌ Do NOT use `ai_analyze_articles.py` (requires external API key)

**Analysis Quality**:
- Direct analysis: Real AI-generated summaries and reasoning
- Script analysis: Just excerpts from article beginning
- Always use direct analysis for best results
