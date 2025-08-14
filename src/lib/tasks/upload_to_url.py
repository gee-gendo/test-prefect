import requests
from prefect import get_run_logger, task


@task
def upload_to_s3(image_url: str, output_url: str) -> bool:
    """Download image from URL and upload to S3 output URL."""
    logger = get_run_logger()

    try:
        # Download the image in memory
        logger.info(f"Downloading image from: {image_url}")
        response = requests.get(image_url)
        response.raise_for_status()  # Raise exception for bad status codes
        image_data = response.content

        logger.info(f"Downloaded {len(image_data)} bytes")

        # Upload the image data to S3
        logger.info(f"Uploading to: {output_url}")
        upload_response = requests.put(
            output_url,
            data=image_data,
            headers={"Content-Type": "image/png"},
        )
        upload_response.raise_for_status()

        success = upload_response.status_code == 200
        logger.info(
            f"Upload {'successful' if success else 'failed'} (status: {upload_response.status_code})"
        )
        return success

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during image upload process: {e}")
        return False
