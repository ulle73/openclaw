## [ERR-20260307-001] openclaw skills info

**Logged**: 2026-03-07T22:49:28.783039Z
**Priority**: medium
**Status**: pending
**Area**: tools

### Summary
`openclaw skills info` requires a skill name argument

### Error
```
missing required argument 'name'
```

### Context
- Command: `openclaw skills info`
- Environment: Windows PowerShell, current dir workspace

### Suggested Fix
Include the skill name when running `openclaw skills info` (e.g., `openclaw skills info self-improvement`).

### Metadata
- Reproducible: yes
- Related Files: None
- Source: command_failure

---

## [ERR-20260312-002] scripts/desktop_control.ps1

**Logged**: 2026-03-12T21:52:00+01:00
**Priority**: medium
**Status**: pending
**Area**: tools

### Summary
`desktop_control.ps1 -RawMessage ...` failed before execution with ChildPath type conversion error.

### Error
```
Cannot convert 'System.Object[]' to the type 'System.String' required by parameter 'ChildPath'.
```

### Context
- Command: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/desktop_control.ps1 -RawMessage "Open Outlook and click New Email"`
- Environment: Windows PowerShell in workspace

### Suggested Fix
Inspect path-building logic in `scripts/desktop_control.ps1` where `Join-Path -ChildPath` may receive an array; cast/sanitize input to string before Join-Path.

### Metadata
- Reproducible: yes
- Related Files: scripts/desktop_control.ps1
- Source: command_failure

---
