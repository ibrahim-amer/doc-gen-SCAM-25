<h3 align="center">Documentation Generation Tool</h3>

<p align="center">
  Prototype that uses LLM APIs to automatically insert inline code documentation into selected files or entire repositories.<br/>
  Supports documenting <strong>Python</strong>, <strong>Java</strong>, <strong>Art (Code Realtime)</strong>, <strong>Makefiles</strong>, <strong>TypeScript</strong>, <strong>PHP</strong>, and <strong>C++</strong>.
</p>

---

## 📋 Table of Contents
<details>
  <summary>Click to expand</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation-local-use">Installation (Local Use)</a></li>
    <li><a href="#installation-gitlab-ci">Installation (GitLab CI)</a></li>
    <li><a href="#setup">Setup</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#llm-as-judge-evaluation">LLM-as-Judge Evaluation</a></li>
    <li><a href="#key-files">Key Files</a></li>

  </ol>
</details>

---

<a id="about-the-project"></a>
## 📖 About The Project

This tool automatically generates inline code documentation for supported programming languages using a configurable LLM provider. It is designed for both <strong>local use</strong> and <strong>CI/CD integration</strong>.

The LLM provider, API credentials, and model settings are configured via <code>tinaa/doc_gen/config/config.yaml</code>. The app uses a <strong>dependency injection + factory pattern</strong> to instantiate the correct LLM implementation at runtime.

---

<a id="installation-local-use"></a>
## ⚙️ Installation (Local Use)

1. <strong>Get API Keys</strong><br/>
   You can use:
   - OpenAI API key — https://platform.openai.com/account/api-keys
   - Google Gemini API key — https://aistudio.google.com/app/apikey

2. <strong>Clone the Repository</strong>
   ```bash
   git clone https://github.com/ibrahim-amer/doc-gen-SCAM-25.git 
   cd documentation-generation
   ```

3. <strong>Configure <code>config.yaml</code></strong><br/>
   Location: <code>tinaa/doc_gen/config/config.yaml</code>

   ```yaml
   # See tinaa/doc_gen/config/LLMProvider.py for list of supported providers
   # You can extend providers by following LLMFactory.py + BaseLLM pattern

   LLM_PROVIDER: openai  # or gemini

   GEMINI:
     KEY: your-gemini-api-key
     MODEL: gemini-1.5-flash-latest
     TEMPERATURE: 0.3

   OPENAI:
     API_KEY: your-openai-api-key
     MODEL: gpt-4o
     TEMPERATURE: 0.3
   ```

   - <code>LLM_PROVIDER</code> selects which LLM implementation the factory returns.
   - Each provider supports its own <code>MODEL</code> and <code>TEMPERATURE</code> values.
   - To add a new provider, extend <code>LLMProvider</code>, implement a new <code>BaseLLM</code> subclass, and register it in <code>LLMFactory</code>.
   - Refer to <a href="#key-files">Key Files</a> section to change 

4. <strong>Install Dependencies</strong>
   ```bash
   poetry install
   ```

---

<a id="installation-gitlab-ci"></a>
## ⚙️ Installation (GitLab CI)

1. <strong>Enable Deploy Key</strong><br/>
   In GitLab repo settings, enable <code>public_deploy_key_nathanael</code> (or add your own deploy key and update configuration).

2. <strong>Set CI/CD Variables</strong><br/>
   - <code>MAINTAINER_KEY</code>
   - <code>DEPLOY_KEY</code>
   - <code>OPENAI_API_KEY</code> or <code>GEMINI_KEY</code>
   - <code>TOKEN</code>

3. <strong>Pipeline Trigger</strong><br/>
   - Runs when a new Merge Request is created or changes are pushed to an existing MR.

---

<a id="setup"></a>
## 🛠️ Setup (Add a New Language)

1. <strong>Language Info</strong><br/>
   Add your language in:
   ```
   tinaa/doc_gen/languages.json
   ```
   The language name must match a <a href="https://tree-sitter.github.io/tree-sitter/">Tree-sitter</a> parser.

2. <strong>Templates</strong><br/>
   Add a Jinja template (documentation format) in:
   ```
   tinaa/doc_gen/jinja_templates/language_doc_templates
   ```

3. <strong>No Tree-sitter Parser?</strong><br/>
   Define grammar rules and visitors in:
   ```
   tinaa/doc_gen/parsing/arpeg.py
   ```
   - Add Arpeggio grammars (see <code>images/python_grammars.png</code>)
   - Add visitor functions in the <code>Visitor</code> class (see <code>images/visitor_class.png</code>)

---

<a id="usage"></a>
## ▶️ Usage

Main script: <code>tinaa/doc_gen/add_documentation.py</code><br/>
Prompt templates: <code>tinaa/doc_gen/jinja_templates</code>

- Run on all files in the current directory:
  ```bash
  python3 -m tinaa.doc_gen.add_documentation -public
  ```

- Run on a specific file:
  ```bash
  python3 -m tinaa.doc_gen.add_documentation path/to/file.py -public
  ```

What happens:
1. <code>config.yaml</code> is loaded into a <code>Config</code> object.
2. <code>LLMFactory.from_config()</code> creates the provider (e.g., <code>OpenAILLM</code> / <code>GeminiLLM</code>) based on <code>LLM_PROVIDER</code>.
3. The selected LLM generates documentation using the appropriate Jinja template.
4. The script inserts inline comments/docstrings into your code.

---

<a id="llm-as-judge-evaluation"></a>
## 🧠 LLM-as-Judge Evaluation

Planned/optional: integrate an LLM-as-judge step to automatically rate generated documentation for <em>clarity</em>, <em>correctness</em>, and <em>completeness</em>.

---

<a id="key-files"></a>
## 📂 Key Files

- <code>tinaa/doc_gen/config/config.yaml</code> — LLM provider + credentials + model settings
- <code>tinaa/doc_gen/config/LLMProvider.py</code> — Enum of supported providers
- <code>tinaa/doc_gen/config/LLMFactory.py</code> — Factory that returns an <code>OpenAILLM</code> / <code>GeminiLLM</code> (or your own) by reading <code>LLM_PROVIDER</code>
- <code>tinaa/doc_gen/config/BaseLLM.py</code> — Base interface
- <code>tinaa/doc_gen/config/OpenAILLM.py</code> — OpenAI implementation
- <code>tinaa/doc_gen/config/GeminiLLM.py</code> — Gemini implementation
- <code>tinaa/doc_gen/add_documentation.py</code> — Main entry script
- <code>tinaa/doc_gen/jinja_templates/</code> — Prompt templates per language

---
