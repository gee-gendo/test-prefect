from dotenv import load_dotenv

load_dotenv()  # before importing prefect


from prefect import flow  # noqa: E402

from lib.models.crowd import CrowdJob  # noqa: E402
from lib.tasks.people_masking import generate_people_mask  # noqa: E402
from lib.tasks.kontext import run_kontext  # noqa: E402
from lib.tasks.refine_people import refine_people  # noqa: E402
from lib.tasks.upload_to_url import upload_to_s3  # noqa: E402


@flow
def crowd(job: CrowdJob) -> dict:
    kontext_url = run_kontext(job.input_url, job.prompt, job.kontext)
    _ = generate_people_mask(kontext_url, job.mask_url, job.people_mask)
    refined_image_url = refine_people(
        kontext_url, job.mask_url_read, job.clarity_upscale
    )
    success = upload_to_s3(refined_image_url, job.output_url)

    return {"output_url": job.output_url, "success": success}


if __name__ == "__main__":
    job = CrowdJob(
        prompt="Add a woman with a red dress on the right side of the image, do not change anything else. Keep the house and the chairs",
        input_url="https://gendo-gee-dev.s3.amazonaws.com/test/crowd/gendo-mediterranean-house.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS63VAQQ7G%2F20250814%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250814T183213Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAMaCWV1LXdlc3QtMiJHMEUCIEuJGDClNrkrCQ1SEEMR3IVOIBrFKh65OCfpgSHfpQmLAiEAuZqRkapZsAH5IbY9zn%2FsdDrehINFO7XZ4d4cLAlX6uQqoAIITBABGgwwNTYyNjU5OTQ4NTMiDCvaT%2BoXC%2FCGn665Lyr9AeTcs7ys92tVucvGpOYY0PkdVdcLxa0rS0EAXscjUT36ucCfXw6Gu7Eus6BPjV9xSs4%2BZmCS9DyBn%2BujcDQVLqv%2B5Vl8EdUX4ViK0OsueMPpCbTEXsy4sNGVELF1Rz%2F%2FaV%2BfwgvnfkJm8MJc7Bqz3QaNeh6TpBJL421Vsiv3ccaEpvH8kbNNNWwYJkXQmYbKIpaJT4mCpWdKtmOSGNk31p3P7sC5jLIg5ijCGeqbpbpLhr1dmfFnIPjW5bmxXWQYxqgozbZYxHTYx1OJYdnKw8Pd0LoMhRcChL9jf4DtDles7o6B31IZBaTEqYiZ7lAyxSTN%2FQc%2FhNL3MKhkSrAwp9f4xAY6nQEfBR5OKb%2FwzjR3ZWgs1GeuDraJ8GoI%2BmS8ZkVwBLEWonkO3QE%2FdMmJfn85EpIQHPFrxXjnox9RvGgJPWapZqCiaqMATOtfXKyGPMVU%2F5uJUP9OemUxjIa0W0hnFglJsAww%2B5sp9oOrQUtHQkHiJPURNixGr9sQZH5bV1i6OTYlh25YDxEbP8vhsdcywKaeBAS4m8BMgaLCAUCwsKCo&X-Amz-Signature=80d28146581bc6695325dd6bfdd5822f0b8fda48d2e215a91942521f3e122c50",
        mask_url="https://gendo-gee-dev.s3.amazonaws.com/test/mask.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS63VAQQ7G%2F20250814%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250814T183323Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAMaCWV1LXdlc3QtMiJHMEUCIEuJGDClNrkrCQ1SEEMR3IVOIBrFKh65OCfpgSHfpQmLAiEAuZqRkapZsAH5IbY9zn%2FsdDrehINFO7XZ4d4cLAlX6uQqoAIITBABGgwwNTYyNjU5OTQ4NTMiDCvaT%2BoXC%2FCGn665Lyr9AeTcs7ys92tVucvGpOYY0PkdVdcLxa0rS0EAXscjUT36ucCfXw6Gu7Eus6BPjV9xSs4%2BZmCS9DyBn%2BujcDQVLqv%2B5Vl8EdUX4ViK0OsueMPpCbTEXsy4sNGVELF1Rz%2F%2FaV%2BfwgvnfkJm8MJc7Bqz3QaNeh6TpBJL421Vsiv3ccaEpvH8kbNNNWwYJkXQmYbKIpaJT4mCpWdKtmOSGNk31p3P7sC5jLIg5ijCGeqbpbpLhr1dmfFnIPjW5bmxXWQYxqgozbZYxHTYx1OJYdnKw8Pd0LoMhRcChL9jf4DtDles7o6B31IZBaTEqYiZ7lAyxSTN%2FQc%2FhNL3MKhkSrAwp9f4xAY6nQEfBR5OKb%2FwzjR3ZWgs1GeuDraJ8GoI%2BmS8ZkVwBLEWonkO3QE%2FdMmJfn85EpIQHPFrxXjnox9RvGgJPWapZqCiaqMATOtfXKyGPMVU%2F5uJUP9OemUxjIa0W0hnFglJsAww%2B5sp9oOrQUtHQkHiJPURNixGr9sQZH5bV1i6OTYlh25YDxEbP8vhsdcywKaeBAS4m8BMgaLCAUCwsKCo&X-Amz-Signature=773c943eab33aea2fe76202efc3de0ec3d7fa1d54692877130bc97c3674c74eb",
        mask_url_read="https://gendo-gee-dev.s3.amazonaws.com/test/mask.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS63VAQQ7G%2F20250814%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250814T183303Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAMaCWV1LXdlc3QtMiJHMEUCIEuJGDClNrkrCQ1SEEMR3IVOIBrFKh65OCfpgSHfpQmLAiEAuZqRkapZsAH5IbY9zn%2FsdDrehINFO7XZ4d4cLAlX6uQqoAIITBABGgwwNTYyNjU5OTQ4NTMiDCvaT%2BoXC%2FCGn665Lyr9AeTcs7ys92tVucvGpOYY0PkdVdcLxa0rS0EAXscjUT36ucCfXw6Gu7Eus6BPjV9xSs4%2BZmCS9DyBn%2BujcDQVLqv%2B5Vl8EdUX4ViK0OsueMPpCbTEXsy4sNGVELF1Rz%2F%2FaV%2BfwgvnfkJm8MJc7Bqz3QaNeh6TpBJL421Vsiv3ccaEpvH8kbNNNWwYJkXQmYbKIpaJT4mCpWdKtmOSGNk31p3P7sC5jLIg5ijCGeqbpbpLhr1dmfFnIPjW5bmxXWQYxqgozbZYxHTYx1OJYdnKw8Pd0LoMhRcChL9jf4DtDles7o6B31IZBaTEqYiZ7lAyxSTN%2FQc%2FhNL3MKhkSrAwp9f4xAY6nQEfBR5OKb%2FwzjR3ZWgs1GeuDraJ8GoI%2BmS8ZkVwBLEWonkO3QE%2FdMmJfn85EpIQHPFrxXjnox9RvGgJPWapZqCiaqMATOtfXKyGPMVU%2F5uJUP9OemUxjIa0W0hnFglJsAww%2B5sp9oOrQUtHQkHiJPURNixGr9sQZH5bV1i6OTYlh25YDxEbP8vhsdcywKaeBAS4m8BMgaLCAUCwsKCo&X-Amz-Signature=2a0232863afe10dfe8e9e16bb68edfa6026af943ae45959464457c7e2320694c",
        output_url="https://gendo-gee-dev.s3.amazonaws.com/test/result.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS63VAQQ7G%2F20250814%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250814T183347Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAMaCWV1LXdlc3QtMiJHMEUCIEuJGDClNrkrCQ1SEEMR3IVOIBrFKh65OCfpgSHfpQmLAiEAuZqRkapZsAH5IbY9zn%2FsdDrehINFO7XZ4d4cLAlX6uQqoAIITBABGgwwNTYyNjU5OTQ4NTMiDCvaT%2BoXC%2FCGn665Lyr9AeTcs7ys92tVucvGpOYY0PkdVdcLxa0rS0EAXscjUT36ucCfXw6Gu7Eus6BPjV9xSs4%2BZmCS9DyBn%2BujcDQVLqv%2B5Vl8EdUX4ViK0OsueMPpCbTEXsy4sNGVELF1Rz%2F%2FaV%2BfwgvnfkJm8MJc7Bqz3QaNeh6TpBJL421Vsiv3ccaEpvH8kbNNNWwYJkXQmYbKIpaJT4mCpWdKtmOSGNk31p3P7sC5jLIg5ijCGeqbpbpLhr1dmfFnIPjW5bmxXWQYxqgozbZYxHTYx1OJYdnKw8Pd0LoMhRcChL9jf4DtDles7o6B31IZBaTEqYiZ7lAyxSTN%2FQc%2FhNL3MKhkSrAwp9f4xAY6nQEfBR5OKb%2FwzjR3ZWgs1GeuDraJ8GoI%2BmS8ZkVwBLEWonkO3QE%2FdMmJfn85EpIQHPFrxXjnox9RvGgJPWapZqCiaqMATOtfXKyGPMVU%2F5uJUP9OemUxjIa0W0hnFglJsAww%2B5sp9oOrQUtHQkHiJPURNixGr9sQZH5bV1i6OTYlh25YDxEbP8vhsdcywKaeBAS4m8BMgaLCAUCwsKCo&X-Amz-Signature=7d53a579bb947b8543445de5968ddab6544ff217822062b64e4505bb90e21700",
    )
    result = crowd(job)
    print(result)
