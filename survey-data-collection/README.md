
# 📊 Docstring Evaluation Survey Platform

This is a Dockerized survey web application for collecting structured human feedback on **AI-generated docstrings** across multiple programming languages. The platform supports research efforts to evaluate how well automatically generated documentation explains source code functionality.

---

## 🎯 Objective

This platform enables researchers to:

- Evaluate the quality of AI-generated docstrings.
- Collect human feedback on various dimensions such as correctness, clarity, and usefulness.
- Compare documentation quality across programming languages.
- Build datasets for training or improving docstring generation models.

---

## 🧪 Languages Supported

- Python
- Make
- C++
- Art / creative samples
- ➕ Easily extendable to more languages

---

## 🧠 Evaluation Metrics

Participants assess each generated docstring based on the following criteria:

| Metric              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **Correctness**     | Is the docstring factually accurate and consistent with the code logic?     |
| **Comprehensiveness** | Does it fully capture the purpose and functionality of the code?            |
| **Clarity**         | Is the language clear, grammatically correct, and easy to understand?       |
| **Usefulness**      | Would this docstring be helpful to a future developer reading the code?     |

---

## ⚙️ Technologies Used

- **Frontend**: Next.js + Tailwind CSS
- **Backend**: Node.js (App API) via Next.js
- **Database**: MongoDB
- **Deployment**: Docker & Docker Compose
- **Reverse Proxy**: Nginx

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository


### 2️⃣ Configure Environment Variables

Copy the environment example file and provide real values:

```bash
cp env.example .env
```

Update the following fields in `.env`:

```env
TUNNEL_TOKEN=
MONGO_INITDB_ROOT_USERNAME=
MONGO_INITDB_ROOT_PASSWORD=
MONGO_EXPRESS_USER=
MONGO_EXPRESS_PASSWORD=
MONGO_DB_PORT=
```

These values configure MongoDB and the optional tunnel.

### 3️⃣ Run the App Using Makefile

This project provides simple Docker automation via `make`.

```bash
# Start the services (frontend, backend, database)
make up

# Stop all services
make down

# Rebuild frontend without cache
make rebuild

# Restart the stack
make restart
```

> The app will be available at: **http://localhost:3000**

---

## 🗂️ Project Structure

```
survey-data-collection/
├── src/
│   ├── app/                # Next.js pages and routing
│   ├── components/         # UI components (header, form controls, etc.)
│   ├── questionnaireData/  # JSON configs, code files, intros for each language
│   ├── hooks/, lib/, ai/   # Utility logic and data fetching
│   └── types.ts            # Shared TypeScript definitions
├── public/                 # Static assets
├── nginx/                  # Nginx configuration
├── Dockerfile              # App container definition
├── docker-compose.yml      # Service composition (app, DB, express, tunnel)
├── makefile                # Simplified Docker commands
├── env.example             # Template for environment variables
└── README.md               # You're here!
```

---

## 📊 Data Format

All survey questions and code snippets live under:  
**`src/questionnaireData/`**

Each language folder includes:

- `*.json`: Metadata and structure for the questionnaire
- `*.py`, `*.cpp`, etc.: Code snippets to evaluate
- `intros/*.html`: Introductory HTML for survey participants

Example (Python):

```
questionnaireData/
├── python/
│   ├── python.json         # Questions and snippet mappings
│   ├── q3_5.py             # Code file
│   └── intro.html          # Displayed before the section begins
```

---

## ☁️ Hosting with Cloudflare

This project can be securely exposed to the internet using **Cloudflare Tunnel** or deployed behind **Cloudflare** as a reverse proxy.

### 🔐 Option 1: Cloudflare Tunnel (Docker-based)

This project supports `cloudflared` as a Docker container for tunneling to Cloudflare without exposing ports.

1. Add the `cloudflared` service to your `docker-compose.yml` (already included if using provided setup).

2. Set the tunnel token in your `.env`:

```env
TUNNEL_TOKEN=your-cloudflare-tunnel-token
```

3. The `cloudflared` container will start with the stack via:

```bash
make up
```


> You must create the tunnel and token via the Cloudflare dashboard and copy it into the `.env` file.

---

### 🚀 Option 2: Cloudflare Proxy with Custom Domain

If you’re running the app on a public server:

1. Point your domain (e.g., `survey.example.com`) to your server using Cloudflare DNS.
2. Configure the Nginx proxy (`nginx/default.conf`) to serve the app.
3. Enable SSL in the Cloudflare dashboard (Full or Full (Strict) mode recommended).
4. Optionally, enable WAF, bot protection, and rate limiting.

---

## 📜 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

## 🧠 Acknowledgements

Developed as part of a research study on **automatic documentation generation**.  
Supported by the **MASE Lab** at Queen's University, Canada in collaboration with Telus, Canada.

---
