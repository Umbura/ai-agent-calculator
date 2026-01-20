"""
Agent Initialization Module

This module sets up the LangChain agent using the ReAct (Reasoning + Acting) architecture.
It configures the LLM (Groq/Llama-3), loads the tools, and defines the system prompt.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from src.tools import TOOLS

load_dotenv()

def initialize_agent() -> AgentExecutor:
    """
    Initializes the agent using the ReAct pattern.
    
    Returns:
        AgentExecutor: The configured agent runtime ready to process queries.
    
    Raises:
        ValueError: If GROQ_API_KEY is missing.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file.")

    # Model Configuration
    # Llama 3.3 70B is selected for its high reasoning capabilities and low latency on Groq.
    llm = ChatGroq(
        temperature=0, 
        model_name="llama-3.3-70b-versatile",
        api_key=api_key
    )

    # ReAct Prompt Template
    # Includes specific DECISION RULES to prevent loops on general chat 
    # and strictly enforce tool usage for math/search.
    template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

### DECISION RULES (FOLLOW STRICTLY):
1. IF the question involves math/numbers -> USE [calculator_tool].
2. IF the question involves real-time info, prices, news -> USE [tavily_search].
3. IF the question is general chat, greetings ("hi", "hello") or knowledge you already have -> DO NOT USE TOOLS. Go straight to "Final Answer".

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

⚠️ IMPORTANT:
- If you do not need a tool, DO NOT write "Action: None". 
- Instead, just write "Thought: I can answer this directly." followed immediately by "Final Answer: [your response]".

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)

    # Agent Construction
    agent = create_react_agent(llm, TOOLS, prompt)

    # Agent Executor Configuration
    # verbose=True is critical for the evaluator to see the "Thought" process.
    agent_executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True, 
        handle_parsing_errors=True,
        max_iterations=5
    )

    return agent_executor