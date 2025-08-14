from lib.models.kontext import KontextParams
from lib.replicate_client import get_replicate_api_key

import replicate
from prefect import get_run_logger, task


from typing import Any


@task
def run_kontext(input_url: str, prompt: str, kontext_params: KontextParams) -> str:
    logger = get_run_logger()
    logger.info(f"Running Replicate with params: {kontext_params.model_dump()}")

    replicate.default_client._api_token = get_replicate_api_key()

    # Construct the Replicate API URL
    output: Any = replicate.run(
        "black-forest-labs/flux-kontext-pro",
        input={
            "prompt": prompt,
            "input_image": input_url,
            **kontext_params.model_dump(),
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
