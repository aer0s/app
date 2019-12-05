import click
import sh
from textwrap import wrap
from tabulate import tabulate
from importlib import import_module
from package_manager import get_package_managers


@click.command()
@click.argument("packages", nargs=-1)
@click.option("--sync", "-S", is_flag=True, help="Package sync flag")
@click.option("--remove", "-R", is_flag=True, help="Package sync flag")
@click.option("--info", "-i", is_flag=True, help="Package sync flag")
@click.option("--search", "-s", is_flag=True, help="Package search")
@click.option("--refresh", "-y", is_flag=True, help="Refresh package database")
@click.option("--upgrade", "-u", is_flag=True, help="Update installed packages")
@click.option("--noconfirm", is_flag=True, default=False, help="Accept questions")
@click.option(
    "--list-pkm", is_flag=True, default=False, help="List enabled package managers"
)
def main(packages, sync, remove, info, search, refresh, upgrade, noconfirm, list_pkm):
    # get package managers
    mgrs = get_package_managers()
    if list_pkm:
        for mgr in mgrs:
            print(mgr.name)
        exit()

    send_to_console = []
    for mgr in mgrs:
        if sync:
            if info:
                mgr.info(*packages)
            elif search:
                click.secho(f"Searching {mgr.name}..", nl=False)
                send_to_console.extend(mgr.search(" ".join(packages)))
                click.secho(f" [done]", fg="green")
            else:
                if refresh:
                    mgr.update(noconfirm)
                if upgrade:
                    mgr.upgrade(*packages, noconfirm=noconfirm)
                if packages:
                    mgr.install(*packages, noconfirm=noconfirm)
        elif remove:
            mgr.remove(*packages, noconfirm=noconfirm)

    if send_to_console:
        fields = ("name", "version", "description")
        formatted_data = [
            {f: "\n".join(wrap(r.get(f, ""), 30)) for f in fields}
            for r in send_to_console
        ]
        table = tabulate(formatted_data, headers="keys")
        print(table)


if __name__ == "__main__":
    main()
