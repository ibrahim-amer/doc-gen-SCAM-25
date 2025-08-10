# 📚 Docstring Generation & Evaluation Platform

[![DOI](https://zenodo.org/badge/1034191475.svg)](https://doi.org/10.5281/zenodo.16786535)

This repository contains a complete pipeline for **automatic documentation generation** and **human evaluation** across multiple programming languages.

It is composed of two main components:

1. **📊 Survey Application** — A web-based platform to collect structured human feedback on generated docstrings.
2. **🛠️ Documentation Generation Tool** — A script-based system that uses LLMs to insert inline documentation into source code.

Together, they form an end-to-end research framework for studying and improving AI-generated code documentation.

---

## 📋 Table of Contents

- [📚 Docstring Generation \& Evaluation Platform](#-docstring-generation--evaluation-platform)
  - [📋 Table of Contents](#-table-of-contents)
  - [📖 About the Project](#-about-the-project)
  - [📂 Project Structure](#-project-structure)
  - [📊 Survey Application](#-survey-application)
  - [🛠️ Documentation Generation Tool](#️-documentation-generation-tool)
  - [🖥️ Tech Stack](#️-tech-stack)
  - [📜 License](#-license)
  - [Citation](#citation)

---

## 📖 About the Project

This project is designed to support research into **AI-assisted software documentation**.  
The workflow typically involves:

1. Using the **Documentation Generation Tool** to insert docstrings into source code files for supported programming languages.
2. Hosting the **Survey Application** to gather feedback from developers or study participants.
3. Analyzing the collected data to evaluate:
   - Correctness
   - Comprehensiveness
   - Clarity
   - Usefulness
4. Using results to refine prompt templates, model configurations, or generation strategies.

---

## 📂 Project Structure

```
.
├── survey-data-collection/          # The Survey Web Application
│   ├── README.md                     # Detailed setup and usage for survey app
│   └── src/ ...                      # Next.js frontend, MongoDB backend, Docker configs
│
├── documentation-folder/            # The Documentation Generation Tool
│   ├── README.md                     # Detailed setup and usage for doc gen tool
│   └── tinaa/doc_gen/ ...            # Core doc generation logic, LLM integration
│
├── LICENSE
└── README.md                         # (This file) Repository overview
```

---

## 📊 Survey Application

- **Purpose:** Collect structured human feedback on generated docstrings.
- **Tech:** Next.js, Tailwind CSS, MongoDB, Docker, Nginx.
- **Hosting Options:** Local Docker setup, remote deployment, or Cloudflare Tunnel for public access.
- **Details:** [Survey App README](survey-data-collection/README.md)

---

## 🛠️ Documentation Generation Tool

- **Purpose:** Generate inline documentation for code files using LLM APIs.
- **Supported Languages:** Python, Java, Makefiles, TypeScript, PHP, C++, and more.
- **Configurable LLM Providers:** OpenAI, Google Gemini (extendable via factory pattern).
- **Details:** [Doc Gen Tool README](documentation-generation/README.md)

---

## 🖥️ Tech Stack

| Component                  | Technology                                           |
|----------------------------|------------------------------------------------------|
| **Frontend (Survey)**      | Next.js, Tailwind CSS                                |
| **Backend (Survey)**       | Node.js (API routes), MongoDB                        |
| **Deployment**             | Docker, Docker Compose, Nginx                       |
| **LLM Integration**        | OpenAI API, Google Gemini API (extendable)           |
| **Language Parsing**       | Tree-sitter, Arpeggio                                |
| **Evaluation Metrics**     | Correctness, Comprehensiveness, Clarity, Usefulness  |

---

## 📜 License

This project is licensed under the **MIT License**.

---
## Citation
To cite this work please use this Bibtex entry
```
@misc{your_repo_name_2025,
  author       = {Nathanael Yao and Juergen Dingel and Ali Tizghadam and Ibrahim M. Amer},
  title        = {Language-Agnostic Generation of Header Comments using Large Language Models},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.xxxxxxx},
  url          = {https://doi.org/10.5281/zenodo.xxxxxxx}
}
```
---
