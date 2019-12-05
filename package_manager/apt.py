import re
from .base import ManagerBase


class APT(ManagerBase):
    """
    APT package manager wrapper
    """

    name = "apt"
    namespaces = ("apt",)

    def info(self, *pkgs):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.pkm.show(*packages, _fg=True)

    def install(self, *pkgs, noconfirm=False):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_pkm.install(*packages, y=noconfirm, _fg=True)

    def remove(self, *pkgs, noconfirm):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_pkm.remove(*packages, y=noconfirm, _fg=True)

    def search(self, term):
        query = next(self.clear_namespace(term))
        out = []
        results = self.pkm.search(query, _tty_out=False)
        lines = results.replace("Sorting...\nFull Text Search...\n", "").split("\n\n")
        regex = re.compile(
            r"(?P<name>^[^/]+)/(?P<repo>[^\s]+)\s(?P<version>[^\s]+)\s(?P<arch>[^\s]+)"
            + r"(?P<installed>\s\[installed[^\]]{0,}\])?[\n\s]+(?P<description>.+)?"
        )
        for pkgstr in lines:
            try:
                pkg = regex.match(pkgstr)
                if pkg:
                    pkg = pkg.groupdict()
                    pkg["name"] = self.format_pkg(pkgmgr=self.name, pkg=pkg["name"])
                    pkg["installed"] = True if pkg.get("installed") else False
                    pkg["repo"] = pkg.get("repo", "main").split(",").pop()
                    out.append(pkg)
            except Exception as err:
                raise err

        return out

    def update(self, noconfirm):
        self.sudo_pkm.update(y=noconfirm, _fg=True)

    def upgrade(self, *pkgs, noconfirm):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_pkm("full-upgrade", *packages, y=noconfirm, _fg=True)
