"""Mock implementation of the DatabaseAccessor for testing purposes."""

from backend.src.services.database.core.database_acessor import DatabaseAccessor

class DatabaseMock(DatabaseAccessor):
    """Mock implementation of the DatabaseAccessor for testing purposes."""
    
    def store_response_time(self, url, response_time):
        """Mock implementation of the store_response_time method."""
        print(f"Storing response time for {url.url}: {response_time} seconds")