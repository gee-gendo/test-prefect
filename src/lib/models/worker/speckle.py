from pydantic import BaseModel


class SpeckleParams(BaseModel):
    """Parameters for speckle workflow"""

    prompt: str
    depth_map_base64: str
    seed: int
