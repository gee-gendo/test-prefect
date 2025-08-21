from pydantic import BaseModel


class EmbeddingParams(BaseModel):
    """Parameters for embedding workflow. Part of the Material feature"""

    image_url: str
    upload_url: str
