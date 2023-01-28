from dataclasses import dataclass, field

from geoserverx.utils.errors import GeoServerXError


@dataclass
class GeoServerXAuth:
    username: str = "admin"
    password: str = "geoserver"
    url = "http://127.0.0.1:8080/geoserver/rest/"

    def __post_init__(self):
        if not self.username and not self.password and not self.url:
            raise GeoServerXError(0, "Username, Password and URL is missing")
        elif not self.username:
            raise GeoServerXError(0, "Username is missing")
        elif not self.password:
            raise GeoServerXError(0, "password is missing")
        elif not self.url:
            raise GeoServerXError(0, "URL is missing")
