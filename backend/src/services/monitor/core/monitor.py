"""Main module for the URL monitoring service"""

from typing import List
import requests
import time
from requests.exceptions import MissingSchema, ReadTimeout, ConnectionError
from backend.src.services.monitor.models.url import URL
from backend.src.services.database.core.database_acessor import DatabaseAccessor
from backend.src.services.monitor.models.monitor_record import MonitorRecord, Status


class Monitor:
    """Main class to monitor the URL health. This class will send HTTP HEAD requests to the 
       services, measuring the time spent 
       between every request and storing it per URL as the service requirements.
    """

    def __init__(self, urls: List[URL], database_accessor: DatabaseAccessor, configs: dict):
        """Initialize the monitor with the list of URLs to monitor.

        Args:
            urls (list[URL]): List of URLs to monitor.
        """
        self.urls = urls
        self.database_accessor = database_accessor
        self.configs = configs
        self.default_timeout = 20

    def monitor_urls(self):
        """Monitor the URLs and store the results in the database."""
        for url in self.urls:
            status = Status.ok
            try:
                response_time = self.send_head_request(url)
                # use time of day clock time as this is a good approximation of when the event
                # took place 
                datetime_measured = time.ctime().split(' ')
                weekday_measure = datetime_measured[0]
                date_measure = f'{datetime_measured[1]} {datetime_measured[2]} {datetime_measured[4]}'
                time_measure = datetime_measured[3]
            except (ReadTimeout, ConnectionError) as exc:
                #TODO add logging here to register that the requested timed out
                # and the error message from the exception
                status = Status.nok
            record = MonitorRecord(url=url,
                                   response_time=response_time, 
                                   date=date_measure, time=time_measure, weekday=weekday_measure, status=status)
            self.database_accessor.store_response_time(record)

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
