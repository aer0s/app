from .apt import APT
from .flatpak import FlatPak
from .pacman import Pacman
from .snap import Snap
from .spm import SPM
from .yay import Yay

__managers__ = [APT, FlatPak, Pacman, Snap, SPM, Yay]


def get_package_managers():
    pkms = {}
    unload = []
    for pkm in __managers__:
        manager = pkm()
        if manager.is_available:
            pkms[manager.name] = manager
        if manager.replaces:
            unload.extend(list(manager.replaces))
    for name in unload:
        del pkms[name]

    return pkms.values()
