#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""端到端测试 - 10篇文章验证"""
import json
import os
import sys
from pathlib import Path

def run_test():
    """运行小规模测试"""
    print("=== 端到端测试开始 ===\n")

    # 1. 检查测试目录
    test_dir = Path("wechat_test_10")
    if not test_dir.exists():
        print("错误: 测试目录不存在，请先运行fetch_articles.py")
        return False

    # 2. 验证文件数量
    meta_files = list(test_dir.glob("meta_*.json"))
    article_files = list(test_dir.glob("article_*.txt"))

    print(f"找到 {len(meta_files)} 个meta文件")
    print(f"找到 {len(article_files)} 个article文件\n")

    if len(meta_files) != len(article_files):
        print("错误: meta和article文件数量不匹配")
        return False

    # 3. 检查scores.json
    scores_file = test_dir / "scores.json"
    if not scores_file.exists():
        print("错误: scores.json不存在")
        return False

    with open(scores_file, 'r', encoding='utf-8') as f:
        scores = json.load(f)

    print(f"scores.json包含 {len(scores)} 条记录\n")

    # 4. 逐条验证数据一致性
    errors = []
    for i, score in enumerate(scores):
        meta_file = test_dir / f"meta_{i}.json"
        if not meta_file.exists():
            errors.append(f"记录{i}: meta_{i}.json缺失")
            continue

        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)

        # 验证关键字段
        if score['title'] != meta['title']:
            errors.append(f"记录{i}: 标题不匹配")
        if score['url'] != meta['url']:
            errors.append(f"记录{i}: URL不匹配")
        if not score.get('summary') or len(score['summary']) < 20:
            errors.append(f"记录{i}: 摘要过短")
        if not score.get('reasoning'):
            errors.append(f"记录{i}: 缺少评分理由")

    # 5. 输出结果
    if errors:
        print(f"发现 {len(errors)} 个错误:")
        for err in errors:
            print(f"  - {err}")
        return False

    print(f"所有 {len(scores)} 条记录验证通过")
    return True

if __name__ == '__main__':
    success = run_test()
    sys.exit(0 if success else 1)
