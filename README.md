# AI-agent

A lightweight and extensible Python-based autonomous agent framework. This project offers a modular structure to develop, test, and extend tool-using AI agents, designed for experimentation and practical integration.

## 🚀 Features

- Modular agent framework
- Built-in tool invocation
- Extendable tool architecture
- Simple configuration
- Minimal dependencies

## 📦 Installation

```bash
git clone https://github.com/kzxjg/AI-agent.git
cd AI-agent
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> If no `requirements.txt` is present, install manually using:
> ```bash
> pip install openai
> ```

## ⚙️ Configuration

All configuration settings are in `config.py`. Update model names, keys, or behavior settings as needed.

Example settings:
- `OPENAI_API_KEY`: your OpenAI key
- `MODEL`: model name (e.g., `gpt-4`)
- `TOOLS`: list of enabled tools

## 🧠 Usage

Run the agent with:

```bash
python main.py
```

The agent will:
1. Accept user input
2. Process it via the LLM
3. Optionally invoke a tool
4. Return the final result

Example:

```bash
> What is 25 * 4?
Using calculator tool...
Answer: 100
```

## 🛠️ Tools

Tools are defined in the `functions/` directory. Example tools:
- `calculator`: simple math operations
- `weather`: (add your own API-based tool)

You can add new tools by:
1. Creating a Python function
2. Registering it in `config.py`

## 📂 Project Structure

```
AI-agent/
├── calculator/           # Tool-specific modules
├── functions/            # General tool functions
├── config.py             # Configuration
├── main.py               # Entry point
├── tests.py              # Basic test cases
└── pyproject.toml        # Project metadata
```

## 🧪 Running Tests

Run the included tests with:

```bash
python tests.py
```

## 🔮 Roadmap Ideas

- Add memory/context persistence
- Implement agent feedback loop
- Enhance logging and monitoring
- Integrate with external APIs

## 📄 License

Specify your license here (e.g., MIT, Apache 2.0).

---

> 📌 Repo: [github.com/kzxjg/AI-agent](https://github.com/kzxjg/AI-agent)
