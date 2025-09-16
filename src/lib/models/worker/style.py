from pydantic import BaseModel


class StyleParams(BaseModel):
    """Parameters for style workflow"""

    input_image_presigned_url: str
    style_strength: float
    canny_strength: float
    depth_strength: float
    prompt: str
    # Commons
    seed: int
    output_image_presigned_url: str
    # Internals
    system_negative_prompt: str
    safety_checker_threshold: float
