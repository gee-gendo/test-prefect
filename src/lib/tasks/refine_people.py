from lib.models.clarity_ai import ClarityUpscaleParams
from lib.replicate_client import get_replicate_api_key

import replicate
from prefect import get_run_logger, task


from typing import Any


@task
def refine_people(
    image: str, mask: str, clarity_upscale_params: ClarityUpscaleParams
) -> str:
    logger = get_run_logger()
    logger.info(
        f"Running Clarity Upscale with params: {clarity_upscale_params.model_dump()}"
    )

    logger.info(f"Image: {image}")
    logger.info(f"Mask: {mask}")

    replicate.default_client._api_token = get_replicate_api_key()

    # Construct the Replicate API URL
    output: Any = replicate.run(
        "philz1337x/clarity-upscaler:dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e",
        input={
            **clarity_upscale_params.model_dump(),
            "image": image,
            "mask": mask,
        },
    )
    if isinstance(output, list):
        logger.debug(f"Replicate output is a list: {output}")
        url = output[0].url  # type: ignore
    else:
        logger.debug(f"Replicate output is not a list: {output}")
        url = output.url  # type: ignore
    logger.info(f"Replicate output: {url}")

    return url
