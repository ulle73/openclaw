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
