"""Mock implementation of the DatabaseAccessor for testing purposes."""

from backend.src.services.database.core.database_acessor import DatabaseAccessor
from backend.src.services.monitor.models.monitor_record import MonitorRecord

class DatabaseMock(DatabaseAccessor):
    """Mock implementation of the DatabaseAccessor for testing purposes."""
    
    def store_response_time(self, monitor_record: MonitorRecord):
        """Mock implementation of the store_response_time method."""
        print(f"Storing response time for {monitor_record.url}: {monitor_record.response_time} seconds")