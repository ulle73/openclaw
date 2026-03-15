# Instagram Autopublish Setup

Add these keys in `.env.local`:

```env
INSTAGRAM_ACCESS_TOKEN=ig-user-access-token
INSTAGRAM_APP_SCOPED_USER_ID=1784...
INSTAGRAM_GRAPH_BASE_URL=https://graph.instagram.com
INSTAGRAM_GRAPH_API_VERSION=v25.0

PUBLIC_BASE_URL=https://your-public-app-url-or-tunnel

INSTAGRAM_AUTO_PUBLISH=true
AUTO_QUEUE_ENABLED=true
AUTO_QUEUE_INTERVAL_MS=300000
ACTIVE_BRAND=default
```

## Notes

- Meta must be able to fetch images from a public URL.
- If running locally, use a tunnel (for example Cloudflare tunnel).
- Scheduled posts (`status=scheduled`) are automatically published by queue worker when due.

## Recommended Sheet Statuses

- `new`
- `processing`
- `generated`
- `approved`
- `scheduled`
- `publishing`
- `published`
- `error`

## Local Scripts

Start local publish stack:

```powershell
.\scripts\start-local-publish.ps1
```

Stop local publish stack:

```powershell
.\scripts\stop-local-publish.ps1
```
