"""Recompute review additions from existing independently validated raw data."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json
from pathlib import Path
from src.refinements import enrich


if __name__=='__main__':
    path=Path(__file__).resolve().parent/'output'/'data'/'results.json'
    data=json.loads(path.read_text(encoding='utf8'))
    if not data.get('optional34_complete'): raise RuntimeError('Finish optional 3/4 first')
    enrich(data)
    temporary=path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')
    temporary.replace(path)
    print('Review analysis computed; total checks:',len(data['checks']))
