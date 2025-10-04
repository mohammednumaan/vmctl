"""
This module provides a function to create and display a table using the rich library.
"""
from rich.table import Table
from rich.console import Console
from utils.errors import VmctlError

def create_table(title, columns, rows):
    """
    Creates and displays a table using the rich library.

    Args:
        title (str): The title of the table.
        columns (list): A list of dictionaries, where each dictionary represents a column.
                        Each dictionary should have a "header" key and an optional "style" key.
        rows (list): A list of lists, where each inner list represents a row.
    """
    try:
        rich_table = Table(title=title)
        for column in columns:
            rich_table.add_column(column["header"], style=column.get("style", ""))

        for row in rows:
            rich_table.add_row(*row)

        console = Console()
        console.print(rich_table)
    except Exception as e:
        raise VmctlError(f"An unexpected error occurred while creating the table: {e}")