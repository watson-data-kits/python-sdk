from watson_data_kits.travel import TravelKit

from unittest.mock import patch


class TestTravelKit(object):
    def setup_method(self):
        self.kit = TravelKit('api_key', 'url', '123')

    @patch('watson_data_kits.client.Client.request')
    def test_attractions(self, patched_request):
        params = {'location': '100,100'}
        self.kit.attractions(**params)
        patched_request.assert_called_with('attractions', **params)

    @patch('watson_data_kits.client.Client.request')
    def test_categories(self, patched_request):
        params = {'keyword': 'beach'}
        self.kit.categories(**params)
        patched_request.assert_called_with('categories', **params)

    @patch('watson_data_kits.client.Client.request')
    def test_countries(self, patched_request):
        params = {'name': 'Fiji'}
        self.kit.countries(**params)
        patched_request.assert_called_with('countries', **params)
