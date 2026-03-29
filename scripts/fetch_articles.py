#!/usr/bin/env python3
import json
import requests
import argparse
import os
import time
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

API_URL = os.getenv("WECHAT_API_URL", "https://www.dajiala.com/fbmain/monitor/v3/kw_search")
API_KEY = os.getenv("WECHAT_API_KEY", "")

if not API_KEY:
    print("Error: WECHAT_API_KEY not found in .env file", file=sys.stderr)
    sys.exit(1)
CACHE_DIR = Path(".wechat_cache")

def fetch_articles(keyword, period=30, pages=1, output_dir="."):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"{keyword}_{period}_{int(time.time()//3600)}.json"
    
    if cache_file.exists():
        print(f"Using cached results: {cache_file}")
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    all_articles = []
    for page in range(1, pages + 1):
        payload = {
            "kw": keyword,
            "sort_type": 1,
            "mode": 3,
            "period": period,
            "page": page,
            "key": API_KEY,
            "any_kw": "",
            "ex_kw": ""
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            articles = data.get('data', [])
            all_articles.extend(articles)
            print(f"Fetched page {page}: {len(articles)} articles")
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}", file=sys.stderr)
            continue
    
    for i, article in enumerate(all_articles):
        content = article.get('content', '')[:1500]
        with open(output_path / f'article_{i}.txt', 'w', encoding='utf-8') as f:
            f.write(content)

        meta = {
            'title': article['title'],
            'url': article['url'],
            'wx_name': article['wx_name'],
            'read': article.get('read', 0),
            'praise': article.get('praise', 0),
            'publish_time': article['publish_time']
        }
        with open(output_path / f'meta_{i}.json', 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False)
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False)
    
    return all_articles

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', required=True)
    parser.add_argument('--period', type=int, default=30)
    parser.add_argument('--pages', type=int, default=1)
    parser.add_argument('--output_dir', default='.')
    args = parser.parse_args()

    articles = fetch_articles(args.keyword, args.period, args.pages, args.output_dir)
    print(f"Total: {len(articles)} articles")
