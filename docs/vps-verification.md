# VPS configuration verification

Verified locally on September 13, 2026 using Docker Engine 29.7.2 and the official `caddy:2-alpine` image, which resolved to Caddy 2.11.4 in this run.

- `docker compose config --quiet` passed.
- Caddy's configuration validator passed for the default HTTP site.
- The Compose stack started with a test project name and ports bound only to `127.0.0.1`.
- `GET /` returned 200 and the expected **SYNTHETIC DEMO** label.
- `GET /sources.csv` returned 200 with aggregate columns and no ResponseId field.
- Requests for `/private/audit.csv`, `/data/raw/qualtrics-export.csv`, `/.git/config`, `/../README.md`, `/README.md`, and `/qa_report.json` all returned 404.
- The expected `X-Content-Type-Options: nosniff` header was present.
- The original survey methods lock remained valid; deployment changes do not alter the analysis rules.
- Independent review checked the mount boundary, port/address configuration, real-data update procedure, and certificate-volume preservation. The guide was corrected to describe IPv4 defaults and force container recreation when deployment configuration changes.

This verifies the local container configuration. No user's VPS was accessed or modified, and live domain/DNS routing or certificate issuance has not been tested. Follow [the deployment guide](vps-deployment.md) for those steps.
