import json
import socket
from pathlib import Path
from urllib.parse import urlencode, quote
from http.client import HTTPResponse
from .base import ManagerBase


class Snap(ManagerBase):
    """
    Snap package manager wrapper
    """
    namespaces = ('snap',)
    variants = ('stable', 'candidate', 'beta', 'edge')
    snapd = '/run/snapd.socket'

    def __init__(self):
        # this seems a bit crazy, but pylint doesn't like sh!
        self.snap = getattr(getattr(self.system.contrib, 'sudo'), 'snap')

    def http(self, verb, endpoint, **params):
        if Path(self.snapd).exists():
            uri = f"{endpoint}?{urlencode(params)}" if params else endpoint
            host = socket.gethostname()
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(self.snapd)
                s.sendall(f"{verb.upper()} {uri} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
                response = HTTPResponse(s)
                response.begin()
                return json.loads(response.read())
        else:
            return False

    def info(self, *pkgs):
        packages = self.parse_pkgs(*pkgs, just_names=True)
        self.snap.info(*packages)

    def install(self, *pkgs, noconfirm=False):
        for pkg in self.parse_pkgs(*pkgs):
            # Get the details on the package befor we try to install it
            detail = self.http('GET', '/v2/find', name=pkg["pkg"])
            if detail and detail['status-code'] == 200:
                pkg_detail = detail.get('result', [{}]).pop()
                self.snap.install(
                    pkg["pkg"], channel=pkg.get("variant", "stable"),
                    classic=bool(pkg_detail.get('confinement', False)),
                    _fg=True)

    def remove(self, *pkgs, noconfirm):
        for pkg in self.parse_pkgs(*pkgs):
            self.snap.remove(
                pkg["pkg"], channel=pkg.get("variant", "stable"),
                _fg=True)

    def search(self, term):
        query = next(self.clear_namespace(term))
        out = []
        qs = self.http('GET', '/v2/find', q=query)
        if qs and qs['status-code'] == 200:
            for row in qs.get('result', []):
                out.append({
                    'name': self.format_pkg(
                        pkgmgr='snap', variant=row['channel'], pkg=row['name']),
                    'description': row['title'],
                    'version': row['version']
                })

        return out

    def upgrade(self, *pkgs, noconfirm):
        for pkg in self.parse_pkgs(*pkgs):
            self.snap.refresh(
                pkg["pkg"], channel=pkg.get("variant", "stable"),
                _fg=True)
