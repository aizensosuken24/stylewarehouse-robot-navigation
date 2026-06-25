param(
  [string]$GitLabUrl = "https://code.swecha.org",
  [string]$RunnerName = "smart-robo-nav-docker-runner",
  [string]$RunnerExecutor = "docker",
  [string]$RunnerImage = "python:3.11-slim",
  [string]$TemplatePath = ".gitlab/runner/config.template.toml",
  [string]$RunnerToken = $env:GITLAB_RUNNER_TOKEN
)

if ([string]::IsNullOrWhiteSpace($RunnerToken)) {
  throw "GITLAB_RUNNER_TOKEN is required."
}

gitlab-runner register `
  --non-interactive `
  --url $GitLabUrl `
  --token $RunnerToken `
  --template-config $TemplatePath `
  --description $RunnerName `
  --executor $RunnerExecutor `
  --docker-image $RunnerImage
