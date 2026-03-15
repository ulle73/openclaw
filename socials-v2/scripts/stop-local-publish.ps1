param(
  [int]$Port = 3000
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$runtimeDir = Join-Path $repoRoot '.runtime'

function Stop-FromPidFile {
  param(
    [Parameter(Mandatory = $true)]
    [string]$PidFilePath
  )

  if (-not (Test-Path $PidFilePath)) {
    return $false
  }

  $pidValue = (Get-Content $PidFilePath -Raw).Trim()
  if (-not $pidValue) {
    return $false
  }

  $process = Get-Process -Id ([int]$pidValue) -ErrorAction SilentlyContinue
  if ($process) {
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
  }

  Remove-Item $PidFilePath -ErrorAction SilentlyContinue
  return [bool]$process
}

function Stop-ProcessesByCommandLine {
  param(
    [Parameter(Mandatory = $true)]
    [string]$ProcessName,
    [Parameter(Mandatory = $true)]
    [scriptblock]$Predicate
  )

  $processes = Get-CimInstance Win32_Process -Filter "Name = '$ProcessName'" -ErrorAction SilentlyContinue
  if (-not $processes) {
    return 0
  }

  $count = 0
  foreach ($process in $processes) {
    $commandLine = [string]$process.CommandLine
    if (& $Predicate $commandLine) {
      Stop-Process -Id $process.ProcessId -Force -ErrorAction SilentlyContinue
      $count += 1
    }
  }

  return $count
}

function Stop-ProcessListeningOnPort {
  param(
    [Parameter(Mandatory = $true)]
    [int]$Port
  )

  $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
    Select-Object -First 1

  if (-not $connection) {
    return $false
  }

  $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
  if (-not $process -or $process.ProcessName -ne 'node') {
    return $false
  }

  Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
  return $true
}

$stopped = @()

if (Stop-FromPidFile -PidFilePath (Join-Path $runtimeDir 'app.pid')) {
  $stopped += 'app'
}

if (Stop-FromPidFile -PidFilePath (Join-Path $runtimeDir 'cloudflared.pid')) {
  $stopped += 'cloudflared'
}

$fallbackAppCount = Stop-ProcessesByCommandLine -ProcessName 'node.exe' -Predicate {
  param($commandLine)
  ($commandLine -match [regex]::Escape($repoRoot)) -and (
    $commandLine -match 'index\.js' -or
    $commandLine -match 'cli\.js\s+serve'
  )
}

if ($fallbackAppCount -gt 0 -and -not ($stopped -contains 'app')) {
  $stopped += 'app'
}

if ((Stop-ProcessListeningOnPort -Port $Port) -and -not ($stopped -contains 'app')) {
  $stopped += 'app'
}

$fallbackTunnelCount = Stop-ProcessesByCommandLine -ProcessName 'cloudflared.exe' -Predicate {
  param($commandLine)
  $commandLine -like "*tunnel*" -and $commandLine -like "*http://localhost:$Port*"
}

if ($fallbackTunnelCount -gt 0 -and -not ($stopped -contains 'cloudflared')) {
  $stopped += 'cloudflared'
}

Remove-Item (Join-Path $runtimeDir 'public-url.txt') -ErrorAction SilentlyContinue

if ($stopped.Count -eq 0) {
  Write-Host 'No managed local publish processes were running.'
  exit 0
}

Write-Host ('Stopped: ' + ($stopped -join ', '))
