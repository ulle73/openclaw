param(
  [int]$Port = 3000,
  [string]$EnvFile = '.env.local',
  [int]$TunnelTimeoutSeconds = 45,
  [switch]$SafeMode
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$runtimeDir = Join-Path $repoRoot '.runtime'
$envPath = Join-Path $repoRoot $EnvFile

function Resolve-ExecutablePath {
  param(
    [Parameter(Mandatory = $true)]
    [string]$CommandName,
    [string[]]$Fallbacks = @()
  )

  $command = Get-Command $CommandName -ErrorAction SilentlyContinue
  if ($command) {
    return $command.Source
  }

  foreach ($candidate in $Fallbacks) {
    if ($candidate -and (Test-Path $candidate)) {
      return $candidate
    }
  }

  throw "Could not find executable for $CommandName."
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
    return
  }

  foreach ($process in $processes) {
    $commandLine = [string]$process.CommandLine
    if (& $Predicate $commandLine) {
      Stop-Process -Id $process.ProcessId -Force -ErrorAction SilentlyContinue
    }
  }
}

function Set-EnvValue {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Path,
    [Parameter(Mandatory = $true)]
    [string]$Key,
    [Parameter(Mandatory = $true)]
    [string]$Value
  )

  if (-not (Test-Path $Path)) {
    throw "Environment file not found: $Path"
  }

  $content = Get-Content $Path -Raw
  $line = "$Key=$Value"
  $pattern = "(?m)^" + [regex]::Escape($Key) + "=.*$"

  if ([regex]::IsMatch($content, $pattern)) {
    $updated = [regex]::Replace($content, $pattern, $line, 1)
  } else {
    $updated = $content
    if ($updated -and -not $updated.EndsWith("`n")) {
      $updated += "`r`n"
    }
    $updated += "$line`r`n"
  }

  Set-Content -Path $Path -Value $updated -NoNewline
}

function Wait-ForTunnelUrl {
  param(
    [Parameter(Mandatory = $true)]
    [string[]]$LogPaths,
    [Parameter(Mandatory = $true)]
    [int]$TimeoutSeconds
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)

  while ((Get-Date) -lt $deadline) {
    foreach ($logPath in $LogPaths) {
      if (-not (Test-Path $logPath)) {
        continue
      }

      $content = Get-Content $logPath -Raw -ErrorAction SilentlyContinue
      if ($content -match 'https://[-a-z0-9]+\.trycloudflare\.com') {
        return $matches[0]
      }
    }

    Start-Sleep -Seconds 1
  }

  return $null
}

function Wait-ForHealth {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Url,
    [Parameter(Mandatory = $true)]
    [int]$TimeoutSeconds
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)

  while ((Get-Date) -lt $deadline) {
    try {
      $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 5
      if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 300) {
        return $true
      }
    } catch {
      Start-Sleep -Milliseconds 750
    }
  }

  return $false
}

function Resolve-ListeningProcessId {
  param(
    [Parameter(Mandatory = $true)]
    [int]$Port
  )

  $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
    Select-Object -First 1

  if (-not $connection) {
    return $null
  }

  return [int]$connection.OwningProcess
}

function Write-TextFile {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Path,
    [Parameter(Mandatory = $true)]
    [string]$Value
  )

  Set-Content -Path $Path -Value $Value -NoNewline
}

New-Item -ItemType Directory -Path $runtimeDir -Force | Out-Null

$cloudflaredExe = Resolve-ExecutablePath -CommandName 'cloudflared' -Fallbacks @(
  (Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages\Cloudflare.cloudflared_Microsoft.Winget.Source_8wekyb3d8bbwe\cloudflared.exe')
)
$nodeExe = Resolve-ExecutablePath -CommandName 'node'

Stop-ProcessesByCommandLine -ProcessName 'cloudflared.exe' -Predicate {
  param($commandLine)
  $commandLine -like "*tunnel*" -and $commandLine -like "*http://localhost:$Port*"
}

Stop-ProcessesByCommandLine -ProcessName 'node.exe' -Predicate {
  param($commandLine)
  ($commandLine -match [regex]::Escape($repoRoot)) -and (
    $commandLine -match 'index\.js' -or
    $commandLine -match 'cli\.js\s+serve'
  )
}

$cloudflaredOut = Join-Path $runtimeDir 'cloudflared.out.log'
$cloudflaredErr = Join-Path $runtimeDir 'cloudflared.err.log'
$appOut = Join-Path $runtimeDir 'app.out.log'
$appErr = Join-Path $runtimeDir 'app.err.log'

Remove-Item $cloudflaredOut, $cloudflaredErr, $appOut, $appErr -ErrorAction SilentlyContinue

$cloudflaredProcess = Start-Process `
  -FilePath $cloudflaredExe `
  -ArgumentList @('tunnel', '--url', "http://localhost:$Port") `
  -WorkingDirectory $repoRoot `
  -WindowStyle Hidden `
  -RedirectStandardOutput $cloudflaredOut `
  -RedirectStandardError $cloudflaredErr `
  -PassThru

$publicBaseUrl = Wait-ForTunnelUrl -LogPaths @($cloudflaredOut, $cloudflaredErr) -TimeoutSeconds $TunnelTimeoutSeconds

if (-not $publicBaseUrl) {
  throw "Could not read a Cloudflare tunnel URL within $TunnelTimeoutSeconds seconds. Check $cloudflaredErr"
}

Set-EnvValue -Path $envPath -Key 'PUBLIC_BASE_URL' -Value $publicBaseUrl
Write-TextFile -Path (Join-Path $runtimeDir 'cloudflared.pid') -Value ([string]$cloudflaredProcess.Id)
Write-TextFile -Path (Join-Path $runtimeDir 'public-url.txt') -Value $publicBaseUrl

$oldAutoQueue = [Environment]::GetEnvironmentVariable('AUTO_QUEUE_ENABLED', 'Process')
$oldAutoPublish = [Environment]::GetEnvironmentVariable('INSTAGRAM_AUTO_PUBLISH', 'Process')

try {
  if ($SafeMode) {
    $env:AUTO_QUEUE_ENABLED = 'false'
    $env:INSTAGRAM_AUTO_PUBLISH = 'false'
  }

  $appProcess = Start-Process `
    -FilePath $nodeExe `
    -ArgumentList @('index.js') `
    -WorkingDirectory $repoRoot `
    -WindowStyle Hidden `
    -RedirectStandardOutput $appOut `
    -RedirectStandardError $appErr `
    -PassThru
} finally {
  if ($null -eq $oldAutoQueue) {
    Remove-Item Env:\AUTO_QUEUE_ENABLED -ErrorAction SilentlyContinue
  } else {
    $env:AUTO_QUEUE_ENABLED = $oldAutoQueue
  }

  if ($null -eq $oldAutoPublish) {
    Remove-Item Env:\INSTAGRAM_AUTO_PUBLISH -ErrorAction SilentlyContinue
  } else {
    $env:INSTAGRAM_AUTO_PUBLISH = $oldAutoPublish
  }
}

if (-not (Wait-ForHealth -Url "http://localhost:$Port/health" -TimeoutSeconds 30)) {
  throw "App did not become healthy on http://localhost:$Port/health. Check $appErr"
}

$listeningAppPid = Resolve-ListeningProcessId -Port $Port
if ($listeningAppPid) {
  Write-TextFile -Path (Join-Path $runtimeDir 'app.pid') -Value ([string]$listeningAppPid)
} else {
  Write-TextFile -Path (Join-Path $runtimeDir 'app.pid') -Value ([string]$appProcess.Id)
}

if (-not (Wait-ForHealth -Url "$publicBaseUrl/health" -TimeoutSeconds 45)) {
  Write-Warning "Tunnel URL is created but public health is still warming up: $publicBaseUrl/health"
}

Write-Host ''
Write-Host 'Local publish stack is running.'
Write-Host "Public URL: $publicBaseUrl"
Write-Host "Dashboard: $publicBaseUrl/"
Write-Host "Health: $publicBaseUrl/health"
Write-Host "App log: $appOut"
Write-Host "Tunnel log: $cloudflaredOut"

if ($SafeMode) {
  Write-Host 'Safe mode is on: AUTO_QUEUE_ENABLED=false and INSTAGRAM_AUTO_PUBLISH=false for this app process.'
}
