from prefect import flow, task
import random
import time

@task
def get_customer_ids(num: int) -> list[str]:
    # Fetch customer IDs from a database or API
    return [f"customer{n}" for n in random.choices(range(100), k=num)]


@task
def process_customer(customer_id: str) -> str:
    # Process a single customer
    time.sleep(1)
    return f"Processed {customer_id}"


@flow
def main() -> list[str]:
    customer_ids = get_customer_ids(10)
    # Map the process_customer task across all customer IDs
    results = process_customer.map(customer_ids)
    return results


if __name__ == "__main__":
    main()
