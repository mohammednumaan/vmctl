import typer
from rich import print

import wrapper.host as host_api
import wrapper.libvirt as libvirt_api

VMCTL_BANNER = r"""
                      _   _ 
__   ___ __ ___   ___| |_| |
\ \ / / '_ ` _ \ / __| __| |
 \ V /| | | | | | (__| |_| |
  \_/ |_| |_| |_|\___|\__|_|

"""
app = typer.Typer(no_args_is_help=True)


@app.command()
def idk():
    print("hi")

# the body definition is temporary, will need to change it
# i was just playing around with typer and rich
@app.command()
def hostname():
    libvirt = libvirt_api.LibVirtApi()
    
    print("Hostname: ", libvirt.host_api.get_hostname())
    print("Max vCPU's: ", libvirt.host_api.get_max_vCpus())

@app.command()
def hostinfo():
    libvirt = libvirt_api.LibVirtApi()
    libvirt.host_api.get_info()
    
if __name__ == "__main__":
    print(VMCTL_BANNER)
    print("""[bold blue]A simple CLI tool to manage VM's using the LibVirt API.[/bold blue]
To get started, type any of the commands vmctl supports.
If you are new, type [green]help[/green] (or) [green]--help[/green] to learn more about [bold blue]vmctl[/bold blue] and what it offers.
""")
    app()
