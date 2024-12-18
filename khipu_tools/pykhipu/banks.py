from .responses import BanksResponse


class Banks:
    ENDPOINT = "/banks"

    def __init__(self, client):
        self.client = client

    def get(self):
        response = self.client.make_request("GET", self.ENDPOINT)
        return BanksResponse.from_response(response)
