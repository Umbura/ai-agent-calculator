"""
Tools Module

This module defines the specific tools that the AI Agent can access.
It currently includes:
1. Calculator: For safe mathematical evaluations.
2. Tavily Search: For real-time web information retrieval.
"""

import numexpr
import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_tavily import TavilySearch

# Load environment variables immediately to ensure API keys are available
load_dotenv()

# Validate Tavily API Key
if not os.getenv("TAVILY_API_KEY"):
    raise ValueError(
        "TAVILY_API_KEY not found in .env file. "
        "Please ensure you have a .env file in the root directory with TAVILY_API_KEY=tvly-..."
    )

# Initialize the Tavily Search Tool
try:
    # Using the correct class from the new 'langchain_tavily' package
    tavily_tool = TavilySearch(max_results=3)
except Exception as e:
    raise ValueError(f"Failed to initialize Tavily tool: {e}")

@tool
def calculator_tool(expression: str) -> str:
    """
    Performs precise mathematical calculations.
    Useful for answering questions involving numbers, arithmetic, sums, multiplications, etc.
    The input must be a pure mathematical expression, e.g., "128 * 46" or "20 + 5 / 2".
    """
    try:
        # Basic sanitization to prevent syntax errors
        safe_expression = expression.replace('^', '**').replace('x', '*')
        
        # Evaluate safely using numexpr (avoids eval() security risks)
        result = numexpr.evaluate(safe_expression)
        return str(result.item())
        
    except Exception as e:
        return f"Calculation error: {str(e)}"

# Export the list of available tools
TOOLS = [calculator_tool, tavily_tool]