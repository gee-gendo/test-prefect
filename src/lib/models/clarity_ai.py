from enum import StrEnum, auto


from pydantic import BaseModel, Field


class ClarityScheduler(StrEnum):
    DPMPP_2M_KARRAS = "DPM++ 2M Karras"
    DPMPP_SDE_KARRAS = "DPM++ SDE Karras"
    DPMPP_2M_SDE_EXPONENTIAL = "DPM++ 2M SDE Exponential"
    DPMPP_2M_SDE_KARRAS = "DPM++ 2M SDE Karras"
    EULER_A = "Euler a"
    EULER = "Euler"
    LMS = "LMS"
    HEUN = "Heun"
    DPM2 = "DPM2"
    DPM2_A = "DPM2 a"
    DPMPP_2S_A = "DPM++ 2S a"
    DPMPP_2M = "DPM++ 2M"
    DPMPP_SDE = "DPM++ SDE"
    DPMPP_2M_SDE = "DPM++ 2M SDE"
    DPMPP_2M_SDE_HEUN = "DPM++ 2M SDE Heun"
    DPMPP_2M_SDE_HEUN_KARRAS = "DPM++ 2M SDE Heun Karras"
    DPMPP_2M_SDE_HEUN_EXPONENTIAL = "DPM++ 2M SDE Heun Exponential"
    DPMPP_3M_SDE = "DPM++ 3M SDE"
    DPMPP_3M_SDE_KARRAS = "DPM++ 3M SDE Karras"
    DPMPP_3M_SDE_EXPONENTIAL = "DPM++ 3M SDE Exponential"
    DPM_FAST = "DPM fast"
    DPM_ADAPTIVE = "DPM adaptive"
    LMS_KARRAS = "LMS Karras"
    DPM2_KARRAS = "DPM2 Karras"
    DPM2_A_KARRAS = "DPM2 a Karras"
    DPMPP_2S_A_KARRAS = "DPM++ 2S a Karras"
    RESTART = "Restart"
    DDIM = "DDIM"
    PLMS = "PLMS"
    UNIPC = "UniPC"


class ImageOutputFormat(StrEnum):
    PNG = auto()
    JPEG = auto()


class ClarityUpscaleParams(BaseModel):
    image: str = ""
    mask: str = ""
    prompt: str = "People cutout, masterpiece, best quality, highres, <lora:more_details:0.5> <lora:SDXLrender_v2.0:1>"
    negative_prompt: str = (
        "(worst quality, low quality, normal quality:2) JuggernautNegative-neg"
    )
    scale_factor: float = Field(default=2.0, ge=1.0, le=4.0)
    dynamic: float = Field(default=6.0, ge=0.0, le=50.0)
    creativity: float = Field(default=0.35, ge=0.0, le=1.0)
    resemblance: float = Field(default=0.6, ge=0.0, le=3.0)
    tiling_width: int = Field(default=80, ge=10, le=4096)
    tiling_height: int = Field(default=112, ge=10, le=4096)
    scheduler: ClarityScheduler = ClarityScheduler.DPMPP_2M_SDE_KARRAS
    steps: int = Field(default=18, ge=3, le=100)
    seed: int = 123
    downscaling: bool = True
    downscaling_resolution: int = Field(default=1024, ge=512, le=4096)
    sharpen: float = Field(default=0.0, ge=0.0, le=10.0)
    hand_fix: bool = False
    output_format: ImageOutputFormat = ImageOutputFormat.PNG
