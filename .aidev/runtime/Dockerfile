# The image AIDEV runs this project's suites in (`environment.image` in
# .aidev/project.yaml). AIDEV runs it as `docker run --rm --network none --user
# <uid>:<gid> -v <workspace>:/work`, so everything a suite needs is in the image.
#
# Based on python:3.14 (pyproject.toml requires python >=3.14), pinned by
# digest. It adds
#   - Poetry at the version pyproject.toml requires and every package
#     poetry.lock pins, installed into the system interpreter (no venv);
#   - poetry-core, the build backend, so the wheel builds without an index.
#
# .aidev/runtime/build.sh builds it; the result is pinned as `environment.image`.
# See .aidev/README.md.
ARG BASE_IMAGE=python:3.14@sha256:22caa054c0d309b1eee6f448326a8821a674a75b98653247fe706db90491fc87
FROM ${BASE_IMAGE}
ENV HOME=/tmp \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false
COPY deps/ /tmp/deps/
RUN python -m pip install --no-cache-dir "poetry==$(sed -n 's/^requires-poetry *= *"\(.*\)"/\1/p' /tmp/deps/pyproject.toml)" \
        "$(sed -n 's/^requires *= *\["\(poetry-core[^"]*\)"\]/\1/p' /tmp/deps/pyproject.toml)" \
    && cd /tmp/deps && poetry install --no-root --no-interaction \
    && python -m pip uninstall -y poetry \
    && cd / && rm -rf /tmp/deps /tmp/.cache
