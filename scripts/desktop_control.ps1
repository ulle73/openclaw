[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RawMessage,
    [switch]$Json
)

$ErrorActionPreference = "Stop"

function Write-Result {
    param(
        [bool]$Handled,
        [bool]$Ok,
        [string]$Message
    )

    $payload = @{
        handled = $Handled
        ok = $Ok
        message = $Message
    }

    if ($Json) {
        $payload | ConvertTo-Json -Compress
    } else {
        $Message
    }
}

function Normalize-Text {
    param([string]$Value)

    if (-not $Value) {
        return ""
    }

    $normalized = $Value.Normalize([Text.NormalizationForm]::FormD)
    $builder = New-Object System.Text.StringBuilder
    foreach ($char in $normalized.ToCharArray()) {
        $category = [Globalization.CharUnicodeInfo]::GetUnicodeCategory($char)
        if ($category -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$builder.Append($char)
        }
    }

    $ascii = $builder.ToString().ToLowerInvariant()
    $ascii = [Regex]::Replace($ascii, "[^a-z0-9]+", " ")
    return [Regex]::Replace($ascii, "\s+", " ").Trim()
}

function Resolve-AppAlias {
    param([string]$Target)

    $normalized = Normalize-Text $Target
    $aliases = @{
        "paper desktop" = "Paper"
        "paper" = "Paper"
        "antigravity" = "Antigravity"
        "anti gravity" = "Antigravity"
        "telegram" = "Telegram"
        "discord" = "Discord"
        "visual studio code" = "Visual Studio Code"
        "vscode" = "Visual Studio Code"
        "edge" = "Microsoft Edge"
        "microsoft edge" = "Microsoft Edge"
    }

    if ($aliases.ContainsKey($normalized)) {
        return $aliases[$normalized]
    }
    return $Target.Trim()
}

function Get-ShortcutInfo {
    param([string]$ShortcutPath)

    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($ShortcutPath)
    return @{
        ShortcutPath = $ShortcutPath
        TargetPath = $shortcut.TargetPath
        Arguments = $shortcut.Arguments
        WorkingDirectory = $shortcut.WorkingDirectory
    }
}

function Find-AppTarget {
    param([string]$Target)

    $resolved = Resolve-AppAlias $Target
    $normalized = Normalize-Text $resolved
    $desktop = Join-Path $env:USERPROFILE "Desktop"
    $startMenu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
    $roots = @(
        @{ Type = "desktop-shortcut"; Path = $desktop; Filter = "*.lnk" },
        @{ Type = "startmenu-shortcut"; Path = $startMenu; Filter = "*.lnk" }
    )

    foreach ($root in $roots) {
        if (-not (Test-Path $root.Path)) {
            continue
        }
        $items = Get-ChildItem -Path $root.Path -Filter $root.Filter -Recurse -ErrorAction SilentlyContinue
        foreach ($item in $items) {
            $stem = [System.IO.Path]::GetFileNameWithoutExtension($item.Name)
            $itemNorm = Normalize-Text $stem
            if ($itemNorm -eq $normalized -or $itemNorm -like "*$normalized*" -or $normalized -like "*$itemNorm*") {
                $shortcutInfo = Get-ShortcutInfo $item.FullName
                return @{
                    DisplayName = $stem
                    Type = $root.Type
                    LaunchPath = $item.FullName
                    TargetPath = $shortcutInfo.TargetPath
                    Arguments = $shortcutInfo.Arguments
                    WorkingDirectory = $shortcutInfo.WorkingDirectory
                }
            }
        }
    }

    $exeCandidates = @(
        Join-Path $env:LOCALAPPDATA "Programs",
        $env:ProgramFiles,
        ${env:ProgramFiles(x86)}
    ) | Where-Object { $_ -and (Test-Path $_) }

    foreach ($root in $exeCandidates) {
        $items = Get-ChildItem -Path $root -Filter "*.exe" -Recurse -ErrorAction SilentlyContinue
        foreach ($item in $items) {
            $stem = [System.IO.Path]::GetFileNameWithoutExtension($item.Name)
            $itemNorm = Normalize-Text $stem
            if ($itemNorm -eq $normalized -or $itemNorm -like "*$normalized*" -or $normalized -like "*$itemNorm*") {
                return @{
                    DisplayName = $stem
                    Type = "executable"
                    LaunchPath = $item.FullName
                    TargetPath = $item.FullName
                    Arguments = ""
                    WorkingDirectory = $item.DirectoryName
                }
            }
        }
    }

    return $null
}

function Wait-ForProcess {
    param(
        [string]$ExecutablePath,
        [int]$TimeoutSeconds = 20
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $exeLeaf = [System.IO.Path]::GetFileNameWithoutExtension($ExecutablePath)

    while ((Get-Date) -lt $deadline) {
        $matches = @(Get-Process -ErrorAction SilentlyContinue | Where-Object {
            try {
                $_.Path -eq $ExecutablePath -or $_.ProcessName -eq $exeLeaf
            } catch {
                $false
            }
        })

        if ($matches) {
            $windowed = @($matches | Where-Object {
                try {
                    $_.MainWindowHandle -ne 0 -or -not [string]::IsNullOrWhiteSpace($_.MainWindowTitle)
                } catch {
                    $false
                }
            })

            if ($windowed.Count -gt 0) {
                return ($windowed | Sort-Object Id -Descending | Select-Object -First 1)
            }

            return ($matches | Sort-Object Id -Descending | Select-Object -First 1)
        }
        Start-Sleep -Milliseconds 500
    }

    return $null
}

function Start-AppTarget {
    param([hashtable]$AppTarget)

    if (-not $AppTarget) {
        throw "No app target provided."
    }

    if ($AppTarget.Type -like "*shortcut") {
        Start-Process -FilePath $AppTarget.LaunchPath | Out-Null
    } else {
        $params = @{
            FilePath = $AppTarget.LaunchPath
        }
        if ($AppTarget.Arguments) {
            $params.ArgumentList = $AppTarget.Arguments
        }
        if ($AppTarget.WorkingDirectory) {
            $params.WorkingDirectory = $AppTarget.WorkingDirectory
        }
        Start-Process @params | Out-Null
    }

    $process = Wait-ForProcess -ExecutablePath $AppTarget.TargetPath
    if (-not $process) {
        throw "Appen startade inte eller stangde sig direkt: $($AppTarget.DisplayName)"
    }
    return $process
}

function Get-TopWindowElement {
    param([int]$ProcessId)

    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes

    $root = [System.Windows.Automation.AutomationElement]::RootElement
    $condition = New-Object System.Windows.Automation.AndCondition(
        (New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ProcessIdProperty, $ProcessId)),
        (New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Window))
    )

    return $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $condition)
}

function Invoke-ControlByName {
    param(
        [int]$ProcessId,
        [string]$ControlName,
        [int]$TimeoutSeconds = 15
    )

    $normalizedTarget = Normalize-Text $ControlName
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)

    while ((Get-Date) -lt $deadline) {
        $window = Get-TopWindowElement -ProcessId $ProcessId
        if ($window) {
            $elements = $window.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
            foreach ($element in $elements) {
                try {
                    $name = $element.Current.Name
                    if (-not $name) {
                        continue
                    }
                    $candidate = Normalize-Text $name
                    if ($candidate -ne $normalizedTarget -and $candidate -notlike "*$normalizedTarget*") {
                        continue
                    }

                    $invokePattern = $null
                    if ($element.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$invokePattern)) {
                        $invokePattern.Invoke()
                        return $name
                    }

                    $selectionPattern = $null
                    if ($element.TryGetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern, [ref]$selectionPattern)) {
                        $selectionPattern.Select()
                        return $name
                    }
                } catch {
                }
            }
        }
        Start-Sleep -Milliseconds 400
    }

    return $null
}

function Parse-DesktopRequest {
    param([string]$Message)

    $clean = ($Message -replace "\r", " " -replace "\n", " ").Trim()
    $launchMatch = [Regex]::Match($clean, "(?i)(?:starta|oppna|öppna|launch|open)\s+(.+?)(?:(?:,|\s+och\s+|\s+then\s+)(?:tryck pa|tryck på|klicka pa|klicka på|click|press)\s+|$)")
    $clickMatch = [Regex]::Match($clean, "(?i)(?:tryck pa|tryck på|klicka pa|klicka på|click|press)\s+(.+?)$")

    $launchTarget = if ($launchMatch.Success) { $launchMatch.Groups[1].Value.Trim(" ,""'") } else { "" }
    $clickTarget = if ($clickMatch.Success) { $clickMatch.Groups[1].Value.Trim(" ,""'") } else { "" }

    $launchTarget = $launchTarget -replace "(?i)\s+pa min dator$", ""
    $launchTarget = $launchTarget -replace "(?i)\s+som ligger pa skrivbordet$", ""
    $launchTarget = $launchTarget -replace "(?i)\s+som ligger på skrivbordet$", ""
    $launchTarget = $launchTarget.Trim()

    $handled = [bool]($launchTarget -or $clickTarget)
    return @{
        Handled = $handled
        LaunchTarget = $launchTarget
        ClickTarget = $clickTarget
    }
}

function Parse-DesktopRequestSafe {
    param([string]$Message)

    $clean = Normalize-Text ($Message -replace "\r", " " -replace "\n", " ")
    $launchMatch = [Regex]::Match($clean, "(?i)(?:starta|oppna|launch|open)\s+(.+?)(?:(?:,|\s+och\s+|\s+then\s+)(?:tryck pa|klicka pa|click|press)\s+|$)")
    $clickMatch = [Regex]::Match($clean, "(?i)(?:tryck pa|klicka pa|click|press)\s+(.+?)$")

    $launchTarget = if ($launchMatch.Success) { $launchMatch.Groups[1].Value.Trim(" ,""'") } else { "" }
    $clickTarget = if ($clickMatch.Success) { $clickMatch.Groups[1].Value.Trim(" ,""'") } else { "" }

    $launchTarget = $launchTarget -replace "(?i)\s+pa min dator$", ""
    $launchTarget = $launchTarget -replace "(?i)\s+som ligger pa skrivbordet$", ""
    $launchTarget = $launchTarget -replace "(?i)\s+pa skrivbordet$", ""
    $launchTarget = $launchTarget -replace "(?i)\s+for mig$", ""
    $launchTarget = $launchTarget.Trim()

    $handled = [bool]($launchTarget -or $clickTarget)
    return @{
        Handled = $handled
        LaunchTarget = $launchTarget
        ClickTarget = $clickTarget
    }
}

$request = Parse-DesktopRequestSafe -Message $RawMessage
if (-not $request.Handled) {
    Write-Result -Handled $false -Ok $false -Message "No desktop action detected."
    exit 0
}

try {
    $status = @()
    $process = $null

    if ($request.LaunchTarget) {
        $target = Find-AppTarget -Target $request.LaunchTarget
        if (-not $target) {
            Write-Result -Handled $true -Ok $false -Message "Kunde inte hitta en lokal app eller genvag for: $($request.LaunchTarget)"
            exit 1
        }

        $process = Start-AppTarget -AppTarget $target
        $status += "Startade $($target.DisplayName)"
    }

    if ($request.ClickTarget) {
        if (-not $process) {
            Write-Result -Handled $true -Ok $false -Message "Det finns ingen aktiv app att klicka i for begaran: $($request.ClickTarget)"
            exit 1
        }

        $clicked = Invoke-ControlByName -ProcessId $process.Id -ControlName $request.ClickTarget
        if (-not $clicked) {
            Write-Result -Handled $true -Ok $false -Message "Startade appen men hittade ingen klickbar kontroll som matchar: $($request.ClickTarget)"
            exit 1
        }
        $status += "tryckte pa $clicked"
    }

    $message = ($status -join " och ") + "."
    Write-Result -Handled $true -Ok $true -Message $message
    exit 0
} catch {
    Write-Result -Handled $true -Ok $false -Message $_.Exception.Message
    exit 1
}
