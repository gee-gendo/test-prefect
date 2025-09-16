from dotenv import load_dotenv

from lib.models.worker.render import RenderParameters
from lib.models.worker.worker import RenderWorkerParams, WorkerFeature, WorkerJob

load_dotenv()  # before importing prefect

from prefect import flow  # noqa: E402

from lib.tasks.render import run_render_runpod  # noqa: E402


@flow
def render(job: WorkerJob) -> dict:
    """
    Render a job using the RunPod API.
    """

    return run_render_runpod(job.model_dump())


if __name__ == "__main__":
    job = WorkerJob(
        input=RenderWorkerParams(
            feature=WorkerFeature.RENDER,
            generation_job_id="prefect-0001",
            parameters=RenderParameters(
                prompt="Picasso style painting of a haidresser shop",
                input_image_presigned_url="https://gendo-gee-dev.s3.amazonaws.com/test/crowd/gendo-mediterranean-house.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JSVG463NOV%2F20250819%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250819T152003Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHgaCWV1LXdlc3QtMiJHMEUCIQCW3l57Y5vHZcnsqLY8qQUeRG1%2Fmm6IKt7e2OAJtBwlHAIgHSLR9%2BG0Dwq8yiZt8p0shCZ%2F0OrvBsy4SHRRhZXFF%2BYqqQIIwP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgwwNTYyNjU5OTQ4NTMiDIyVyf%2BRJVojiCM8QSr9AVd9mVfcRZMX8J7sq8iiYnuuRgkxllnsRFrzdaocN2KfuIQDii1DaaBQflul5yuyxgzzWKbsww3iyYVyzHEQxiRFTU7tIvagnK1DOkdkwr4CI8qOhxmqaeJrDGZ9G1l6XwFNyzxGBDsgQCDEk7wiyU11oBeKEWd5N37e1rSv3QPXDAG5qj5g6M%2F9qsHJytcEMEPKY7GSezB8ielQ6w3OgBzsUFHM3eILlQGAUpNBPdoPtHyHDE%2BXllmpp6bL7%2BlBoJzVpQlwWn4f80xB6I6s6cElpOikxB7CRz6r2JeGJKw3tm9pfVFvbLY3cszxTGTWBIkSa2NOAmN41yucAZow7quSxQY6nQH80WviXbJyLbaRMUM44D6wmAeIXgXFfJXa8Y%2BABsNIdpq%2BMixVVBMu13mGRlNH9Gp9VftI88KQil7LnNA5WG0RCQFbpVd4wLU8QbgP1nZQFWiy%2Bi4AJ6LwAT%2BfX6c0QqCwIv7bKCMYn%2F5t52dZdhqnuInJJZZDhZmPLeZptnEwMT%2F5cVVNTrABYOUmJJV0%2FfzvbpmV5z%2FZiFC2NsOE&X-Amz-Signature=44eb1feb6a9880a2d5b65ac949ee0cb3cd8e72a1e52ea1e8b0252d488dbb83e2",
                upload_url="https://gendo-gee-dev.s3.amazonaws.com/test/mask.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JSVG463NOV%2F20250819%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250819T152021Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHgaCWV1LXdlc3QtMiJHMEUCIQCW3l57Y5vHZcnsqLY8qQUeRG1%2Fmm6IKt7e2OAJtBwlHAIgHSLR9%2BG0Dwq8yiZt8p0shCZ%2F0OrvBsy4SHRRhZXFF%2BYqqQIIwP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgwwNTYyNjU5OTQ4NTMiDIyVyf%2BRJVojiCM8QSr9AVd9mVfcRZMX8J7sq8iiYnuuRgkxllnsRFrzdaocN2KfuIQDii1DaaBQflul5yuyxgzzWKbsww3iyYVyzHEQxiRFTU7tIvagnK1DOkdkwr4CI8qOhxmqaeJrDGZ9G1l6XwFNyzxGBDsgQCDEk7wiyU11oBeKEWd5N37e1rSv3QPXDAG5qj5g6M%2F9qsHJytcEMEPKY7GSezB8ielQ6w3OgBzsUFHM3eILlQGAUpNBPdoPtHyHDE%2BXllmpp6bL7%2BlBoJzVpQlwWn4f80xB6I6s6cElpOikxB7CRz6r2JeGJKw3tm9pfVFvbLY3cszxTGTWBIkSa2NOAmN41yucAZow7quSxQY6nQH80WviXbJyLbaRMUM44D6wmAeIXgXFfJXa8Y%2BABsNIdpq%2BMixVVBMu13mGRlNH9Gp9VftI88KQil7LnNA5WG0RCQFbpVd4wLU8QbgP1nZQFWiy%2Bi4AJ6LwAT%2BfX6c0QqCwIv7bKCMYn%2F5t52dZdhqnuInJJZZDhZmPLeZptnEwMT%2F5cVVNTrABYOUmJJV0%2FfzvbpmV5z%2FZiFC2NsOE&X-Amz-Signature=28c1ae0ddb85c9d2606c4b652af7e8401221912c4d7b3ac12644367c1a25c375",
            ),
        )
    )
    result = render(job)
    print(result)
