"""Main module for the URL monitoring service"""

from typing import List
import requests
from requests.exceptions import MissingSchema
from backend.src.services.monitor.models.url import URL
from backend.src.services.database.core.database_acessor import DatabaseAccessor


class Monitor:
    """Main class to monitor the URL health. This class will send HTTP HEAD requests to the services, 
       measuring the time spent 
       between every request and storing it per URL as the service requirements.
    """

    def __init__(self, urls: List[URL], databaseAccessor: DatabaseAccessor, configs: dict):
        """Initialize the monitor with the list of URLs to monitor.

        Args:
            urls (list[URL]): List of URLs to monitor.
        """
        self.urls = urls
        self.database_accessor = databaseAccessor
        self.configs = configs
        self.default_timeout = 20

    def monitor_urls(self):
        """Monitor the URLs and store the results in the database."""
        for url in self.urls:
            response_time = self.send_head_request(url)
            self.database_accessor.store_response_time(url, response_time)

    def send_head_request(self, url: URL) -> float:
        """send a HTTP HEAD request to the given URL and return the elapsed time in seconds
        Args:
            url (URL): The URL to send the request to.
        """
        try:
            timeout = self.configs.get('timeout') or self.default_timeout
            response = requests.head(url.url, timeout=timeout)
            # use response.elased.total_seconds as it is more precise than this method
            # calculating the time before and after the request
        except MissingSchema as e:
            #TODO add logging here before assuming the schema is HTTPS
            print(f"Missing schema for URL {url.url}, assuming HTTPS. Error: {e}")
            schema = 'https://'
            response = requests.head(schema + url.url, timeout=timeout)
        return response.elapsed.total_seconds()
