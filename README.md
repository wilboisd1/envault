# envault

> A CLI tool to securely store and inject environment variables per project using encrypted local vaults.

---

## Installation

```bash
pip install envault
```

Or install from source:

```bash
git clone https://github.com/yourname/envault.git && cd envault && pip install .
```

---

## Usage

**Initialize a vault for your project:**
```bash
envault init
```

**Add a secret:**
```bash
envault set DATABASE_URL "postgres://user:pass@localhost/db"
```

**Inject variables into a command:**
```bash
envault run -- python app.py
```

**List stored keys:**
```bash
envault list
```

**Remove a variable:**
```bash
envault unset DATABASE_URL
```

Vaults are encrypted using AES-256 and stored locally at `.envault/vault.enc`. A master password is required on first use and cached securely via your OS keyring.

---

## How It Works

1. Run `envault init` inside any project directory.
2. Store secrets with `envault set KEY VALUE`.
3. Use `envault run -- <command>` to spawn processes with secrets automatically injected as environment variables.

No secrets are ever written to `.env` files or committed to version control.

---

## License

MIT © 2024 [yourname](https://github.com/yourname)