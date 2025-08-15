from prefect.deployments import run_deployment

# Basic usage
flow_run = run_deployment(
    name="render/render",
    parameters={
        "job": {
            "seed": 28337543,
            "prompt": "Picasso style painting of a haidresser shop",
            "input_image": "https://gendo-gee-dev.s3.amazonaws.com/test/render-gendo/axo-004.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS6HBCNAF7%2F20250806%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250806T084116Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEDkaCWV1LXdlc3QtMiJGMEQCIFgPIMYpdSe%2FLOwNSd1Qd6zMQpv7x8%2BePxSqYdOVKw6oAiA8mo82CQ1qFAkf0WhVmf4KDC0g2n1pWxjdk6QVgOn%2FICqgAghyEAEaDDA1NjI2NTk5NDg1MyIMdrcNX86CRsDgD7YhKv0ByonTqMlomr21BRSs2d9cqDkMHKoZlstCn5ZrMpqSwgTztHrKtVz0K2JohzJYLfv6B1exQwAhNIlnRYS5t2cKXheSQw%2BdD2C%2BjH3UGNFrBPwvcHSRDvXMk2UJlYWaK7iNsZG2JtfWfiXjCUDKX3%2FhDabv1Cf4aB7sGzUi0RnDU8hmQyk1WWe78bjLCDibRNp8ag9czmBfLVN5HEsrY87Hd2vIiuJ4jaCs8C2xZQSzOJoY0xTK%2FSwWbHOi2mvehSFn%2BYRXpcqT9WqifOQmr%2Fq5yGIs6CEBban8mW%2BJASN1AK4Eslmll6NHofjODMfP1vYruW1JpwSOhDW%2FQB4e%2FjDhqMzEBjqeAQfWf6%2F0wx11LfzvbdsByElQc%2FQxd%2BqkozeCNwbzoiFEzv0VDBBwCA8Vk28SkpESXPs2L3sRHeoufARqjfBVw5JhI9a%2FeAE%2BQnO6lUIasgyki7lF%2BmJOEqqqzgA9bJbhBwrQ5fGUh3f%2BqBl4%2BWguTZnFUrL%2FlfcycbwsDb%2FD5BAdUADKP9MtUCr8lzPr3UvQ%2F4Veu25%2F9d92OaVlUcF7&X-Amz-Signature=70e0da762d822003210c88e4f4089d3b58548cef001be83edd5ebfde71b40a50",
            "upload_url": "https://gendo-gee-dev.s3.amazonaws.com/test/result.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ2GNW6JS6HBCNAF7%2F20250806%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250806T084016Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEDkaCWV1LXdlc3QtMiJGMEQCIFgPIMYpdSe%2FLOwNSd1Qd6zMQpv7x8%2BePxSqYdOVKw6oAiA8mo82CQ1qFAkf0WhVmf4KDC0g2n1pWxjdk6QVgOn%2FICqgAghyEAEaDDA1NjI2NTk5NDg1MyIMdrcNX86CRsDgD7YhKv0ByonTqMlomr21BRSs2d9cqDkMHKoZlstCn5ZrMpqSwgTztHrKtVz0K2JohzJYLfv6B1exQwAhNIlnRYS5t2cKXheSQw%2BdD2C%2BjH3UGNFrBPwvcHSRDvXMk2UJlYWaK7iNsZG2JtfWfiXjCUDKX3%2FhDabv1Cf4aB7sGzUi0RnDU8hmQyk1WWe78bjLCDibRNp8ag9czmBfLVN5HEsrY87Hd2vIiuJ4jaCs8C2xZQSzOJoY0xTK%2FSwWbHOi2mvehSFn%2BYRXpcqT9WqifOQmr%2Fq5yGIs6CEBban8mW%2BJASN1AK4Eslmll6NHofjODMfP1vYruW1JpwSOhDW%2FQB4e%2FjDhqMzEBjqeAQfWf6%2F0wx11LfzvbdsByElQc%2FQxd%2BqkozeCNwbzoiFEzv0VDBBwCA8Vk28SkpESXPs2L3sRHeoufARqjfBVw5JhI9a%2FeAE%2BQnO6lUIasgyki7lF%2BmJOEqqqzgA9bJbhBwrQ5fGUh3f%2BqBl4%2BWguTZnFUrL%2FlfcycbwsDb%2FD5BAdUADKP9MtUCr8lzPr3UvQ%2F4Veu25%2F9d92OaVlUcF7&X-Amz-Signature=a86be6535bfd3f2ca6ca6b18be0049481754525fa5235d699bdb5496500ff631",
        }
    },
)
print(flow_run.id)
# # With parameters
# flow_run = run_deployment(
#     name="my-flow/my-deployment",
#     parameters={
#         "my_param": 42,
#         "another_param": "hello"
#     }
# )

# # With job variables (environment variables, etc.)
# flow_run = run_deployment(
#     name="my-flow/my-deployment",
#     parameters={"my_param": 42},
#     job_variables={"env": {"MY_ENV_VAR": "production"}}
# )

# # Don't wait for completion
# flow_run = run_deployment(
#     name="my-flow/my-deployment",
#     timeout=0  # returns immediately
# )

# # Wait with custom timeout (seconds)
# flow_run = run_deployment(
#     name="my-flow/my-deployment",
#     timeout=300  # wait up to 5 minutes
# )

# # Schedule for later
# from datetime import datetime, timedelta

# flow_run = run_deployment(
#     name="my-flow/my-deployment",
#     scheduled_time=datetime.now() + timedelta(hours=2)
# )

# # With custom tags
# flow_run = run_deployment(
#     name="my-flow/my-deployment",
#     tags=["production", "critical"]
# )
