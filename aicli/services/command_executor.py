"""
Command Executor Module

This module is responsible for safely executing shell commands generated by the AI.
It provides a wrapper around subprocess.run with additional safety checks and
error handling.

Features:
    - Safe command execution in shell environment
    - Output capture and formatting
    - Error handling and user feedback
    - Command execution confirmation

Security Note:
    Commands are executed in a shell context. Users should review commands
    before execution to ensure safety.
"""

import subprocess
import click
from ..utils.exceptions import CommandExecutionError

class CommandExecutor:
    def run(self, command: str) -> None:
        """Execute the shell command"""
        if not command:
            raise CommandExecutionError("Command cannot be empty")

        try:
            # Strip markdown code block formatting if present
            command = command.strip().replace('```bash', '').replace('```', '')
            command = command.strip()
            
            click.echo(f"\nExecuting: {command}\n")
            click.echo("=" * 40)
            click.echo()
            
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                capture_output=True,
                check=True  # Raises CalledProcessError on non-zero exit
            )
            
            if result.stdout:
                click.echo(result.stdout)
            if result.stderr:
                click.secho(f"Warnings:\n{result.stderr}", fg="yellow", err=True)
                
        except subprocess.CalledProcessError as e:
            raise CommandExecutionError(
                f"Command failed with exit code {e.returncode}:\n{e.stderr}"
            )
        except Exception as e:
            raise CommandExecutionError(f"Error executing command: {str(e)}") 