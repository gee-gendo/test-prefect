from pydantic import BaseModel


class MaskParams(BaseModel):
    """Parameters for mask workflow for the Material feature"""

    input_image_presigned_url: str
    input_mask_presigned_url: str
    control_image_strength: float
    canny_strength: float
    depth_strength: float
    # Material description
    prompt: str
    # Optional reference image
    style_reference_image_presigned_url: str | None = None
    image_prompt_strength: float | None = None
    # Commons
    upload_url: str
    seed: int
    # Internals
    safety_checker_threshold: float
    system_negative_prompt: str
