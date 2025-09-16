from prefect import get_run_logger, task

from lib.runpod_client import get_runpod_api_key, run_runpod_job


# staging
RENDER_ENDPOINT_ID = "oh1xx5fpoeogpw"


@task(log_prints=True)
def run_render_runpod(job: dict) -> dict:
    logger = get_run_logger()

    # Get API key from environment
    api_key = get_runpod_api_key()

    # TODO: remove this once the upload_url is renamed downstream
    upload_url = job["input"]["parameters"].pop("output_image_presigned_url")
    job["input"]["parameters"]["upload_url"] = upload_url

    import json

    print(json.dumps(job, indent=4))

    # Construct the RunPod API URL
    r = run_runpod_job(job, logger, api_key, RENDER_ENDPOINT_ID)
    return r
