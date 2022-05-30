from dataclasses import dataclass, field
@dataclass
class GeoServerXAuth:
    username : str = 'admin'
    password : str = 'geoserver'
    url = 'http://127.0.0.1:8080/geoserver/rest/'

    def __post_init__(self):
        if not self.username and not self.password and not self.url:
            raise GeoServerXAuth(0, "Username, Password and URL is missing")
        elif not self.username:
            raise GeoServerXAuth(0, "Username is not missing")
        elif not self.password:
            raise GeoServerXAuth(0, "password is not missing")
        elif not self.url:
            raise GeoServerXAuth(0, "URL is not missing")
