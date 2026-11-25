#!/bin/bash
# Phase 11 Part 2 (11a + 11b), in order; rerunnable (finished steps are skipped):
#   1. dev fairness sets with the fixed code            → phases/phase-11/reports-11ab/
#   2. the 82-question golden_dev (regression check)     → phases/phase-11/reports-11ab/golden_dev-*
#   3. holdout with the Phase 9 code (git worktree)      → phases/phase-11/reports-holdout-phase9/
#   4. holdout with the fixed code                       → phases/phase-11/reports-holdout-11ab/
#   nohup caffeinate -is phases/phase-11/run_part2.sh > phases/logs/phase11-part2.log 2>&1 &
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
WORKTREE=${WORKTREE:-/Users/neslihaneti/Desktop/rag_phase9_baseline}
OUT=$HERE/reports-11ab "$HERE/run_split.sh" dev || exit 1
"$HERE/run_eval.sh" "$ROOT/eval/golden_dev.jsonl" golden_dev "$HERE/reports-11ab" || exit 1
OUT=$HERE/reports-holdout-phase9 CODE=$WORKTREE "$HERE/run_split.sh" holdout || exit 1
OUT=$HERE/reports-holdout-11ab "$HERE/run_split.sh" holdout || exit 1
echo "$(date '+%F %T') part 2 done"
