# Web Browsing Agent 🌐

A simple Python agent that browses the web and summarizes content using Claude (Anthropic API) with tool use.

## Features

- Fetches and parses webpage content
- Uses Claude to reason, browse, and summarize
- Agentic loop with tool use (fetch_webpage)

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
python agent.py "Summarize the latest news on AI from https://news.ycombinator.com"
```

Or run interactively:

```bash
python agent.py
```

## How It Works

1. You give the agent a task (e.g. "summarize this URL")
2. Claude decides which URLs to fetch using the `fetch_webpage` tool
3. The agent loops until Claude has enough info to write a summary
