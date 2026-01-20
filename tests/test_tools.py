"""
Unit Tests for Tools

This module validates the functionality, security, and integration
of the tools provided to the Agent (Calculator and Search).
"""

import pytest
from unittest.mock import patch, MagicMock
from src.tools import calculator_tool, TOOLS

# --- Calculator Tool Tests (Robustness & Security) ---

def test_calculator_basic_addition():
    """Test simple arithmetic operations."""
    result = calculator_tool.invoke("2 + 2")
    assert result == "4"

def test_calculator_complex_expression():
    """Test operator precedence and brackets."""
    result = calculator_tool.invoke("(2 + 2) * 10")
    assert result == "40"

def test_calculator_sanitization():
    """Test sanitization of colloquial math symbols."""
    # Replaces 'x' with '*' and '^' with '**'
    assert calculator_tool.invoke("10 x 5") == "50"
    assert calculator_tool.invoke("2^3") == "8"

def test_calculator_division_by_zero():
    """Test graceful handling of division by zero (must not crash)."""
    result = calculator_tool.invoke("10 / 0")
    # Numexpr may return 'inf' or an error string; both are acceptable safe outputs
    assert "error" in result.lower() or "inf" in result.lower()

def test_calculator_security_injection():
    """
    Security Test: Ensure users cannot execute arbitrary Python code.
    This confirms we are not using unsafe eval().
    """
    # Attempt to import a system library
    result = calculator_tool.invoke("import os")
    assert "error" in result.lower()

def test_calculator_empty_input():
    """Test handling of empty input strings."""
    result = calculator_tool.invoke("")
    assert "error" in result.lower()

def test_calculator_garbage_input():
    """Test handling of non-mathematical text input."""
    result = calculator_tool.invoke("Hello World")
    assert "error" in result.lower()

# --- Search Tool Tests ---

def test_search_tool_exists():
    """Verify tool configuration and loading."""
    assert len(TOOLS) == 2
    # Confirms the search tool is the second item and uses the official library name
    assert TOOLS[1].name == "tavily_search"

@patch("src.tools.tavily_tool._run")
def test_search_tool_execution(mock_search):
    """
    Test the execution logic of the search tool.
    Mocks the API call to avoid external network requests.
    """
    # LangChain expects a tuple (content, artifact) for this tool type
    fake_result = [{"url": "http://example.com", "content": "Bitcoin is $100k"}]
    mock_search.return_value = (fake_result, None) 
    
    search_tool = TOOLS[1]
    search_tool.invoke("Bitcoin price")
    
    mock_search.assert_called_once()