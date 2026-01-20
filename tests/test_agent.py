"""
Unit Tests for Agent

This module tests the agent initialization process, environment validation,
and static analysis of the System Prompt (Prompt Engineering).
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from src.agent import initialize_agent

def test_initialize_agent_missing_api_key():
    """Test if ValueError is raised when GROQ_API_KEY is missing from environment."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GROQ_API_KEY not found"):
            initialize_agent()

@patch("src.agent.ChatGroq") 
@patch("src.agent.create_react_agent") 
@patch("src.agent.AgentExecutor") 
def test_initialize_agent_success(mock_executor, mock_create_agent, mock_llm):
    """Test if the agent initializes all components correctly with a valid key."""
    
    with patch.dict(os.environ, {"GROQ_API_KEY": "fake_key_123"}):
        executor = initialize_agent()
        
        # 1. Verify LLM Initialization
        mock_llm.assert_called_once()
        assert mock_llm.call_args[1]["model_name"] == "llama-3.3-70b-versatile"
        
        # 2. Verify Agent Creation
        mock_create_agent.assert_called_once()
        
        # 3. Verify Executor Creation
        assert executor is not None

@patch("src.agent.ChatGroq") 
@patch("src.agent.create_react_agent") 
@patch("src.agent.AgentExecutor") 
def test_agent_prompt_engineering(mock_executor, mock_create_agent, mock_llm):
    """
    Prompt Engineering Test:
    Static analysis of the PromptTemplate passed to the agent.
    Ensures that critical rules and guardrails are present in the system instructions.
    """
    with patch.dict(os.environ, {"GROQ_API_KEY": "fake_key_123"}):
        initialize_agent()
        
        # Inspect arguments passed to create_react_agent(llm, tools, prompt)
        call_args = mock_create_agent.call_args
        # The prompt object is the 3rd argument (index 2)
        prompt_passed = call_args[0][2] 
        
        # Get the raw template string
        template_text = prompt_passed.template
        
        # --- Critical Safety Check (Fix for 'Action: None' loop) ---
        assert 'DO NOT write "Action: None"' in template_text
        
        # --- Logic Routing Checks ---
        assert "IF the question involves math" in template_text
        assert "IF the question involves real-time info" in template_text
        
        # --- Tool Definition Checks ---
        assert "calculator_tool" in template_text
        assert "tavily_search" in template_text