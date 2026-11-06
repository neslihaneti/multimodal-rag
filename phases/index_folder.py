"""Index one folder from the command line with timing, e.g. python3 phases/index_folder.py data/index_queue/doc2"""
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env"))

import db
from indexer import index_folder

db.create_tables()
start = time.time()
summary = index_folder(sys.argv[1], lambda message, fraction: print(f"{time.time() - start:7.0f}s {fraction:5.1%} {message}", flush=True))
print(f"DONE in {(time.time() - start) / 60:.1f} min: {summary}", flush=True)
