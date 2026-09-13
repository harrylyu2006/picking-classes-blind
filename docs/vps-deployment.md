# Deploy the dashboard on a VPS

This project already generates a complete static website: HTML plus aggregate CSV downloads. The VPS runs one Caddy container. It needs no Python service, database, Node server, Qualtrics API key, or Google account. Qualtrics remains the survey collector; Looker Studio remains a separate optional report. Hosting this HTML dashboard does not create either service.

The shipped site uses synthetic data. Keep its **SYNTHETIC DEMO** label until replacing it with a reviewed participant run.

## 1. Prepare the server

Assumptions: a current Ubuntu or Debian VPS, SSH access, and a sudo-capable account. If Docker Engine and the Compose plugin already work, skip installation.

Follow the official [Ubuntu installation guide](https://docs.docker.com/engine/install/ubuntu/) or [Debian installation guide](https://docs.docker.com/engine/install/debian/), using the distribution's Docker apt repository. Install `docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin`, and `docker-compose-plugin`. For the remaining commands, install the small file-transfer tools:

```bash
sudo apt update
sudo apt install -y git rsync curl
sudo docker version
sudo docker compose version
```

Allow inbound TCP 80 and 443 in the VPS provider's firewall/security group; UDP 443 is optional for HTTP/3. Preserve your SSH access. For Docker-published ports, do not assume UFW alone controls access; Docker's [firewall notes](https://docs.docker.com/engine/install/ubuntu/#firewall-limitations) explain the interaction. If another web server already owns ports 80/443, use the existing-proxy option below instead of replacing it.

## 2. Clone and start the synthetic dashboard

Run these commands on the VPS. No GitHub login is needed to clone this public repository.

```bash
git clone https://github.com/harrylyu2006/picking-classes-blind.git
cd picking-classes-blind
cp .env.example .env
mkdir -p deploy/public
cp -R demo/public/. deploy/public/
sudo docker compose config --quiet
sudo docker compose pull
sudo docker compose up -d
sudo docker compose ps
curl -I http://127.0.0.1/
```

Open `http://YOUR_VPS_IP/`. The default `.env` uses `SITE_ADDRESS=:80`, so an IP-only launch serves HTTP. `restart: unless-stopped` brings the container back after a Docker/server restart. Only `deploy/public/` is mounted into the web root; the repository and private datasets are outside it. Bind mounts fail if their source files/directories are missing instead of silently creating incorrect sources.

## 3. Add a domain and HTTPS

Point your domain's A record to the VPS IPv4 address. This configuration explicitly publishes ports on IPv4 (`0.0.0.0`), so leave the domain's AAAA record unset unless you separately configure and verify Docker's IPv6 port publication and external IPv6 access. Make sure TCP 80/443 reach this server. Then edit `.env`:

```dotenv
SITE_ADDRESS=classes.example.com
BIND_ADDRESS=0.0.0.0
HTTP_PORT=80
HTTPS_PORT=443
```

Use your actual domain, without `https://` or a path. Apply the environment change:

```bash
sudo docker compose up -d --force-recreate
sudo docker compose logs --tail=50 dashboard
curl -I https://classes.example.com/
```

Caddy obtains and renews a certificate and redirects HTTP to HTTPS once DNS and external port access are correct. Certificate state persists in the named `caddy_data` volume. [Caddy HTTPS prerequisites](https://caddyserver.com/docs/quick-starts/https).

## 4. Replace the demo with actual aggregate results

The simplest arrangement is to process responses on your own computer, then copy only the reviewed public output to the VPS. On your computer, from the same checked-out project used to freeze the production methods:

```bash
uv sync --frozen
uv run pcb verify-lock --lock methods-lock-production.json
uv run pcb run data/raw/qualtrics-export.csv \
  --output runs/collection-final-20260920 \
  --lock methods-lock-production.json
```

Use a new run directory each time. Review `qa_report.md`, the private audit and `public/chart_status.csv`. The participant run will correctly withhold unsupported subgroup charts. Never copy the raw CSV, the run's parent directory, or its `private/` folder to the web root.

For a simple update, pause the site during the transfer so visitors cannot see mixed old/new tables. On the VPS, from the cloned repo:

```bash
sudo docker compose stop dashboard
```

From your computer, replace `USER`, `VPS_IP`, and the remote checkout path:

```bash
rsync -av --delete runs/collection-final-20260920/public/ \
  USER@VPS_IP:/absolute/path/to/picking-classes-blind/deploy/public/
```

The trailing `/public/` is intentional: only files inside that directory are transferred. `--delete` removes stale public files from that dedicated web-root directory. Double-check the destination before running it. Then on the VPS:

```bash
sudo docker compose start dashboard
curl -I http://127.0.0.1/
```

For a domain-based deployment, check the real HTTPS URL as well. Keep a local copy of the previous public release so you can restore it with the same transfer procedure. The web-root staging directory is Git-ignored, so `git pull` does not overwrite real results with the bundled demo.

If you prefer to run Python on the VPS, install uv there and use `uv sync --frozen` / `uv run pcb` from the checkout root. Participant runs intentionally reject a runtime imported from a different checkout or a wheel-only installation. Keep raw files and full runs outside `deploy/public/`.

## Existing reverse proxy

If Nginx, Caddy or another proxy already serves your VPS domains, change `.env` to keep this container reachable only locally:

```dotenv
SITE_ADDRESS=:80
BIND_ADDRESS=127.0.0.1
HTTP_PORT=8080
HTTPS_PORT=8443
```

Start the Compose stack, then configure your existing HTTPS virtual host to proxy to `http://127.0.0.1:8080`. TLS belongs to the existing proxy in this mode. Do not set the inner `SITE_ADDRESS` to the public domain or it will try to manage its own public certificates.

## Routine commands

```bash
# Status and recent logs
sudo docker compose ps
sudo docker compose logs --tail=100 dashboard

# Validate the Caddy configuration
sudo docker compose exec dashboard caddy validate --config /etc/caddy/Caddyfile

# Update deployment files and the maintained Caddy 2 image
git pull --ff-only
sudo docker compose pull
sudo docker compose up -d --force-recreate

# Stop containers while preserving certificate volumes and staged data
sudo docker compose down
```

Do not add `--volumes` when you intend to preserve certificate state. The `caddy:2-alpine` tag receives updates; test changes before updating a live site. For a fixed infrastructure release, replace it with a tested official image digest and record that deployment version separately from the survey methods lock.

If the site is unreachable, check `docker compose ps`, Caddy logs, provider firewall rules and port conflicts. A blank/404 site usually means the public files were not copied into `deploy/public/`. TLS failures usually mean DNS or external port access is incorrect. The committed demo footer calls itself a local preview; serving that same file on a VPS does not turn synthetic results into participant findings.
