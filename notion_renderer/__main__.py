# type: ignore[attr-defined]
from typing import Optional

from enum import Enum
from random import choice

import typer
from rich.console import Console

from notion_renderer import version
from notion_renderer.example import hello
from notion_renderer.notion_to_mdx import convert


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="notion_renderer",
    help="Awesome `notion_renderer` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]notion_renderer[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


def main():
    """Print a greeting with a giving name."""
    convert()


if __name__ == "__main__":
    app()
