import unittest
from backend.src.services.monitor.core.monitor import Monitor
from backend.src.services.database.core.database_mock import DatabaseMock
from backend.src.services.monitor.models.url import URL

class TestMonitor(unittest.TestCase):
    """Test class for monitor features"""
    def setUp(self) -> None:
        urls = [URL(url="www.google.com"), URL(url="www.uxinnovation.com.br"), URL(url="caguei")]
        self.monitor = Monitor(urls, DatabaseMock(), {})
        super().setUp()


    def test_monitor_url(self):
        """Basic unit test to monitor a handful of URLs and print the results to the console."""
        self.monitor.monitor_urls()
