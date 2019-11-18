import click
import sh
from tabulate import tabulate
from importlib import import_module

@click.command()
@click.argument('packages', nargs=-1)
@click.option('--sync', '-S', is_flag=True, help='Package sync flag')
@click.option('--remove', '-R', is_flag=True, help='Package sync flag')
@click.option('--info', '-i', is_flag=True, help='Package sync flag')
@click.option('--search', '-s', is_flag=True, help='Package search')
@click.option('--refresh', '-y', is_flag=True, help='Refresh package database')
@click.option('--upgrade', '-u', is_flag=True, help='Update installed packages')
@click.option('--noconfirm', is_flag=True, default=False, help="Accept questions")
def main(packages, sync, remove, info, search, refresh, upgrade, noconfirm):
    # get package managers
    mgrs = []
    if sh.which('apt'):
        mgrs.append(getattr(import_module('managers.apt'), 'APT')())
    if sh.which('snap'):
        mgrs.append(getattr(import_module('managers.snap'), 'Snap')())

    send_to_console = []
    for mgr in mgrs:
        if sync:
            if info:
                mgr.info(*packages)
            elif search:
                send_to_console.extend(mgr.search(' '.join(packages)))
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
        fields = ('name', 'version', 'description')
        print(tabulate(
            [{k: v for k, v in r.items() if k in fields} for r in send_to_console],
            headers="keys"))


if __name__ == '__main__':
    main()
