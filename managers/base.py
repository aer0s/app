import re
import sh


class ManagerBase:
    """
    Package manager base class
    """
    system = sh
    namespaces = tuple()
    variants = tuple()

    def clear_namespace(self, *pkgs):
        ns = r'|'.join(
            [r'|'.join([rf"{n}\-{v}" for v in self.variants])
                for n in self.namespaces]
        )
        regex = re.compile(rf"({ns})/")
        for pkg in pkgs:
            yield regex.sub('', pkg)

    def info(self, *pkgs):
        pass

    def install(self, *pkgs, noconfirm):
        pass

    def remove(self, *pkgs, noconfirm):
        pass

    def search(self, term):
        pass

    def format_pkg(self, pkgmgr:str, pkg:str, variant:str=None):
        """
        #Params
        - pkgmgr:str
        - pkg: str
        - [variant:str]
        
        Returns a formatted string containg package manager, varriant, and package name
        """
        return f'{pkgmgr}-{variant}/{pkg}' if variant else f'{pkgmgr}/{pkg}'

    def parse_pkgs(self, *pkgs, just_names=False):
        """
        # Params
        - pkgs:List(str)
        - just_names:bool [False]

        Converts list of namespaced/pkgs into a list of dictionaries:

        [{'pkgmgr':str, 'variant':str, 'pkg':str}, ...]
        """
        rtn = []
        regex = re.compile(
            r"(?P<pkgmgr>^[a-z]+)-?(?P<variant>[a-z]+)\/(?P<pkg>.+)")
        for pkg in pkgs:
            match = regex.match(pkg)
            if match:
                matches = match.groupdict()
                if matches.get('pkgmgr') in self.namespaces:
                    rtn.append(matches if not just_names else matches.get('pkg'))
        return rtn

    def update(self, noconfirm):
        pass

    def upgrade(self, *pkgs, noconfirm):
        pass

