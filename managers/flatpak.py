from .base import ManagerBase


class FlatPak(ManagerBase):
    """
    FlatPak Package manager
    =======================
    Two approches for finding packages
     - flatpak cli
     - flathub REST api

    Flathub's rest api is basic, slow, and limited in scope.
     - Make cache of flathub apps for search and reference
     - Refresh cache frequently

    ## REST API [base_url](https://flathub.org/api/v1/apps)
    Endpoints are not published, but this is what I've found.
    All return `application/json;charset=UTF-8` and list endpoints
    return a list, while retrieve returns a single dict.
        - List all apps
            `GET {base_url}`
        - Retrieve details of single app 
            `GET {base_url}/{app_id}`
        - List all apps in a category
            `GET {base_url}/category/{category_name}`
        - List all NEW apps
            `GET {base_url}/collection/new`
        - List all POPULAR apps
            `GET {base_url}/collection/popular`
        - List all Recently Updated apps
            `GET {base_url}/collection/recently-updated`
    """
    namespaces = ('flathub',)

    
    def __init__(self, *args, **kwargs):
        self.flatpak = getattr(self.system, 'flatpak')

    def info(self, *pkgs):
        self.flatpak.info(*pkgs, _fg=True)

    def install(self, *pkgs, noconfirm):
        for pkg in pkgs:
            self.flatpak.install(pkg["name"], pkg["flatpakAppId"])

    def remove(self, *pkgs, noconfirm):
        pass

    def search(self, term):
        pass

    def update(self, noconfirm):
        pass

    def upgrade(self, *pkgs, noconfirm):
        pass

