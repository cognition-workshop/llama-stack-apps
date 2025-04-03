#
import os
import uuid
import fire
from termcolor import colored

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.lib.agents.react.agent import ReActAgent
from llama_stack_client.lib.agents.react.tool_parser import ReActOutput

from examples.client_tools.web_search import WebSearchTool

from .utils import check_model_is_available, get_any_available_model


def main(host: str, port: int, model_id: str | None = None):
    """
    Run a web search agent that combines reasoning with web search capabilities.
    
    Args:
        host: The host of the Llama Stack server
        port: The port of the Llama Stack server
        model_id: The model ID to use for the agent
    """
    client = LlamaStackClient(base_url=f"http://{host}:{port}")
    
    api_key = ""
    engine = "tavily"
    if "TAVILY_SEARCH_API_KEY" in os.environ:
        api_key = os.getenv("TAVILY_SEARCH_API_KEY")
        print(colored("Using Tavily Search API", "green"))
    elif "BRAVE_SEARCH_API_KEY" in os.environ:
        api_key = os.getenv("BRAVE_SEARCH_API_KEY")
        engine = "brave"
        print(colored("Using Brave Search API", "green"))
    else:
        print(
            colored(
                "Warning: TAVILY_SEARCH_API_KEY or BRAVE_SEARCH_API_KEY is not set; Web search will not work",
                "yellow",
            )
        )
    
    if model_id is None:
        model_id = get_any_available_model(client)
        if model_id is None:
            return
    else:
        if not check_model_is_available(client, model_id):
            return
    
    print(colored(f"Using model: {model_id}", "green"))
    
    web_search_tool = WebSearchTool(engine, api_key) if api_key else None
    
    agent = ReActAgent(
        client=client,
        model=model_id,
        instructions=(
            "You are a helpful AI assistant that can search the web to find information "
            "and answer questions. When answering questions, follow these steps:\n"
            "1. Break down complex questions into simpler sub-questions if needed\n"
            "2. Use web search to find relevant information\n"
            "3. Analyze and synthesize the information\n"
            "4. Provide a clear, concise answer with citations\n"
            "Always think step by step and explain your reasoning."
        ),
        tools=[web_search_tool] if web_search_tool else ["builtin::websearch"],
        response_format={
            "type": "json_schema",
            "json_schema": ReActOutput.model_json_schema(),
        },
    )
    
    session_id = agent.create_session(f"web-search-session-{uuid.uuid4().hex}")
    print(colored(f"Created session_id={session_id} for Agent({agent.agent_id})", "green"))
    
    example_queries = [
        "What is the capital of France?",  # Simple factual query
        "Who won the Nobel Prize in Physics in 2023?",  # Recent factual query
        "Compare the benefits of electric vehicles versus gasoline vehicles",  # Comparative analysis
        "What are the main causes of climate change and what solutions are being proposed?",  # Complex multi-part query
    ]
    
    for query in example_queries:
        print("\n" + "="*80)
        print(colored(f"User> {query}", "cyan"))
        
        response = agent.create_turn(
            messages=[{"role": "user", "content": query}],
            session_id=session_id,
            stream=True,
        )
        
        for log in EventLogger().log(response):
            log.print()
    
    print("\n" + "="*80)
    print(colored("Enter your questions (type 'exit' to quit):", "green"))
    
    while True:
        user_input = input(colored("User> ", "cyan"))
        if user_input.lower() == "exit":
            break
        
        response = agent.create_turn(
            messages=[{"role": "user", "content": user_input}],
            session_id=session_id,
            stream=True,
        )
        
        for log in EventLogger().log(response):
            log.print()


if __name__ == "__main__":
    fire.Fire(main)
