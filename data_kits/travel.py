from .client import Client


class TravelKit(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(kit='travel', *args, **kwargs)

    def attractions(self, **params):
        return self.request('attractions', **params)

    def categories(self, **params):
        return self.request('categories', **params)

    def countries(self, **params):
        return self.request('countries', **params)
