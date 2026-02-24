""" Pydantic model for a valid URL to be monitored."""

from pydantic import BaseModel, Field


class URL(BaseModel):
    "Model class for URLs to be monitored"
    url: str = Field(frozen=True, description="The URL to be monitored")

