from .base import ManagerBase


class AppImage(ManagerBase):
    """
    AppImage Package manager
    """
    namespaces = ('appimg',)

    def info(self, *pkgs):
        pass

    def install(self, *pkgs, noconfirm):
        pass

    def remove(self, *pkgs, noconfirm):
        pass

    def search(self, term):
        pass

    def update(self, noconfirm):
        pass

    def upgrade(self, *pkgs, noconfirm):
        pass

