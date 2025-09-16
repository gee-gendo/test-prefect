from pydantic import BaseModel


class EmbeddingParams(BaseModel):
    """Parameters for embedding workflow. Part of the Material feature"""

    image_url: str
    output_image_presigned_url: str
