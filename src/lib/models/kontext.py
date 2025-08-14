from enum import StrEnum

from lib.models.clarity_ai import ImageOutputFormat

from pydantic import BaseModel, Field


class KontextAspectRatio(StrEnum):
    MATCH_INPUT_IMAGE = "match_input_image"
    _1_1 = "1:1"
    _16_9 = "16:9"
    _9_16 = "9:16"
    _4_3 = "4:3"
    _3_4 = "3:4"
    _3_2 = "3:2"
    _2_3 = "2:3"
    _4_5 = "4:5"
    _5_4 = "5:4"
    _21_9 = "21:9"
    _9_21 = "9:21"
    _2_1 = "2:1"
    _1_2 = "1:2"


class KontextParams(BaseModel):
    aspect_ratio: KontextAspectRatio = KontextAspectRatio.MATCH_INPUT_IMAGE
    prompt_upsampling: bool = False
    seed: int = 123
    output_format: ImageOutputFormat = ImageOutputFormat.PNG
    safety_tolerance: int = Field(default=2, ge=0, le=6)
