# Brands

Each folder in this directory is a complete customer profile.

Structure:

- `brands/<brand-key>/brand.yaml`
- `brands/<brand-key>/company.yaml`
- `brands/<brand-key>/platforms.yaml`
- `brands/<brand-key>/knowledge/**.md`

How to add a new customer:

1. Copy `brands/template` to `brands/<new-brand-key>`.
2. Edit all files in that new folder.
3. Start the app with `ACTIVE_BRAND=<new-brand-key>` or switch brand in the dashboard.
