import unittest
from unittest.mock import patch
from ...processing.search import search_google, filter_links
import requests


class TestSearch(unittest.TestCase):
   
    @patch('processing.search.requests.get')
    def test_search_google_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = '<html><div class="yuRUbf"><a href="/url?q=http://example.com&sa=U"></a></div></html>'.encode('utf-8')
        data = {"search_cache": {}}
        links = search_google("test", data)
        self.assertEqual(links, ["http://example.com"])
    
    @patch('processing.search.requests.get')
    def test_search_google_no_links(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = '<html></html>'.encode('utf-8')
        data = {"search_cache": {}}
        links = search_google("test", data)
        self.assertEqual(links, [])
    
    @patch('processing.search.requests.get')
    def test_search_google_error(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.RequestException("Error")
        data = {"search_cache": {}}
        links = search_google("test", data)
        self.assertEqual(links, [])
    
    def test_filter_links(self):
        links = ["http://example.com", "https://youtube.com/watch", "http://test.com/pdf", "http://test.com/обучение", "http://test.com/python"]
        query = "python обучение"
        filtered_links = filter_links(links, query)
        self.assertIn("http://test.com/python", filtered_links)
        self.assertIn("http://test.com/обучение", filtered_links)
        self.assertNotIn("https://youtube.com/watch", filtered_links)
        self.assertNotIn("http://test.com/pdf", filtered_links)
        
if __name__ == '__main__':
    unittest.main()