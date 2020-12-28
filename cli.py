import argparse
import json
from textwrap import wrap
from tabulate import tabulate
from importlib import import_module
from package_manager import get_package_managers
from package_manager.utils import secho
from typing import List


def run_manager(
    packages: List[str],
    sync: bool = False,
    remove: bool = False,
    info: bool = False,
    search: bool = False,
    refresh: bool = False,
    upgrade: bool = False,
    noconfirm: bool = False,
    list_pkm: bool = False,
    tty=True,
) -> str:
    # get package managers
    managers = get_package_managers()
    if list_pkm:
        for mgr in managers:
            print(mgr.name)
        exit()

    send_to_console = []
    for mgr in managers:
        if sync:
            if info:
                mgr.info(*packages)
            elif search:
                secho(f"Searching {mgr.name}..", nl=False)
                send_to_console.extend(mgr.search(" ".join(packages)))
                secho(f" [done]", fg="green")
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
        if tty:
            formatted_data = [
                {f: "\n".join(wrap(r.get(f, ""), 30)) for f in fields}
                for r in send_to_console
            ]
            table = tabulate(formatted_data, headers="keys")
            print(table)
        else:
            return json.dumps({"fields": fields, "data": send_to_console})

    return "Done"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Application Package-management Proxy (APP)"
    )
    parser.add_argument(
        "--sync", "-S", action="store_true", dest="sync", help="Package sync flag"
    )
    parser.add_argument(
        "--remove", "-R", action="store_true", dest="remove", help="Package sync flag"
    )
    parser.add_argument(
        "--info", "-i", action="store_true", dest="info", help="Package sync flag"
    )
    parser.add_argument(
        "--search", "-s", action="store_true", dest="search", help="Package search"
    )
    parser.add_argument(
        "--refresh",
        "-y",
        action="store_true",
        dest="refresh",
        help="Refresh package database",
    )
    parser.add_argument(
        "--upgrade",
        "-u",
        action="store_true",
        dest="upgrade",
        help="Update installed packages",
    )
    parser.add_argument(
        "--noconfirm",
        "-Y",
        action="store_true",
        dest="noconfirm",
        help="Accept questions",
    )
    parser.add_argument(
        "--list-pkm",
        action="store_true",
        dest="list",
        help="List enabled package managers",
    )
    parser.add_argument(
        "packages", metavar="PKG", type=str, nargs="?", default=[],
        help="Package name(s)"
    )
    parser.set_defaults(noconfirm=False, list=False)

    args = parser.parse_args()
    run_manager(
        packages=args.packages,
        sync=args.sync,
        remove=args.remove,
        info=args.info,
        search=args.search,
        refresh=args.refresh,
        upgrade=args.upgrade,
        noconfirm=args.noconfirm,
        list_pkm=args.list,
    )
