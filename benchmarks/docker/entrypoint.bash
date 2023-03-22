#!/bin/bash

echo "setting up paths"
mkdir -p "$JMETER_WORKDIR"

echo "starting benchmarks"
python3 "$ROOT_DIR/benchmarks/benchmark.py"  \
    -r "$ROOT_DIR"                           \
    -d "$JMETER_WORKDIR"                      \
    -j "$JMETER"                              \
    -p "$PORT"                               \
    -a "$ADDRESS"                            \
    --postgres "$POSTGRES_URL"               \
    --postgres-schema "$POSTGRES_SCHEMA"     \
    -n "$API"                                \
    -c "$CSV"                                \
    -k "$LOOPS"                              \
    -t "$JOBS"                               \
    --call-style "$CALL_STYLE"               \
    $@; true

echo "generating JUNIT report"
$M2U --input "$JMETER_WORKDIR/raw_jmeter_report.xml" --output "$JMETER_WORKDIR/report.junit"; true
echo "generated output to: $JMETER_WORKDIR/report.junit"

if [ -n "${eSERVE_PORT}" ]; then
    echo "serving output from benchmarks on http://0.0.0.0:$SERVE_PORT"
    python3 "$WOOF" -i 0.0.0.0 -p "$SERVE_PORT" -Z -c 1 $JMETER_WORKDIR
fi
