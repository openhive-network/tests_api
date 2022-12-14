#!/bin/bash

echo "setting up paths"
mkdir -p "$JMETER_WORKDIR"

echo "starting benchmarks"
python3 "$eROOT_DIR/benchmarks/benchmark.py"  \
    -r "$eROOT_DIR"                           \
    -d "$JMETER_WORKDIR"                      \
    -j "$JMETER"                              \
    -p "$ePORT"                               \
    -a "$eADDRESS"                            \
    --postgres "$ePOSTGRES_URL"               \
    --postgres-schema "$ePOSTGRES_SCHEMA"     \
    -n "$eAPI"                                \
    -c "$eCSV"                                \
    -k "$eLOOPS"                              \
    -t "$eJOBS"                               \
    --call-style "$eCALL_STYLE"               \
    $@; true

echo "generating JUNIT report"
$M2U --input "$JMETER_WORKDIR/raw_jmeter_report.xml" --output "$JMETER_WORKDIR/report.junit"; true
echo "generated output to: $JMETER_WORKDIR/report.junit"

if [ -n "${eSERVE_PORT}" ]; then
    echo "serving output from benchmarks on http://0.0.0.0:$eSERVE_PORT"
    python3 "$WOOF" -i 0.0.0.0 -p "$eSERVE_PORT" -Z -c 1 wdir
fi
