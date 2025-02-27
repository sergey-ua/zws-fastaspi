import urllib.parse

from zws.database.repositories.blocked_hostnames_repo import BlockedHostnamesRepository


class BlockedHostnamesService:
    def __init__(self, blocked_hostnames_repo: BlockedHostnamesRepository):
        self.blocked_hostnames_repo = blocked_hostnames_repo

    def is_url_blocked(self, url: str) -> bool:
        hostname = urllib.parse.urlparse(url).hostname
        if not hostname:
            return False
        blocked_hostnames = self.blocked_hostnames_repo.get_all_blocked_hostnames()
        return any(blocked.hostname == hostname for blocked in blocked_hostnames)