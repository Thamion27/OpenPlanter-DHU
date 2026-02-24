# DHU TUI Banner for OpenPlanter-DHU
# DigitalHermetica Studios

DHU_BANNER = '''
[bold cyan]
  ██████╗ ██╗  ██╗██╗   ██╗
  ██╔══██╗██║  ██║██║   ██║
  ██║  ██║███████║██║   ██║
  ██║  ██║██╔══██║██║   ██║
  ██████╔╝██║  ██║╚██████╔╝
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝
  DigitalHermetica Investigations
  Recursive AI Investigation Agent
[/bold cyan]
'''

def get_dhu_banner(compact=False):
    if compact:
        return '[bold cyan]=== DHU Planter ===[/bold cyan] [dim]DigitalHermetica Investigations[/dim]'
    return DHU_BANNER

def get_status_line(provider, model, reasoning, mode):
    return (
        f'[bold green]Provider[/bold green]  {provider}\n'
        f'[bold green]   Model[/bold green]  {model}\n'
        f'[bold green]Reasoning[/bold green]  {reasoning}\n'
        f'[bold green]    Mode[/bold green]  {mode}\n'
        f'[bold green]Division[/bold green]  [cyan]DHU Investigations[/cyan]\n'
    )
