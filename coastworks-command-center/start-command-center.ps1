$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
Start-Process powershell -ArgumentList '-NoProfile','-Command','cd "'+$PSScriptRoot+'"; node server.mjs' -WindowStyle Minimized
Start-Process "http://localhost:4310"
Write-Output "Coastworks Command Center startad på http://localhost:4310"