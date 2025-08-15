from pydantic import BaseModel


class RenderJob(BaseModel):
    prompt: str
    input_image_presigned_url: str
    upload_url: str
    # controlnet parameters
    control_image_strength: float = 1.0
    canny_strength: float = 0.0
    depth_strength: float = 0.0
    # IP adapter parameters
    style_reference_image_presigned_url: str | None = None
    image_prompt_strength: float | None = None
    # System parameters
    system_negative_prompt: str = "ugly, pixel art"
    safety_checker_threshold: float = 0.5
    seed: int = 28337543
