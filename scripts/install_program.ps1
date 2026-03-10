[CmdletBinding()]
param(
    [ValidateSet("verify", "install-winget", "install-url")]
    [string]$Action = "verify",
    [string]$Name = "",
    [string]$WingetId = "",
    [string]$DownloadUrl = "",
    [string]$SilentArgs = "",
    [ValidateSet("auto", "none", "quiet", "nsis", "inno", "installshield")]
    [string]$SilentProfile = "auto",
    [string]$VerifyCommand = "",
    [string]$VerifyPath = "",
    [int]$TimeoutSeconds = 900
)

$ErrorActionPreference = "Stop"

function Get-CommandPath {
    param([Parameter(Mandatory = $true)][string]$Name)

    $command = Get-Command $Name -ErrorAction Stop
    return $command.Source
}

function Invoke-ExternalProcess {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [string]$ArgumentList = "",
        [int]$Timeout = 900
    )

    $process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -PassThru -WindowStyle Hidden
    if (-not $process.WaitForExit($Timeout * 1000)) {
        try {
            $process.Kill()
        } catch {
        }
        throw "Process timeout after $Timeout seconds: $FilePath $ArgumentList"
    }

    return $process.ExitCode
}

function Test-Verify {
    param(
        [string]$CommandToRun,
        [string]$PathToCheck,
        [string]$WingetPackageId
    )

    if ($CommandToRun) {
        $tempScript = Join-Path $env:TEMP ("openclaw-verify-" + [System.Guid]::NewGuid().ToString() + ".ps1")
        try {
            Set-Content -LiteralPath $tempScript -Value $CommandToRun -Encoding UTF8
            $output = & powershell -NoProfile -ExecutionPolicy Bypass -File $tempScript 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0 -or $?) {
                return @{
                    Ok = $true
                    Detail = $output.Trim()
                }
            }
            return @{
                Ok = $false
                Detail = $output.Trim()
            }
        } finally {
            if (Test-Path -LiteralPath $tempScript) {
                Remove-Item -Force -LiteralPath $tempScript
            }
        }
    }

    if ($PathToCheck) {
        if (Test-Path -LiteralPath $PathToCheck) {
            return @{
                Ok = $true
                Detail = "Found path: $PathToCheck"
            }
        }
        return @{
            Ok = $false
            Detail = "Missing path: $PathToCheck"
        }
    }

    if ($WingetPackageId) {
        $winget = Get-CommandPath -Name "winget"
        $output = & $winget list --id $WingetPackageId --exact --accept-source-agreements 2>&1 | Out-String
        if ($LASTEXITCODE -eq 0 -and $output -match [Regex]::Escape($WingetPackageId)) {
            return @{
                Ok = $true
                Detail = $output.Trim()
            }
        }
        return @{
            Ok = $false
            Detail = $output.Trim()
        }
    }

    return @{
        Ok = $true
        Detail = "No explicit verification target provided; install command completed."
    }
}

function Get-TempInstallerPath {
    param([Parameter(Mandatory = $true)][string]$Url)

    $uri = [System.Uri]$Url
    $leaf = [System.IO.Path]::GetFileName($uri.AbsolutePath)
    if (-not $leaf) {
        $leaf = "installer.bin"
    }

    $targetDir = Join-Path $env:TEMP "openclaw-installs"
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    return Join-Path $targetDir $leaf
}

function Resolve-DownloadedFilePath {
    param(
        [Parameter(Mandatory = $true)][string]$InitialPath,
        [Parameter(Mandatory = $true)]$Response
    )

    $currentPath = $InitialPath
    $headers = $Response.Headers
    $contentDisposition = $headers["Content-Disposition"]
    if (-not $contentDisposition -and $headers["content-disposition"]) {
        $contentDisposition = $headers["content-disposition"]
    }

    $serverFilename = $null
    if ($contentDisposition -and $contentDisposition -match 'filename="?([^";]+)"?') {
        $serverFilename = $matches[1]
    }

    if (-not $serverFilename) {
        $contentType = $headers["Content-Type"]
        if (-not $contentType -and $headers["content-type"]) {
            $contentType = $headers["content-type"]
        }
        $extension = [System.IO.Path]::GetExtension($currentPath)
        if (-not $extension) {
            switch -Regex ($contentType) {
                "msi" { $serverFilename = ([System.IO.Path]::GetFileName($currentPath) + ".msi") }
                "zip" { $serverFilename = ([System.IO.Path]::GetFileName($currentPath) + ".zip") }
                "msix|appx" { $serverFilename = ([System.IO.Path]::GetFileName($currentPath) + ".msix") }
                "octet-stream|application/x-msdownload" { $serverFilename = ([System.IO.Path]::GetFileName($currentPath) + ".exe") }
            }
        }
    }

    if (-not $serverFilename) {
        return $currentPath
    }

    $safeFilename = [System.IO.Path]::GetFileName($serverFilename)
    $resolvedPath = Join-Path ([System.IO.Path]::GetDirectoryName($currentPath)) $safeFilename
    if ($resolvedPath -ne $currentPath) {
        if (Test-Path $resolvedPath) {
            Remove-Item -Force $resolvedPath
        }
        Move-Item -Force -LiteralPath $currentPath -Destination $resolvedPath
        return $resolvedPath
    }
    return $currentPath
}

function Get-ExeArgumentCandidates {
    param(
        [string]$Profile,
        [string]$ExplicitArgs
    )

    if ($ExplicitArgs) {
        return @($ExplicitArgs)
    }

    switch ($Profile) {
        "none" { return @("") }
        "quiet" { return @("/quiet /norestart") }
        "nsis" { return @("/S") }
        "inno" { return @("/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-") }
        "installshield" { return @("/s /v/qn") }
        default {
            return @(
                "/quiet /norestart",
                "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-",
                "/S",
                "/s /v/qn"
            )
        }
    }
}

function Install-WithWinget {
    param([Parameter(Mandatory = $true)][string]$PackageId)

    $winget = Get-CommandPath -Name "winget"
    $args = @(
        "install",
        "--id", $PackageId,
        "--exact",
        "--silent",
        "--accept-package-agreements",
        "--accept-source-agreements",
        "--disable-interactivity"
    )
    $code = Invoke-ExternalProcess -FilePath $winget -ArgumentList ($args -join " ") -Timeout $TimeoutSeconds
    if ($code -ne 0 -and $code -ne 3010) {
        throw "winget install failed with exit code $code for $PackageId"
    }
}

function Install-FromUrl {
    param([Parameter(Mandatory = $true)][string]$Url)

    $targetPath = Get-TempInstallerPath -Url $Url
    $response = Invoke-WebRequest -Uri $Url -OutFile $targetPath -PassThru
    $targetPath = Resolve-DownloadedFilePath -InitialPath $targetPath -Response $response

    $extension = [System.IO.Path]::GetExtension($targetPath).ToLowerInvariant()
    if ($extension -eq ".msi") {
        $code = Invoke-ExternalProcess -FilePath "msiexec.exe" -ArgumentList "/i `"$targetPath`" /qn /norestart" -Timeout $TimeoutSeconds
        if ($code -ne 0 -and $code -ne 3010) {
            throw "MSI install failed with exit code $code"
        }
        return $targetPath
    }

    if ($extension -in @(".msix", ".msixbundle", ".appx", ".appxbundle")) {
        Add-AppxPackage -Path $targetPath
        return $targetPath
    }

    if ($extension -eq ".zip") {
        $extractDir = Join-Path ([System.IO.Path]::GetDirectoryName($targetPath)) ([System.IO.Path]::GetFileNameWithoutExtension($targetPath))
        if (Test-Path $extractDir) {
            Remove-Item -Recurse -Force $extractDir
        }
        Expand-Archive -Path $targetPath -DestinationPath $extractDir -Force
        return $extractDir
    }

    if ($extension -eq ".exe" -or -not $extension) {
        $attempts = Get-ExeArgumentCandidates -Profile $SilentProfile -ExplicitArgs $SilentArgs
        $attemptErrors = @()
        foreach ($args in $attempts) {
            try {
                $code = Invoke-ExternalProcess -FilePath $targetPath -ArgumentList $args -Timeout $TimeoutSeconds
                if ($code -eq 0 -or $code -eq 3010) {
                    Start-Sleep -Seconds 3
                    return $targetPath
                }
                $attemptErrors += "args=[$args] exit=$code"
            } catch {
                $attemptErrors += "args=[$args] error=$($_.Exception.Message)"
            }
        }
        throw "EXE install failed. Attempts: $($attemptErrors -join '; ')"
    }

    throw "Unsupported installer type: $extension"
}

switch ($Action) {
    "verify" {
        $verification = Test-Verify -CommandToRun $VerifyCommand -PathToCheck $VerifyPath -WingetPackageId $WingetId
        if (-not $verification.Ok) {
            Write-Error $verification.Detail
        }
        Write-Output $verification.Detail
    }

    "install-winget" {
        if (-not $WingetId) {
            throw "install-winget requires -WingetId"
        }
        Install-WithWinget -PackageId $WingetId
        $verification = Test-Verify -CommandToRun $VerifyCommand -PathToCheck $VerifyPath -WingetPackageId $WingetId
        if (-not $verification.Ok) {
            throw "Install completed but verification failed: $($verification.Detail)"
        }
        Write-Output "Installed via winget: $WingetId"
        Write-Output $verification.Detail
    }

    "install-url" {
        if (-not $DownloadUrl) {
            throw "install-url requires -DownloadUrl"
        }
        $location = Install-FromUrl -Url $DownloadUrl
        $verification = Test-Verify -CommandToRun $VerifyCommand -PathToCheck $VerifyPath -WingetPackageId $WingetId
        if (-not $verification.Ok) {
            throw "Install completed from URL but verification failed: $($verification.Detail)"
        }
        Write-Output "Installed from URL: $DownloadUrl"
        Write-Output "Artifact: $location"
        Write-Output $verification.Detail
    }
}
