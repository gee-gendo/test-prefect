from prefect.blocks.notifications import CustomWebhookNotificationBlock

hook = CustomWebhookNotificationBlock(
    name="my-alert",
    url="https://example.com/webhook",
    method="POST",
    json_data={"text": "Hello from Prefect"},
)
hook.save("my-alert")  # select this block in an Automation action
