#!/usr/bin/env python3
import os
import glob
import sys
from pathlib import Path

output_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
output_path = Path(output_dir)

files_to_remove = (
    list(output_path.glob('article_*.txt')) +
    list(output_path.glob('meta_*.json')) +
    [output_path / 'scores.json']
)

for f in files_to_remove:
    if f.exists():
        f.unlink()
        print(f"Removed: {f.name}")

print("Cleanup complete")
