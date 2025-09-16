from enum import StrEnum, auto
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from lib.models.worker.cutout import CutoutParams
from lib.models.worker.describe import DescribeParams
from lib.models.worker.embedding import EmbeddingParams
from lib.models.worker.render import RenderParameters
from lib.models.worker.mask import MaskParams
from lib.models.worker.speckle import SpeckleParams
from lib.models.worker.style import StyleParams


class WorkerFeature(StrEnum):
    CUTOUT = auto()
    DESCRIBE = auto()
    EMBEDDING = auto()
    MASK = auto()
    MATERIAL = auto()
    RENDER = auto()
    SPECKLE = auto()
    STYLE = auto()


_FEATURE_TO_PARAMS_MAP = {
    WorkerFeature.RENDER: RenderParameters,
    WorkerFeature.CUTOUT: CutoutParams,
    WorkerFeature.DESCRIBE: DescribeParams,
    WorkerFeature.EMBEDDING: EmbeddingParams,
    WorkerFeature.MASK: MaskParams,
    WorkerFeature.SPECKLE: SpeckleParams,
    WorkerFeature.STYLE: StyleParams,
}


class BaseWorkerParams(BaseModel):
    generation_job_id: str
    core_api_base_url: str | None = None
    manual_webhook_route: str | None = None
    log_context: dict = Field(default_factory=dict)
    external_webhook_url: str | None = None

    @model_validator(mode="after")
    def check_feature_type(self):
        """Check that the feature is valid."""
        if self.feature not in _FEATURE_TO_PARAMS_MAP:
            raise ValueError(f"Invalid feature: {self.feature}")

        return self

    # configure to avoid unknown fields
    model_config = ConfigDict(extra="forbid")


class RenderWorkerParams(BaseWorkerParams):
    parameters: RenderParameters
    feature: Literal["render"]


class CutoutWorkerParams(BaseWorkerParams):
    parameters: CutoutParams
    feature: Literal["cutout"]


class DescribeWorkerParams(BaseWorkerParams):
    parameters: DescribeParams
    feature: Literal["describe"]


class EmbeddingWorkerParams(BaseWorkerParams):
    parameters: EmbeddingParams
    feature: Literal["embedding"]


class MaskWorkerParams(BaseWorkerParams):
    parameters: MaskParams
    feature: Literal["Mask"]


class SpeckleWorkerParams(BaseWorkerParams):
    parameters: SpeckleParams
    feature: Literal["Speckle"]


class StyleWorkerParams(BaseWorkerParams):
    parameters: StyleParams
    feature: Literal["style"]


class WorkerJob(BaseModel):
    """Worker job"""

    input: (
        RenderWorkerParams
        | CutoutWorkerParams
        | DescribeWorkerParams
        | EmbeddingWorkerParams
        | MaskWorkerParams
        | SpeckleWorkerParams
        | StyleWorkerParams
    ) = Field(discriminator="feature")
    webhook_url: str | None = None


if __name__ == "__main__":
    d = {
        "job": {
            "input": {
                "feature": "render",
                "parameters": {
                    "seed": 846164,
                    "prompt": "Picasso style rendering, painting, super abstract",
                    "canny_strength": 0.3,
                    "depth_strength": 0.2,
                    "image_prompt_strength": 0,
                    "control_image_strength": 0.9,
                    "system_negative_prompt": "blurry, unsharp, low resolution, low quality, bad quality, noisy",
                    "safety_checker_threshold": 0.5,
                    "input_image_presigned_url": "https://gendo-gee-dev.s3.amazonaws.com/test/crowd/gendo-mediterranean-house.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS4CXSX5GN%2F20250916%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250916T091510Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBIaCWV1LXdlc3QtMiJIMEYCIQDNCyj2Hr3qMnNy2keaMxG%2ByYPghB2HPCZmE2mVknIdAAIhANp6z47s0hrp%2FehfnxoHnFDuxR%2FaHdAEAHSvdKc1SDOuKqkCCIr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMDU2MjY1OTk0ODUzIgxiS9yfK4CdWtgaemUq%2FQHuYA%2BOw2bPRFu3O3820Pfun1EsnW60FrRZ6NMDHaoacPhs9QT0c7sLcWZ9V6FN2JBn6ApD2QAj7qecwBz9x8ND4gHiinllAUgiCdG3fmpm2bQJo5Q6wdmqNF13v2Eyha1Mnaa5NhWzTUOPeZA3CL%2BzcWOWBJb9nDhRBhwE9RejjBVpmj42vHBre7umndaFp%2Bbx7HMNe6qJcmpETil98xRdv5oUcExadR0etFAJDdtxbCpBBrKy4%2FUaFyS0eY0YV70Y%2BPQtBN5I03dhkPBYb2WuNdVjFjxXtI63bVgT4VuMWdHIZ6A3smJRj%2FPtVVjcX0UN%2Blfln5P7j8HSatP%2BMIjVpMYGOpwBN%2FEyb8A0PfnsFbi22hStSyzrePaEJG%2FJw%2FIocgGy2l3lKgl1U%2Fs2Vr5zdHAgELVC24dFLlodIyNWAtpzw1M6VQLFmxNj2f7mjGKGo%2FAJADtl0o5dpo4zE07Iq4NWi7P4KQwe8QsYNaS%2F%2Fckwp8P9s2K5kJJBjj6%2BhTp373jWJAeCRez3S7nUTzduo9XGkX3yebxqqZAVtlevH00f&X-Amz-Signature=1bf971a5dc2ca7d12e93e953f79c66f169c68a5c476777eab156386d4472bdb4",
                    "output_image_presigned_url": "https://gendo-gee-dev.s3.amazonaws.com/test/mask.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS4CXSX5GN%2F20250916%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250916T091538Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBIaCWV1LXdlc3QtMiJIMEYCIQDNCyj2Hr3qMnNy2keaMxG%2ByYPghB2HPCZmE2mVknIdAAIhANp6z47s0hrp%2FehfnxoHnFDuxR%2FaHdAEAHSvdKc1SDOuKqkCCIr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMDU2MjY1OTk0ODUzIgxiS9yfK4CdWtgaemUq%2FQHuYA%2BOw2bPRFu3O3820Pfun1EsnW60FrRZ6NMDHaoacPhs9QT0c7sLcWZ9V6FN2JBn6ApD2QAj7qecwBz9x8ND4gHiinllAUgiCdG3fmpm2bQJo5Q6wdmqNF13v2Eyha1Mnaa5NhWzTUOPeZA3CL%2BzcWOWBJb9nDhRBhwE9RejjBVpmj42vHBre7umndaFp%2Bbx7HMNe6qJcmpETil98xRdv5oUcExadR0etFAJDdtxbCpBBrKy4%2FUaFyS0eY0YV70Y%2BPQtBN5I03dhkPBYb2WuNdVjFjxXtI63bVgT4VuMWdHIZ6A3smJRj%2FPtVVjcX0UN%2Blfln5P7j8HSatP%2BMIjVpMYGOpwBN%2FEyb8A0PfnsFbi22hStSyzrePaEJG%2FJw%2FIocgGy2l3lKgl1U%2Fs2Vr5zdHAgELVC24dFLlodIyNWAtpzw1M6VQLFmxNj2f7mjGKGo%2FAJADtl0o5dpo4zE07Iq4NWi7P4KQwe8QsYNaS%2F%2Fckwp8P9s2K5kJJBjj6%2BhTp373jWJAeCRez3S7nUTzduo9XGkX3yebxqqZAVtlevH00f&X-Amz-Signature=9beaaac7239152a4901f46ed99115119dd9fbdfc167256a3201a6f85d3fd9f44",
                    "style_reference_image_presigned_url": "",
                },
                "log_context": {},
                "generation_job_id": "local-test-10-15",
                "external_webhook_url": None,
                "manual_webhook_route": None,
            },
            "webhook_url": "https://example.com/",
        }
    }

    job = WorkerJob.model_validate(d["job"]).model_dump()
    # TODO: remove this once the upload_url is renamed downstream
    upload_url = job["input"]["parameters"].pop("output_image_presigned_url")
    job["input"]["parameters"]["output_image_presigned_url"] = upload_url

    print(job)
