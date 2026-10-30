# Automated contributions

This directory configures the automated development platform that contributes to this
repository. This note says which branches it uses here and how its work reaches the
project's main line.

## Branches

- `aidev/integration` — the integration branch. Automated work lands here and nowhere else.
- `master` — the project's main line; reached from `aidev/integration` only by merge request
  (`aidev handoff`). Merge integration MRs **keeping the source branch**
  (`aidev/integration` is protected, so GitLab never deletes it).
- `ai/*` — one branch per task, created and deleted by the platform. Do not commit to them.
- `session/*` — a session's accumulated work, landed on the integration branch as a batch.

## How work reaches the main line

Task and session branches never reach `aidev/integration` through merge requests; the platform
lands them after its own verification. `aidev/integration` reaches `master` by this project's
usual process, merge requests included — the platform never merges into any other branch.

Whether this project's CI pipelines skip `ai/*` and `session/*` branches is decided by the
project's CI rules (today `.gitlab-ci.yaml` has one manual job, `Trigger any benchmark`, so a push creates a pipeline whose only job waits to be started by hand).

## Suites run before work lands

Declared in `.aidev/project.yaml` under `verification`, all through `.aidev/run-checks.sh`,
which writes `test-results/<slot>/junit.xml` (one case per step):

- `quick`, `full`, `canary`, `system` — `compile import package cli`
- `baseline`, `coverage` — `compile import`
- `static` — `compile`

**This repository has no test suite that can run here.** It holds API test data and tools (`validate_response`, `benchmarks`, `testbase.py`, `jsonsocket.py`, the hivemind reference scripts) that other projects' CI runs against a live hived/hivemind node. So the slots bind to build and static checks only:

- `compile` — `python -m py_compile` over every `.py` file;
- `import` — imports `validate_response`, `benchmarks` and `jsonsocket` with `poetry.lock`'s dependencies. `testbase.py` is left out: it imports `jsondiff`, which `pyproject.toml` does not declare;
- `package` — builds the wheel with the `poetry-core` backend, without an index, and checks it carries `validate_response` and `benchmarks`;
- `cli` — `benchmarks/benchmark.py --help` and `--list` (needs no node).

The set takes a few seconds. There is no linter configuration and no coverage tool, so `static` is `compile` and `coverage` measures nothing (it repeats `baseline`). A change to the API tests' behaviour is only exercised by the consuming projects' pipelines (hivemind and others).

### Not run

- Every API test and reference comparison: needs a live hived/hivemind node.
- CI's only job, the manual `Trigger any benchmark` (JMeter in the `benchmark_aio` service against `BENCHMARK_ADDRESS`).

`test-results/` is not in `.gitignore`; do not commit it.

## Test runtime

`.aidev/runtime/Dockerfile` builds on `python:3.14` (`pyproject.toml` requires `>=3.14`), pinned by digest, and installs every package `poetry.lock` pins into the system interpreter with the Poetry version `pyproject.toml` requires (Poetry itself is removed afterwards), plus the `poetry-core` build backend. Rebuild and re-pin with `.aidev/runtime/build.sh --push` when `pyproject.toml` or `poetry.lock` changes (`environment.inputs`), and put the printed `repo@sha256:…` into `environment.image`.
