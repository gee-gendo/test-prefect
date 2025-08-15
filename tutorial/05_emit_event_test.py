from prefect.events import emit_event


def process_file(file_name: str):
    e = emit_event(
        event="custom.file_processed",
        resource={
            "prefect.resource.id": f"file.{file_name}",
            "potatoe.id": "123",
            "name": "chips",
        },
        payload={"file_name": file_name},
        related=[
            {
                "prefect.resource.id": "myresourceid",
                "prefect.resource.role": "myrole",
            }
        ],
    )
    print(e)


if __name__ == "__main__":
    process_file("test4.txt")
