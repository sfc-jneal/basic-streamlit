# Streamlit Template (Local Docker + Streamlit in Snowflake Parity)

This project helps you run a Streamlit app locally via Docker while keeping the environment similar to Streamlit in Snowflake (SiS). It includes:
- A local Docker setup with env parity
- Key‑pair authentication to Snowflake
- Makefile helpers
- A sample GitHub Actions workflow for CI/CD

## Prerequisites
- Docker + Docker Compose
- Python knowledge (optional for local tweaks)
- Snowflake account, user, role, and warehouse

## 1) Generate a private key and enable key‑pair auth in Snowflake
This project authenticates to Snowflake with a private key. Generate a private key on your machine and register the public key to your Snowflake user.

Example using OpenSSL (no passphrase):
```bash
mkdir -p ~/.snowflake
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out ~/.snowflake/rsa_key.p8 -nocrypt
openssl rsa -in ~/.snowflake/rsa_key.p8 -pubout -out ~/.snowflake/rsa_key.pub
```

Example with a passphrase (recommended):
```bash
mkdir -p ~/.snowflake
openssl genrsa -aes256 -out ~/.snowflake/rsa_key_encrypted.pem 2048
openssl pkcs8 -topk8 -v2 aes256 -inform PEM -outform PEM \
  -in ~/.snowflake/rsa_key_encrypted.pem -out ~/.snowflake/rsa_key.p8
openssl rsa -in ~/.snowflake/rsa_key.p8 -pubout -out ~/.snowflake/rsa_key.pub
```

Register the public key to your Snowflake user (run as an admin or the user itself):
```sql
-- Replace <USER_NAME> and paste your public key contents (single line, no header/footer)
ALTER USER <USER_NAME> SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...';
-- Or use RSA_PUBLIC_KEY_2 for rotation
```

Notes:
- Keep your private key secure (permissions like `chmod 600 ~/.snowflake/rsa_key.p8`).
- If you use a passphrase, you will supply it via `.env` for local dev.

## 2) Configure environment variables
Copy the sample and fill in your values:
```bash
cp env.sample .env
```
Then edit `.env` to set your Snowflake parameters and key values, for example:
```env
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_ROLE=your_role
SNOWFLAKE_WAREHOUSE=your_wh
SNOWFLAKE_DATABASE=your_db
SNOWFLAKE_SCHEMA=public
SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/your/rsa_key.p8
SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=your_passphrase # if password protected

# Local app port (optional)
APP_PORT=8501
```

This repo’s `Makefile` auto-loads `.env` so `docker compose` receives your variables.

## 3) Run locally with Docker
Build and start the app:
```bash
make build && make up
```
Then open `http://localhost:8501`.

Handy commands:
```bash
make logs     # tail container logs
make sh       # open a shell in the running container
make down     # stop containers
```

### How the private key is handled locally
- Docker bind‑mounts your host key file into the container at `/run/secrets/rsa_key.p8` (read‑only). It isn’t copied into the repo or the image.
- The app reads the key at `/run/secrets/rsa_key.p8` and uses key‑pair auth.
- You may rotate keys by updating the file and the Snowflake user’s public key.

## 4) CI/CD with GitHub Actions
This project contains an example workflow at:
- `.github/workflows/streamlit_app_deploy.yml`

You will need to configure your GitHub repository:
- Set repository variables: `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_ROLE`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`
- Add a secret for your private key (for example, `SNOWFLAKE_PRIVATE_KEY`) and any passphrase (`SNOWFLAKE_PRIVATE_KEY_PASSPHRASE`)
- Adjust environments/branches to control where/when deploys occur

After configuration, pushes to the appropriate branch can trigger Snowflake app deployments via the workflow.

## 5) Adding Python libraries
When you add dependencies:
- Update `requirements.txt` for local Docker usage
- Update `app/environment.yml` for Streamlit in Snowflake

Keeping both files in sync ensures parity between local Docker and the Snowflake runtime.

## Troubleshooting
- If the app shows no Snowflake session, confirm the key file is available inside the container and that `.env` values are correct.
- Validate your user’s public key in Snowflake and role/warehouse/database permissions.
- Check container logs with `make logs` for stack traces.

---
Feel free to adapt this template to your organization’s standards (e.g., Docker secrets with Swarm, Vault/1Password injection, or tmpfs mounts with a bootstrap script).

