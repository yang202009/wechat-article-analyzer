#!/usr/bin/env python3
import json
import argparse
from datetime import datetime
from pathlib import Path

def generate_html(articles, keyword, threshold):
    qualified = [a for a in articles if a['score'] >= threshold]
    qualified.sort(key=lambda x: x.get('sort_key', x['score']), reverse=True)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>微信文章分析报告 - {keyword}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }}
.container {{ max-width: 1200px; margin: 0 auto; }}
.header {{ background: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
.article-card {{ background: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); transition: transform 0.3s; }}
.article-card:hover {{ transform: translateY(-5px); }}
.score {{ display: inline-block; padding: 8px 16px; border-radius: 20px; font-weight: bold; font-size: 18px; }}
.score-high {{ background: #10b981; color: white; }}
.score-medium {{ background: #f59e0b; color: white; }}
.summary {{ color: #555; font-size: 14px; line-height: 1.6; margin-top: 10px; padding: 10px; background: #f9fafb; border-radius: 8px; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>🦞 微信文章分析报告</h1>
<p>关键词：{keyword} | 符合标准：{len(qualified)}篇</p>
</div>
'''
    
    for a in qualified:
        score_class = 'score-high' if a['score'] >= 8 else 'score-medium'
        pub_time = datetime.fromtimestamp(a['publish_time']).strftime('%Y-%m-%d')
        summary = a.get('summary', '')
        
        html += f'''
<div class="article-card">
<div class="score {score_class}">评分: {a['score']}/10</div>
<div style="font-size:20px;font-weight:bold;margin:10px 0">
<a href="{a['url']}" target="_blank" style="color:#333;text-decoration:none">{a['title']}</a>
</div>
<div style="color:#666;font-size:14px;margin:10px 0">
📱 {a['wx_name']} | 👁 {a['read']:,} | 👍 {a['praise']} | 📅 {pub_time}
</div>
<div style="color:#666;font-size:14px">{a['reasoning']}</div>
{f'<div class="summary">📝 {summary}</div>' if summary else ''}
</div>
'''
    
    html += '</div></body></html>'
    return html

def generate_markdown(articles, keyword, threshold):
    qualified = [a for a in articles if a['score'] >= threshold]
    qualified.sort(key=lambda x: x.get('sort_key', x['score']), reverse=True)
    
    md = f"# 微信文章分析报告\n\n**关键词**: {keyword}  \n**符合标准**: {len(qualified)}篇\n\n---\n\n"
    
    for a in qualified:
        pub_time = datetime.fromtimestamp(a['publish_time']).strftime('%Y-%m-%d')
        md += f"## [{a['title']}]({a['url']})\n\n"
        md += f"**评分**: {a['score']}/10  \n"
        md += f"**公众号**: {a['wx_name']} | 阅读: {a['read']:,} | 点赞: {a['praise']} | 日期: {pub_time}\n\n"
        md += f"**评价**: {a['reasoning']}\n\n"
        if a.get('summary'):
            md += f"**摘要**: {a['summary']}\n\n"
        md += "---\n\n"
    
    return md

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', default='html', choices=['html', 'markdown', 'json'])
    parser.add_argument('--threshold', type=int, default=6)
    parser.add_argument('--sort_by', default='score', choices=['score', 'read', 'praise', 'time'])
    parser.add_argument('--keyword', default='搜索结果')
    parser.add_argument('--output_dir', default='.')
    args = parser.parse_args()

    output_path = Path(args.output_dir)
    with open(output_path / 'scores.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)

    sort_keys = {'score': 'score', 'read': 'read', 'praise': 'praise', 'time': 'publish_time'}
    for a in articles:
        a['sort_key'] = a.get(sort_keys[args.sort_by], 0)

    if args.format == 'html':
        content = generate_html(articles, args.keyword, args.threshold)
        (output_path / 'wechat_report.html').write_text(content, encoding='utf-8')
    elif args.format == 'markdown':
        content = generate_markdown(articles, args.keyword, args.threshold)
        (output_path / 'wechat_report.md').write_text(content, encoding='utf-8')
    else:
        qualified = [a for a in articles if a['score'] >= args.threshold]
        (output_path / 'wechat_report.json').write_text(json.dumps(qualified, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"Report generated: wechat_report.{args.format}")
