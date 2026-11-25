#!/bin/bash
# Phase 11: persona, style and stereotype runs of one split, then the stereotype judge and the fairness report.
#   OUT=<dir> CODE=<dir> nohup caffeinate -is phases/phase-11/run_split.sh dev|holdout > <log> 2>&1 &
# OUT (default phases/phase-11/reports) gets the reports; CODE (default this repository) is where evaluate.py runs,
# e.g. a git worktree of the Phase 9 code for the holdout baseline. Rerunnable: finished steps are skipped.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
SPLIT=${1:?usage: run_split.sh dev|holdout}
OUT=${OUT:-$ROOT/phases/phase-11/reports}
CODE=${CODE:-$ROOT}
mkdir -p "$OUT"
for KIND in persona style stereotype; do
  "$HERE/run_eval.sh" "$ROOT/eval/fairness/${SPLIT}_${KIND}.jsonl" "${SPLIT}_${KIND}" "$OUT" "$CODE" || exit 1
done
export FAIRNESS_REPORTS=$OUT
if [ ! -f "$OUT/${SPLIT}_stereotype-labels.jsonl" ]; then
  echo "$(date '+%F %T') stereotype judge ($CODE)"
  python3 -u "$ROOT/eval/fairness/analyze.py" judge --split "$SPLIT" --code "$CODE" || exit 1
fi
python3 -u "$ROOT/eval/fairness/analyze.py" report --split "$SPLIT"
echo "$(date '+%F %T') done $SPLIT"
