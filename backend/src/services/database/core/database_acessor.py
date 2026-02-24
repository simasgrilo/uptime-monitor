"""Template for the database accessor class, which will handle all interactions with the database."""

from typing import Protocol
from backend.src.services.monitor.models.url import URL

class DatabaseAccessor(Protocol):
    """Protocol for the database accessor, which will handle all interactions with the database."""

    def store_response_time(self, url: URL, response_time: float) -> None:
        """Store the response time for a given URL in the database.

        Args:
            url (URL): The URL for which the response time is being stored.
            response_time (float): The response time to be stored.
        """

