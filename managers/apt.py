import re
from .base import ManagerBase

class APT(ManagerBase):
    """
    APT package manager wrapper
    """
    namespaces = ('apt',)

    def __init__(self):
        # this seems a bit crazy, but pylint doesn't like sh!
        self.apt = getattr(self.system, 'apt')
        self.sudo_apt = getattr(getattr(self.system.contrib, 'sudo'), 'apt')

    def info(self, *pkgs):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.apt.show(*packages, _fg=True)

    def install(self, *pkgs, noconfirm=False):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_apt.install(
            *packages, y=noconfirm, _fg=True)

    def remove(self, *pkgs, noconfirm):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_apt.remove(
            *packages, y=noconfirm, _fg=True)

    def search(self, term):
        query = next(self.clear_namespace(term))
        out = []
        results = self.apt.search(query, _tty_out=False)
        lines = results.replace('Sorting...\nFull Text Search...\n', '').split('\n\n')
        regex = re.compile(
            r"(?P<name>^[^/]+)/(?P<repo>[^\s]+)\s(?P<version>[^\s]+)\s(?P<arch>[^\s]+)"
            + r"(?P<installed>\s\[installed[^\]]{0,}\])?[\n\s]+(?P<description>.+)?"
        )
        for pkgstr in lines:
            try:
                pkg = regex.match(pkgstr)
                if pkg:
                    pkg = pkg.groupdict()
                    pkg['name'] = self.format_pkg(pkgmgr='apt', pkg=pkg['name'])
                    pkg['installed'] = True if pkg.get('installed') else False
                    pkg['repo'] = pkg.get('repo', 'main').split(',').pop()
                    out.append(pkg)
            except Exception as err:
                raise err
        
        return out

    def update(self, noconfirm):
        self.sudo_apt.update(y=noconfirm, _fg=True)

    def upgrade(self, *pkgs, noconfirm):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_apt('full-upgrade',
            *packages, y=noconfirm, _fg=True)
