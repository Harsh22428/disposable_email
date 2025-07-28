# Disposable Email Service

## Features

- Receive emails on any `@arp1it.club` address
- Inbox auto-clears after 7 days (MongoDB TTL)
- REST API via FastAPI
- SMTP Receiver via aiosmtpd

## Deployment Checklist

1. Set env vars in `.env`
2. Run `uvicorn api.main:app --host 0.0.0.0 --port 8000`
3. Start SMTP server via `python smtp_server/server.py`
4. Configure Nginx reverse proxy & Let's Encrypt
5. Add MX record for `mail.arp1it.club` → Droplet IP
