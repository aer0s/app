from .base import ManagerBase


class FlatPak(ManagerBase):
    """
    FlatPak Package manager
    """

    name = "flatpak"
    namespaces = ("flathub",)

    def info(self, *pkgs):
        self.pkm.info(*pkgs, _fg=True)

    def install(self, *pkgs, noconfirm):
        for pkg in pkgs:
            for package in self.search(pkg):
                self.pkm.install(package["name"], package["app_id"])

    def remove(self, *pkgs, noconfirm):
        for pkg in pkgs:
            for package in self.search(pkg):
                self.pkm.uninstall(package["app_id"])

    def search(self, term):
        query = next(self.clear_namespace(term))
        results = self.pkm.search(query, _tty_out=False)
        out = []
        if "No matches found" in results:
            return out

        fields = ["name", "description", "app_id", "version", "channel", "repo"]
        for pkgstr in results.splitlines():
            if pkgstr:
                pkg = dict(zip(fields, pkgstr.split("\t")))
                pkg.update(
                    {
                        "name": self.format_pkg(pkgmgr=self.name, pkg=pkg["name"]),
                        "installed": None,
                    }
                )
                out.append(pkg)
        return out

    def upgrade(self, *pkgs, noconfirm):
        self.pkm.update()
        self.pkm.uninstall(unused=True)
