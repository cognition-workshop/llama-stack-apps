# Web Search Agent

This example demonstrates a simple AI agent that combines web search capabilities with reasoning to answer questions. The agent can:

1. Break down complex questions into simpler sub-questions
2. Use web search to find relevant information
3. Analyze and synthesize the information
4. Provide clear, concise answers with citations

## Features

- **Reasoning Capabilities**: Uses the ReActAgent framework to implement step-by-step reasoning
- **Web Search Integration**: Leverages either Tavily or Brave search APIs to find information
- **Structured Output**: Provides structured responses with thoughts and actions
- **Interactive Mode**: Allows users to ask questions interactively

## Prerequisites

Before running the agent, you need to:

1. Set up a Llama Stack server
2. Set one of the following environment variables for web search:
   - `TAVILY_SEARCH_API_KEY` for Tavily search
   - `BRAVE_SEARCH_API_KEY` for Brave search

## Usage

Run the agent with:

```bash
python -m examples.agents.web_search_agent localhost 8321
```

Where:
- `localhost` is the host of your Llama Stack server
- `8321` is the port of your Llama Stack server

## Example Queries

The agent comes with example queries to demonstrate different capabilities:

1. Simple factual query: "What is the capital of France?"
2. Recent factual query: "Who won the Nobel Prize in Physics in 2023?"
3. Comparative analysis: "Compare the benefits of electric vehicles versus gasoline vehicles"
4. Complex multi-part query: "What are the main causes of climate change and what solutions are being proposed?"

After running the example queries, you can enter your own questions in interactive mode.

## How It Works

The agent uses:
- `ReActAgent` from Llama Stack for structured reasoning
- `WebSearchTool` for web search capabilities
- Custom instructions to guide the agent's reasoning process

When a query is received, the agent:
1. Analyzes the query and determines if web search is needed
2. Performs web searches to gather relevant information
3. Processes the search results and formulates a response
4. Provides a structured answer with its reasoning process

## Customization

You can customize the agent by:
- Modifying the instructions to change the agent's behavior
- Adding additional tools to extend its capabilities
- Adjusting the example queries to demonstrate different use cases
