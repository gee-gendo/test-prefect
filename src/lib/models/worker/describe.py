from pydantic import BaseModel


class DescribeParams(BaseModel):
    """Parameters for describe (text) workflow"""

    prompt: str
    # Optional reference image
    style_reference_image_presigned_url: str | None = None
    image_prompt_strength: float | None = None
    # Commons
    upload_url: str
    seed: int
    # Internals
    system_negative_prompt: str
    safety_checker_threshold: float
