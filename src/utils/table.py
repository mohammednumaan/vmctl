from rich.table import Table
from rich.console import Console


def create_table(title, columns, rows):
    rich_table = Table(title=title)
    for column in columns:
        rich_table.add_column(column["header"], style=column["style"])

    for row in rows:
        rich_table.add_row(*row)

    console = Console()
    console.print(rich_table)