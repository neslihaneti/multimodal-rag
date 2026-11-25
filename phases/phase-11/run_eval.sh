#!/bin/bash
# Retrieval + answers for one golden file, with the memory guard and resume (phases/CHALLENGES.md).
#   phases/phase-11/run_eval.sh <golden.jsonl> <name> <out dir> [code dir]
# The reports are copied to <out dir>/<name>-retrieval.* and <name>-answers.*; a step whose copy exists is skipped.
# [code dir] (default: this repository) is where evaluate.py runs, e.g. a git worktree of an older phase.
set -u
GOLDEN=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
NAME=$2
OUT=$(mkdir -p "$3" && cd "$3" && pwd)
CODE=${4:-$(cd "$(dirname "$0")/../.." && pwd)}
GUARD_GB=${GUARD_GB:-70}
MAX_RESTARTS=${MAX_RESTARTS:-15}
LOGS=$(cd "$(dirname "$0")/../logs" && pwd)
export PYTHONUNBUFFERED=1
cd "$CODE" || exit 1

footprint_gb() { footprint "$1" 2>/dev/null | sed -nE 's/.*Footprint: ([0-9.]+) GB.*/\1/p' | head -1 | cut -d. -f1; }

copy_report() {  # copy the report named on the last "Report:" line of the log
  local stem
  stem=$(grep -E "^Report: " "$1" | tail -1 | sed -E 's/^Report: (.*)\.md$/\1/')
  [ -n "$stem" ] && [ -f "$stem.json" ] || { echo "no report in $1"; return 1; }
  cp "$stem.json" "$OUT/$2.json"; cp "$stem.md" "$OUT/$2.md"
  [ -f "$stem-judgments.jsonl" ] && cp "$stem-judgments.jsonl" "$OUT/$2-judgments.jsonl"
  echo "copied $stem → $OUT/$2"
}

STEP=$NAME-retrieval
if [ ! -f "$OUT/$STEP.json" ]; then
  LOG=$LOGS/phase11-$(basename "$OUT")-$STEP.log
  echo "$(date '+%F %T') retrieval $NAME ($CODE)"
  python3 -u evaluate.py retrieval --golden "$GOLDEN" > "$LOG" 2>&1 || { echo "retrieval failed, see $LOG"; exit 1; }
  copy_report "$LOG" "$STEP" || exit 1
fi

STEP=$NAME-answers
[ -f "$OUT/$STEP.json" ] && exit 0
LOG=$LOGS/phase11-$(basename "$OUT")-$STEP.log
: > "$LOG"
RESUME=""
[ -f reports/answers-partial.jsonl ] && RESUME="--resume"  # reused only if it belongs to the same golden file (hash)
for TRY in $(seq 0 "$MAX_RESTARTS"); do
  echo "$(date '+%F %T') answers $NAME try $TRY $RESUME"
  python3 -u evaluate.py answers --golden "$GOLDEN" $RESUME >> "$LOG" 2>&1 &
  PID=$!
  while kill -0 "$PID" 2>/dev/null; do
    GB=$(footprint_gb "$PID"); GB=${GB:-0}
    if [ "$GB" -ge "$GUARD_GB" ]; then
      echo "$(date '+%F %T') footprint ${GB} GB ≥ ${GUARD_GB} GB → restart" | tee -a "$LOG"
      kill "$PID"; sleep 5; kill -9 "$PID" 2>/dev/null
    fi
    sleep 20
  done
  wait "$PID"
  RESUME="--resume"
  if grep -q "^Report: " "$LOG"; then copy_report "$LOG" "$STEP"; exit $?; fi
  # the same error twice in a row is not a memory problem: stop instead of retrying it
  if [ "$(grep -c '^Traceback' "$LOG")" -ge 2 ]; then echo "answers keep failing, see $LOG"; exit 1; fi
done
echo "gave up after $MAX_RESTARTS restarts"; exit 1
