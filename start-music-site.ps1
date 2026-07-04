param(
  [int]$Port = 8765
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$nodeCommand = Get-Command node -ErrorAction SilentlyContinue

if ($nodeCommand) {
  $nodePath = $nodeCommand.Source
} else {
  $codexNodePath = Join-Path $HOME ".cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
  if (Test-Path $codexNodePath) {
    $nodePath = $codexNodePath
  } else {
    throw "Node.js was not found. Install Node.js or run this from Codex Desktop with its bundled runtime available."
  }
}

$env:PORT = [string]$Port

Write-Host "Starting Linger Music Memory at http://127.0.0.1:$Port/"
Write-Host "Press Ctrl+C to stop."

& $nodePath (Join-Path $projectRoot "server.js")
