from lib.models.clarity_ai import ClarityUpscaleParams
from lib.models.kontext import KontextParams
from lib.models.people_mask import PeopleMaskParams


from pydantic import BaseModel, model_validator


class CrowdJob(BaseModel):
    prompt: str
    input_url: str
    mask_url: str
    mask_url_read: str
    output_url: str
    kontext: KontextParams = KontextParams()
    people_mask: PeopleMaskParams = PeopleMaskParams()
    clarity_upscale: ClarityUpscaleParams = ClarityUpscaleParams()
    seed: int = 123

    @model_validator(mode="after")
    def inject_dependent_attributes(self):
        """Inject attributes into dependent classes."""
        # Seed injection
        self.kontext.seed = self.seed
        self.clarity_upscale.seed = self.seed

        return self
