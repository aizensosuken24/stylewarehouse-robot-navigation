#!/usr/bin/env bash
set -euo pipefail

GITLAB_URL="${GITLAB_URL:-https://code.swecha.org}"
RUNNER_NAME="${RUNNER_NAME:-smart-robo-nav-docker-runner}"
RUNNER_EXECUTOR="${RUNNER_EXECUTOR:-docker}"
RUNNER_IMAGE="${RUNNER_IMAGE:-python:3.11-slim}"
RUNNER_TOKEN="${GITLAB_RUNNER_TOKEN:-}"
TEMPLATE_PATH="${TEMPLATE_PATH:-.gitlab/runner/config.template.toml}"

if [[ -z "$RUNNER_TOKEN" ]]; then
  echo "GITLAB_RUNNER_TOKEN is required." >&2
  exit 1
fi

gitlab-runner register \
  --non-interactive \
  --url "$GITLAB_URL" \
  --token "$RUNNER_TOKEN" \
  --template-config "$TEMPLATE_PATH" \
  --description "$RUNNER_NAME" \
  --executor "$RUNNER_EXECUTOR" \
  --docker-image "$RUNNER_IMAGE"
