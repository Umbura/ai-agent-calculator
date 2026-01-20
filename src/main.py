"""
Main Entry Point (CLI)

This script runs the AI Agent in a Command Line Interface (CLI) environment
using the 'rich' library for formatted output. It allows users to interact
with the agent directly from the terminal.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from src.agent import initialize_agent

# Initialize the rich console for pretty printing
console = Console()

def main() -> None:
    """
    Main loop for the CLI application.
    Initializes the agent and handles the user input/output loop.
    """
    # Application Header
    console.print(Panel.fit(
        "[bold blue]AI Agent Calculator[/bold blue]\n"
        "[italic]Technical Challenge - AI Engineer[/italic]",
        border_style="blue"
    ))

    # Agent Initialization
    try:
        agent = initialize_agent()
        console.print("[green]✔ Agent initialized successfully! (Model: Llama-3.3 via Groq)[/green]\n")
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        return

    console.print("Type [bold red]'exit'[/bold red] to quit.\n")

    # Interaction Loop
    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]")

        # Exit conditions
        if user_input.lower() in ["exit", "quit", "bye"]:
            console.print("[yellow]Shutting down... Goodbye![/yellow]")
            break

        # Skip empty inputs
        if not user_input.strip():
            continue

        console.print("\n[dim]🤖 Thinking... (Reasoning & Acting)[/dim]")
        
        try:
            # Invoking the agent
            response = agent.invoke({"input": user_input})
            
            # Extract output safely
            output = response.get("output", "No response generated.")
            
            # Pretty print the final response
            console.print(Panel(
                output,
                title="[bold green]Assistant[/bold green]",
                border_style="green"
            ))
            console.print("") # Spacing
            
        except Exception as e:
            console.print(f"[bold red]Execution Error:[/bold red] {e}")

if __name__ == "__main__":
    main()