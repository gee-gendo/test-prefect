import os

from prefect.blocks.system import Secret


def get_replicate_api_key() -> str:
    api_key = os.getenv("REPLICATE_API_TOKEN")
    if api_key:
        return api_key
    else:
        secret: Secret[str] = Secret.load("replicate-api-token-dev")  # type: ignore
        return secret.get()
