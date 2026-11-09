#!/usr/bin/env bash
# Check the Rocq proof inside a checkout of busycoq (branch BB6), tested with Coq 8.20.1.
#   bash check.sh /path/to/busycoq
# copies the three files into busycoq/verify, builds the needed busycoq modules and the proof,
# and prints the assumptions of the final theorem (expected: "Closed under the global context").
set -euo pipefail
BC=${1:?path to a busycoq checkout (branch BB6)}
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$BC/verify"
cp "$HERE/RWLAccT.v" "$HERE/RWLAccT62.v" "$HERE/PR_LongTranslatedCycler.v" .
ulimit -s unlimited || true
coq_makefile -Q . BusyCoq -Q ./BigInt BigInt -o Makefile.tc48 $(ls *.v) $(ls BigInt/*.v 2>/dev/null) >/dev/null
make -f Makefile.tc48 RWLAccT62.vo
time coqc -Q . BusyCoq -Q ./BigInt BigInt PR_LongTranslatedCycler.v
printf 'From BusyCoq Require Import PR_LongTranslatedCycler.\nPrint Assumptions nonhalt.\n' > tc48_check.v
coqc -Q . BusyCoq -Q ./BigInt BigInt tc48_check.v
