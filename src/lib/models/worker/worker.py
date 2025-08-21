from enum import StrEnum, auto

from pydantic import BaseModel, Field, model_validator

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


class WorkerParams(BaseModel):
    parameters: (
        CutoutParams
        | DescribeParams
        | EmbeddingParams
        | MaskParams
        | RenderParameters
        | SpeckleParams
        | StyleParams
    )
    generation_job_id: str
    feature: WorkerFeature
    core_api_base_url: str | None = None
    manual_webhook_route: str | None = None
    log_context: dict = Field(default_factory=dict)
    external_webhook_url: str | None = None

    @model_validator(mode="after")
    def check_feature_type(self):
        """Check that the feature is valid."""
        if self.feature not in _FEATURE_TO_PARAMS_MAP:
            raise ValueError(f"Invalid feature: {self.feature}")

        if not isinstance(
            self.parameters, param := _FEATURE_TO_PARAMS_MAP[self.feature]
        ):
            raise ValueError(
                f"For feature {self.feature}, parameters must be a {param.__name__} object, got {self.parameters.__class__.__name__}."
                f" {param.__name__} schema: {param.model_json_schema()}"
            )

        return self


class WorkerJob(BaseModel):
    input: WorkerParams
    webhook_url: str | None = None
