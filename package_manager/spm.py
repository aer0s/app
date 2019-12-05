from .base import ManagerBase


class SPM(ManagerBase):
    name = "spm"
    namespaces = ("spm",)

    def info(self, *pkgs):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        for pkg in packages:
            self.pkm.info(pkg)

    def install(self, *pkgs, noconfirm):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        for pkg in packages:
            if noconfirm:
                self.pkm.install(self.system.echo(1), pkg)
            else:
                self.pkm.install(pkg)

    def remove(self, *pkgs, noconfirm):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        for pkg in packages:
            if noconfirm:
                self.pkm.remove(self.system.echo(1), pkg)
            else:
                self.pkm.remove(pkg)

    def search(self, term):
        query = next(self.clear_namespace(term))
        out = []
        installed = self.pkm.list(installed=True, _tty_out=False)
        results = self.pkm.search(query, _tty_out=False).splitlines()[2:-1]
        if "No results for" in " ".join(results):
            results = []
        for pkgstr in results:
            try:
                pkg = {
                    "name": self.format_pkg(pkgmgr=self.name, pkg=pkgstr),
                    "description": "",
                    "version": "",
                    "installed": pkgstr in installed,
                    "repo": "GitHub",
                }
                out.append(pkg)
            except Exception as err:
                raise err

        return out

    def update(self, noconfirm):
        self.pkm.update()

    def upgrade(self, *pkgs, noconfirm):
        self.spm.update()
