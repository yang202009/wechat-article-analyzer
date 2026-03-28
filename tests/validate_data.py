#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数据验证脚本 - 确保评分数据完整性"""
import json
import os
import sys

def validate_scores(output_dir):
    """验证scores.json数据完整性"""
    scores_file = os.path.join(output_dir, 'scores.json')

    if not os.path.exists(scores_file):
        print("❌ scores.json不存在")
        return False

    with open(scores_file, 'r', encoding='utf-8') as f:
        scores = json.load(f)

    errors = []

    for i, item in enumerate(scores):
        # 检查必需字段
        required = ['title', 'url', 'score', 'reasoning', 'summary']
        for field in required:
            if field not in item or not item[field]:
                errors.append(f"文章{i}: 缺少{field}")

        # 检查评分范围
        if 'score' in item and not (0 <= item['score'] <= 10):
            errors.append(f"文章{i}: 评分{item['score']}超出范围")

        # 检查标题和摘要是否匹配
        if 'title' in item and 'summary' in item:
            if len(item['summary']) < 10:
                errors.append(f"文章{i}: 摘要过短")

    if errors:
        print(f"❌ 发现{len(errors)}个错误:")
        for err in errors[:10]:
            print(f"  - {err}")
        return False

    print(f"✅ 验证通过: {len(scores)}篇文章")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_data.py <output_dir>")
        sys.exit(1)

    success = validate_scores(sys.argv[1])
    sys.exit(0 if success else 1)
