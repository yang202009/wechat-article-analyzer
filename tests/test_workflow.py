#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""端到端测试工作流"""
import json
import os
import sys
import io

# 设置UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_data_integrity(output_dir):
    """测试数据完整性"""
    print(f"\n=== 测试目录: {output_dir} ===\n")

    # 1. 检查scores.json
    scores_file = os.path.join(output_dir, 'scores.json')
    if not os.path.exists(scores_file):
        print("X scores.json不存在")
        return False

    with open(scores_file, 'r', encoding='utf-8') as f:
        scores = json.load(f)

    print(f"OK 找到 {len(scores)} 条评分记录\n")

    # 2. 逐一验证每条记录
    errors = []
    for i, score in enumerate(scores):
        meta_file = os.path.join(output_dir, f'meta_{i}.json')

        if not os.path.exists(meta_file):
            errors.append(f"记录{i}: meta_{i}.json不存在")
            continue

        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)

        # 验证标题匹配（忽略引号编码差异）
        title_norm = score.get('title', '').replace('"', '').replace('"', '').replace('"', '')
        meta_norm = meta.get('title', '').replace('"', '').replace('"', '').replace('"', '')
        if title_norm != meta_norm:
            errors.append(f"记录{i}: 标题不匹配\n  scores: {score.get('title')}\n  meta: {meta.get('title')}")

        # 验证URL匹配
        if score.get('url') != meta.get('url'):
            errors.append(f"记录{i}: URL不匹配")

        # 验证必需字段
        if not score.get('summary') or len(score.get('summary', '')) < 10:
            errors.append(f"记录{i}: 摘要缺失或过短")

        if not score.get('reasoning'):
            errors.append(f"记录{i}: 缺少评分理由")

    # 3. 输出结果
    if errors:
        print(f"X 发现 {len(errors)} 个错误:\n")
        for err in errors[:10]:
            print(f"  {err}\n")
        return False

    print(f"OK 所有 {len(scores)} 条记录验证通过")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_workflow.py <output_dir>")
        sys.exit(1)

    success = test_data_integrity(sys.argv[1])
    sys.exit(0 if success else 1)
