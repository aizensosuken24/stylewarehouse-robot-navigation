# GitLab Runner Setup

This project's GitLab pipeline expects a runner tagged:

`smart-robo-nav`

The pipeline uses Docker executor images such as:

- `python:3.11-slim`
- `node:20-alpine`
- `alpine:3.20`
- `curlimages/curl:8.8.0`

## 1. Create the runner in GitLab

In your GitLab project:

`Settings -> CI/CD -> Runners -> New project runner`

Use these settings:

- Tags: `smart-robo-nav`
- Run untagged jobs: `disabled`
- Locked to current project: `enabled`

Copy the runner authentication token. Current GitLab tokens usually begin with:

`glrt-`

GitLab recommends runner authentication tokens over legacy registration tokens. See the official docs:

- GitLab docs: [Registering runners](https://docs.gitlab.com/runner/register/)

## 2. Install prerequisites on the runner host

- Docker
- GitLab Runner

## 3. Register the runner

### Windows PowerShell

```powershell
$env:GITLAB_RUNNER_TOKEN="glrt-REPLACE_ME"
.\.gitlab\runner\register-runner.ps1
```

### Linux/macOS shell

```bash
export GITLAB_RUNNER_TOKEN="glrt-REPLACE_ME"
bash .gitlab/runner/register-runner.sh
```

## 4. Start the runner service

After registration, make sure the GitLab Runner service is started on the host.

## 5. Optional deploy hooks

If you want the `deploy` stage to trigger hosting from GitLab, add these CI/CD variables in GitLab:

- `RENDER_DEPLOY_HOOK_URL`
- `VERCEL_DEPLOY_HOOK_URL`

Both deploy jobs are manual and only appear on `main` when the corresponding variable exists.
