import os
import json
import typing
import urllib.error
import urllib.parse
import urllib.request
import time
from email.message import Message

from prefect import flow, task, get_run_logger

# staging
RENDER_ENDPOINT_ID = "oh1xx5fpoeogpw"


class Response(typing.NamedTuple):
    body: str
    headers: Message
    status: int
    error_count: int = 0

    def json(self) -> typing.Any:
        """
        Decode body's JSON.

        Returns:
            Pythonic representation of the JSON object
        """
        try:
            output = json.loads(self.body)
        except json.JSONDecodeError:
            output = ""
        return output


def request(
    url: str,
    data: typing.Optional[dict] = None,
    params: typing.Optional[dict] = None,
    headers: typing.Optional[dict] = None,
    method: str = "GET",
    data_as_json: bool = True,
    error_count: int = 0,
) -> Response:
    if not url.casefold().startswith("http"):
        raise urllib.error.URLError("Incorrect and possibly insecure protocol in url")
    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers = {"Accept": "application/json", **headers}

    if method == "GET":
        params = {**params, **data}
        data = None

    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True, safe="/")

    if data:
        if data_as_json:
            request_data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json; charset=UTF-8"
        else:
            request_data = urllib.parse.urlencode(data).encode()

    httprequest = urllib.request.Request(
        url, data=request_data, headers=headers, method=method
    )

    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response = Response(
                headers=httpresponse.headers,
                status=httpresponse.status,
                body=httpresponse.read().decode(
                    httpresponse.headers.get_content_charset("utf-8")
                ),
            )
    except urllib.error.HTTPError as e:
        response = Response(
            body=str(e.reason),
            headers=e.headers,
            status=e.code,
            error_count=error_count + 1,
        )

    return response


@task
def post_runpod_job(job: dict) -> dict:
    logger = get_run_logger()

    # Get API key from environment
    api_key = os.getenv("RUNPOD_API_KEY")
    if not api_key:
        raise ValueError("RUNPOD_API_KEY is not set")

    # Construct the RunPod API URL
    url = f"https://api.runpod.ai/v2/{RENDER_ENDPOINT_ID}/run"

    # Set up headers
    headers = {"authorization": api_key, "content-type": "application/json"}

    # Make the request using the request function
    response = request(
        url=url, data=job, headers=headers, method="POST", data_as_json=True
    )

    # Log the response
    logger.info(f"RunPod API response status: {response.status}")
    logger.info(f"RunPod API response: {response.body}")

    # Check for errors
    if response.status != 200:
        raise Exception(f"RunPod API error: {response.status} - {response.body}")
    request_id = response.json().get("id")
    if not request_id:
        raise Exception(f"Request ID not found in response: {response.body}")
    status_url = f"https://api.runpod.ai/v2/{RENDER_ENDPOINT_ID}/status/{request_id}"
    while True:
        response = request(
            url=status_url,
            headers=headers,
            method="GET",
        )
        logger.info(f"RunPod API response ({response.status}): {response.body}")
        if response.status == 200:
            if response.json().get("status").upper() in ["COMPLETED", "FAILED", "TIMED_OUT", "CANCELLED"]:
                break
        time.sleep(1)
    # Parse and return the JSON response
    return response.json()


@flow
def render(job: dict) -> dict:
    return post_runpod_job(job)


if __name__ == "__main__":
    input_image = "https://gendo-gee-dev.s3.amazonaws.com/test/base_interior.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS4PXMQRNG%2F20250716%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250716T124443Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEUaCWV1LXdlc3QtMiJHMEUCIQD5dJPc0x85cDKIpqct2g558lXjJX1sGvF2qCXT7lyDuwIgD%2Fejt5A3hcIW%2FG2p3pmLA9Kq4uWsHfOVZnZXBRPfBn4qoAIIXhABGgwwNTYyNjU5OTQ4NTMiDPJd2SfErnQPS9FNRir9AYzFlr0wz4Fpc7H%2Btqke2Pxa%2F2Zhcph1KLHqcOQOArlXx12ufmTHGUtVXNg%2Fuz69O%2Fow021FQbupl7TE0WYx95lnTUryD1arJmOZ23Kxyu%2BEcPo7TwRqNOzAje2bb1%2B7yVw5eoocbMbUCxoMnlUCwcYAyUWDG3ePRLU6aaN%2FdiLbI89EhVrl%2FIBX73jPvWS9uHKqWQioNyQBej5%2FVV7oZJUvbm9pplh62ZX5dN2VnnCFNNcjjlbP9jwuwI6xrJSDdk8lICzAPMXcwcIJOYk%2FnNZ%2BFn5dvYrD4XdceugPEEcyy0BQH6LE8fvFbw8KELnmAo%2Fji%2FMECXgAdHUR33MwmL3ewwY6nQHB34LviwtOVff4SqT8B6SlXrOf7RhpfdaX0VcGQj0vLNCoSXleGYwdE67rYahv3kc4QUVPbGg6GISLSpzFeaLkz3lYYgCqcQV77zw8D12eh94Or3QponiAN2NeuPs1STOXgu1jr9PcM0PlZ9vChg6m%2FI5gvXLgaOdxTZLn1wAG1f0xQ%2FXgbKftLq919qweRHBVADcKeZsosNA56808&X-Amz-Signature=390274070e79ae720457ef8dfa84dc37e49967e14f6ecb45638f4676f6ceeaff"
    ref_image = "https://gendo-gee-dev.s3.amazonaws.com/test/standing-06.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS4PXMQRNG%2F20250716%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250716T124604Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEUaCWV1LXdlc3QtMiJHMEUCIQD5dJPc0x85cDKIpqct2g558lXjJX1sGvF2qCXT7lyDuwIgD%2Fejt5A3hcIW%2FG2p3pmLA9Kq4uWsHfOVZnZXBRPfBn4qoAIIXhABGgwwNTYyNjU5OTQ4NTMiDPJd2SfErnQPS9FNRir9AYzFlr0wz4Fpc7H%2Btqke2Pxa%2F2Zhcph1KLHqcOQOArlXx12ufmTHGUtVXNg%2Fuz69O%2Fow021FQbupl7TE0WYx95lnTUryD1arJmOZ23Kxyu%2BEcPo7TwRqNOzAje2bb1%2B7yVw5eoocbMbUCxoMnlUCwcYAyUWDG3ePRLU6aaN%2FdiLbI89EhVrl%2FIBX73jPvWS9uHKqWQioNyQBej5%2FVV7oZJUvbm9pplh62ZX5dN2VnnCFNNcjjlbP9jwuwI6xrJSDdk8lICzAPMXcwcIJOYk%2FnNZ%2BFn5dvYrD4XdceugPEEcyy0BQH6LE8fvFbw8KELnmAo%2Fji%2FMECXgAdHUR33MwmL3ewwY6nQHB34LviwtOVff4SqT8B6SlXrOf7RhpfdaX0VcGQj0vLNCoSXleGYwdE67rYahv3kc4QUVPbGg6GISLSpzFeaLkz3lYYgCqcQV77zw8D12eh94Or3QponiAN2NeuPs1STOXgu1jr9PcM0PlZ9vChg6m%2FI5gvXLgaOdxTZLn1wAG1f0xQ%2FXgbKftLq919qweRHBVADcKeZsosNA56808&X-Amz-Signature=367ce5d55c2c77fa5545addbb0e7eb413bd03cf8580c0dd3b6f71c6f20da750c"
    upload_url = "https://gendo-gee-dev.s3.amazonaws.com/test/prefect-output.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS4PXMQRNG%2F20250716%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250716T124420Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEUaCWV1LXdlc3QtMiJHMEUCIQD5dJPc0x85cDKIpqct2g558lXjJX1sGvF2qCXT7lyDuwIgD%2Fejt5A3hcIW%2FG2p3pmLA9Kq4uWsHfOVZnZXBRPfBn4qoAIIXhABGgwwNTYyNjU5OTQ4NTMiDPJd2SfErnQPS9FNRir9AYzFlr0wz4Fpc7H%2Btqke2Pxa%2F2Zhcph1KLHqcOQOArlXx12ufmTHGUtVXNg%2Fuz69O%2Fow021FQbupl7TE0WYx95lnTUryD1arJmOZ23Kxyu%2BEcPo7TwRqNOzAje2bb1%2B7yVw5eoocbMbUCxoMnlUCwcYAyUWDG3ePRLU6aaN%2FdiLbI89EhVrl%2FIBX73jPvWS9uHKqWQioNyQBej5%2FVV7oZJUvbm9pplh62ZX5dN2VnnCFNNcjjlbP9jwuwI6xrJSDdk8lICzAPMXcwcIJOYk%2FnNZ%2BFn5dvYrD4XdceugPEEcyy0BQH6LE8fvFbw8KELnmAo%2Fji%2FMECXgAdHUR33MwmL3ewwY6nQHB34LviwtOVff4SqT8B6SlXrOf7RhpfdaX0VcGQj0vLNCoSXleGYwdE67rYahv3kc4QUVPbGg6GISLSpzFeaLkz3lYYgCqcQV77zw8D12eh94Or3QponiAN2NeuPs1STOXgu1jr9PcM0PlZ9vChg6m%2FI5gvXLgaOdxTZLn1wAG1f0xQ%2FXgbKftLq919qweRHBVADcKeZsosNA56808&X-Amz-Signature=dbc2eaeba49074edb7b1aa47b4ea1ede422159cf224bff9f0d96353c9f9a10a1"
    render_parmas = {
        "prompt": "Picasso style painting of a house",
        "system_negative_prompt": "ugly, pixel art",
        "input_image_presigned_url": input_image,
        "upload_url": upload_url,
        "seed": 28337543,
        "safety_checker_threshold": 0.5,
        "control_image_strength": 1.99,
        "canny_strength": 0.0,
        "depth_strength": 0.0,
        "style_reference_image_presigned_url": ref_image,  # Optional
        "image_prompt_strength": 1.8,  # Optional
    }
    job = {
        "input": {
            "feature": "render",  # Name of the feature to use
            "parameters": render_parmas,
            # Optional parameters
            "generation_job_id": "prefect-0001",  # ID for tracking in core API
            "core_api_base_url": None,  # Base URL for core API
            "manual_webhook_route": None,  # Webhook URL for job updates
            "log_context": {},  # Additional logging context
            "external_webhook_url": None,  # Required for speckle handler
        },
    }
    render(job)
