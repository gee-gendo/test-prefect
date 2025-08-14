from lib.models.people_mask import (
    PeopleMaskParams,
    get_person_masking_workflow_from_params,
)
from lib.runpod_client import get_runpod_api_key, run_runpod_job


from prefect import get_run_logger, task

# staging
CROWD_RUNPOD_ENDPOINT_ID = "33a0cvuzq77poh"


@task
def generate_people_mask(
    image: str, mask_url: str, people_mask_params: PeopleMaskParams
) -> str:
    logger = get_run_logger()

    # Get API key from environment
    api_key = get_runpod_api_key()

    workflow = get_person_masking_workflow_from_params(
        image, mask_url, people_mask_params
    )
    r = run_runpod_job(workflow, logger, api_key, CROWD_RUNPOD_ENDPOINT_ID)
    logger.info(f"Runpod job result: {r}")
    return mask_url
