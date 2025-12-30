# CLAUDE.md - tests_api Repository

## Project Overview

API test suite for Hive blockchain nodes. Tests both **hived** (core blockchain node) and **hivemind** (social layer) APIs. The repository maintains a flat test structure allowing different CI processes to run tests independently. Includes comprehensive benchmarking tools for API performance testing.

## Tech Stack

- **Language:** Python 3.12+
- **Package Manager:** Poetry
- **Testing Frameworks:**
  - Tavern - YAML-based REST API testing (pytest-compatible)
  - PyRestTest - REST API testing
  - pytest - Test runner with parallel execution
  - CMake - Test orchestration (ApiTests.cmake)
- **Benchmarking:** Apache JMeter, custom Python benchmark script
- **Key Dependencies:**
  - `requests` (2.32.3) - HTTP client
  - `deepdiff` (6.3.0) - Deep object comparison
  - `prettytable` (3.8.0) - Table formatting

## Directory Structure

```
tests_api/
├── benchmarks/              # API performance benchmarking
│   ├── benchmark.py         # Main benchmark script
│   ├── performance_data/    # JMeter test data and CSVs
│   │   ├── account_history_api/
│   │   ├── blocks_api/
│   │   └── universal/
│   ├── Dockerfile.jmeter
│   └── setup_jmeter.bash
├── hivemind/                # Hivemind API tests
│   ├── reference/           # Reference comparison tests
│   │   ├── block_api/
│   │   ├── bridge/
│   │   ├── condenser_api/
│   │   ├── database_api/
│   │   ├── follow_api/
│   │   └── tags_api/
│   ├── tavern/              # Tavern YAML tests
│   └── api_error_smoketest.py
├── validate_response/       # Response validation library
│   └── __init__.py          # Pattern comparison functions
├── testbase.py              # Base class for JSON comparison
├── jsonsocket.py            # JSON-RPC socket communication
├── ApiTests.cmake           # CMake test configuration
├── pyproject.toml           # Poetry configuration
└── .gitlab-ci.yaml          # CI/CD configuration
```

## Development Commands

### Setup
```bash
poetry install
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Running Tavern Tests
```bash
# Set target node
export HIVEMIND_ADDRESS=127.0.0.1
export HIVEMIND_PORT=8080

# Run all tests with parallel execution
pytest --workers auto --tests-per-worker auto .

# Run specific directory
pytest --workers auto --tests-per-worker auto hivemind/tavern/

# Run full sync tests
./scripts/run_tests_full_sync.sh URL PORT
```

### Running Benchmarks
```bash
# List available CSV files
./benchmarks/benchmark.py -l

# Benchmark blocks_api on local node
./benchmarks/benchmark.py -n blocks_api -p 8090 -c perf_5M_light.csv

# Benchmark on remote machine
./benchmarks/benchmark.py -n blocks_api -p 8090 -c perf_5M_light.csv -a hive-6.pl.syncad.com
```

### Formatting
```bash
poetry run black .
```

## Key Files

| File | Purpose |
|------|---------|
| `validate_response/__init__.py` | Core pattern comparison and validation functions |
| `testbase.py` | `SimpleJsonTest` base class for node comparison tests |
| `jsonsocket.py` | JSON-RPC HTTP/HTTPS communication with retry logic |
| `benchmarks/benchmark.py` | Performance benchmarking tool with JMeter integration |
| `ApiTests.cmake` | CMake macros for test registration |
| `.gitlab-ci.yaml` | CI benchmark stage configuration |

## Coding Conventions

### Python Patterns
- Shebang: `#!/usr/bin/env python3` for executables
- Type hints (Python 3.12+ syntax)
- Logging via `logging` module
- Path handling via `pathlib.Path`

### Test Patterns
- **Reference comparison:** Test node output vs reference node output
- **Pattern files:** Expected responses stored as `.pat.json`
- **Output files:** Actual responses saved as `.out.json`
- **Ignore tags:** Predefined sets for dynamic fields (timestamps, IDs, etc.)
- **TAVERN_DIR:** Environment variable for test directory context

### Benchmark CSV Naming
Format: `<mode>_<blocks>M_<tag1>_<tag2>.csv`
- Modes: `perf` (performance), `cl` (constant load)
- Blocks: `5M`, `60M`
- Tags: `light`, `heavy`, `prod`, `psql`, `jrpc`, `custom`

### Validation Functions
Key functions in `validate_response/__init__.py`:
- `compare_response_with_pattern()` - Main pattern comparison
- `compare_rest_response_with_pattern()` - REST API comparison
- `has_valid_response()` - Response format validation
- Predefined ignore tags: `BRIDGE_POSTS_IGNORE_TAGS`, `CONDENSER_POSTS_IGNORE_TAGS`, etc.

## CI/CD Notes

### GitLab CI (.gitlab-ci.yaml)
- Single stage: `benchmark` (manual trigger only)
- Docker image: `registry.gitlab.syncad.com/hive/tests_api/benchmark_aio:latest`
- Environment variables:
  - `BENCHMARK_ADDRESS` - Target node address
  - `BENCHMARK_PORT` - Target node port
  - `eJOBS` - Number of parallel jobs
  - `eLOOPS` - Number of test loops

### Running in CI
Pipeline is manual-trigger only. Configure via CI/CD variables before running.

## Connection Retry Logic

Both `jsonsocket.py` and `benchmark.py` implement retry logic:
- Default: 10 attempts with 5-second delay
- Handles transient connection failures
- Critical for reliable CI execution
