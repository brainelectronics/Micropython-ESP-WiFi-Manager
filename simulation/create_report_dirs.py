#!/usr/bin/env python3
"""Create test report directories."""
from pathlib import Path
import os
import shutil

if os.path.exists('reports'):
    shutil.rmtree('reports', ignore_errors=True)

Path('reports/sca').mkdir(parents=True, exist_ok=True)
Path('reports/test_results').mkdir(parents=True, exist_ok=True)
Path('reports/coverage').mkdir(parents=True, exist_ok=True)
