import json
import typing
import urllib.error
import urllib.parse
import urllib.request
import time
import logging
import os
from email.message import Message

from prefect.blocks.system import Secret


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


def run_runpod_job(
    job: dict,
    logger: logging.Logger | logging.LoggerAdapter[logging.Logger],
    api_key: str,
    render_endpoint_id: str,
) -> dict:
    url = f"https://api.runpod.ai/v2/{render_endpoint_id}/run"

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
    status_url = f"https://api.runpod.ai/v2/{render_endpoint_id}/status/{request_id}"
    while True:
        response = request(
            url=status_url,
            headers=headers,
            method="GET",
        )
        logger.info(f"RunPod API response ({response.status}): {response.body}")
        if response.status == 200:
            if response.json().get("status").upper() in [
                "COMPLETED",
                "FAILED",
                "TIMED_OUT",
                "CANCELLED",
            ]:
                break
        time.sleep(1)
    # Parse and return the JSON response
    r = response.json()
    return r


def get_runpod_api_key() -> str:
    api_key = os.getenv("RUNPOD_API_KEY")
    if api_key:
        return api_key
    else:
        secret: Secret[str] = Secret.load("runpod-api-key-dev")  # type: ignore
        return secret.get()
