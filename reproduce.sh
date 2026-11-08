#!/usr/bin/env bash
# Reproduce the translated-cycler result for 1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---.
# needs: python3, gcc. Runs in sim/.
#   bash reproduce.sh check     # only re-check the stored restart tapes (seconds)
#   bash reproduce.sh direct    # compare the accelerated simulator with direct simulation up to 5e10 steps (~3 min)
#   bash reproduce.sh full      # simulate up to the third restart and check the cycle (about 30-60 min)
set -euo pipefail
cd "$(dirname "$0")/sim"
gcc -O3 -o at48 at48.c
gcc -O3 -o step48 step48.c
case "${1:-check}" in
  check)
    python3 tccheck.py ../data/tc_restarts.pkl ;;
  direct)
    BS48=40 python3 chk48.py 5e10 80 ;;
  full)
    rm -f restarts.pkl
    TCDUMP=restarts.pkl BS48=40 python3 -u phase48m.py 2.67445e28 | grep -v '^ANCHOR' | tee phases.txt
    python3 tccheck.py restarts.pkl ;;
esac
