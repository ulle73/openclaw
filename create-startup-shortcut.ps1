$ws = New-Object -ComObject WScript.Shell
$startup = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup'
$lnk = Join-Path $startup 'Start Gateway.lnk'
$sc = $ws.CreateShortcut($lnk)
$sc.TargetPath = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
$sc.Arguments = '-NoExit -File "C:\Users\ryd\.openclaw\workspace\start-gateway.ps1"'
$sc.WorkingDirectory = 'C:\Users\ryd\.openclaw\workspace'
$sc.Save()
