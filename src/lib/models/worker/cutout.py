from typing import Optional

from pydantic import BaseModel


class CutoutParams(BaseModel):
    """Parameters for cutout workflow"""

    mannequin_image_presigned_url: str
    pose_image_presigned_url: str
    depth_image_presigned_url: Optional[str] = None
    prompt: str

    # Commons
    upload_url: str
    seed: int
    # Internals
    system_negative_prompt: str
    safety_checker_threshold: float
