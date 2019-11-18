from .base import ManagerBase
import re


class Pacman(ManagerBase):
    """
    Pacman Package manager
    """
    namespaces = ('pacman',)

    def __init__(self, *args, **kwargs):
        self.pacman = getattr(self.system, 'pacman')
        self.sudo_pacman = getattr(getattr(self.system.contrib,'sudo'), 'pacman')

    def info(self, *pkgs):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_pacman(*packages, S=True, i=True, _fg=True)        

    def install(self, *pkgs, noconfirm):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_pacman(*packages, S=True, noconfirm=noconfirm, _fg=True)        

    def remove(self, *pkgs, noconfirm):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_pacman(*packages, R=True, noconfirm=noconfirm, _fg=True)

    def search(self, term):
        query = next(self.clear_namespace(term))
        out = []
        results = re.sub(r'\n\s{4}', ' ',
                         self.pacman(query, S=True, s=true, _tty_out=False),
                         0, re.MULTILINE)
        lines = results.split('\n')
        regex = re.compile(
            r"(?P<repo>^[^/]+)/(?P<name>[^\s]+)\s(?P<version>[^\s]+)"
            + r"(?P<installed>\s\[installed[^\]]{0,}\])?[\s]+(?P<description>.+)?"
        )
        for pkgstr in lines:
            try:
                pkg = regex.match(pkgstr)
                if pkg:
                    pkg = pkg.groupdict()
                    pkg['name'] = self.format_pkg(pkgmgr='pacman', pkg=pkg['name'])
                    pkg['installed'] = True if pkg.get('installed') else False
                    pkg['repo'] = pkg.get('repo', 'main').split(',').pop()
                    out.append(pkg)
            except Exception as err:
                raise err
        
        return out

    def update(self, noconfirm):
        self.sudo_pacman(S=True, y=True, noconfirm=noconfirm, _fg=True)

    def upgrade(self, *pkgs, noconfirm):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.sudo_pacman(S=True, u=True, *packages, noconfirm=noconfirm, _fg=True)

