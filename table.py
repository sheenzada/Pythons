from rich.table import Table
from rich.console import Console

console = Console()
table = Table(title="User Data")

table.add_column("ID" , justify = "right" , style = "cyan" , no_wrap = True)
table.add_column("Name" , style = "magneta")
table.add_column("Age" , style = "green" , justify = "right")

table.add_row("1" , "Inam" , "20")
table.add_row("2" , "Ikram" , "23")
table.add_row("3" , "Niamat" , "32")

console.print(table)
