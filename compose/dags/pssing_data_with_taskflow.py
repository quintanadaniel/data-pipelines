import time

from airflow.utils.dates import days_ago
from airflow.decorators import dag, task

default_args = {
    "owner": "daniel quintana"
}


@dag(
    dag_id="passing_data_with_taskflow",
    description="XCom using TaskFlow API",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=["xcom", "python", "taskflow_api"]
)
def passing_data_with_taskflow_api():
    @task
    def get_order_prices():
        order_price_data = {
            'o1': 234.5,
            'o2': 10.00,
            'o3': 34.77,
            'o4': 45.66,
            'o5': 399
        }

        return order_price_data

    @task
    def compute_sum(order_price_data: dict):
        total = sum(order_price_data[order] for order in order_price_data)
        return total

    @task
    def compute_average(order_price_data: dict):
        total = 0
        count = 0
        for order in order_price_data:
            total += order_price_data[order]
            count += 1

        average = total / count

        return average

    @task
    def display_results(total, average):
        print(f"Total price of goods: {total}")
        print(f"Average price of goods: {average}")

    order_price_data = get_order_prices()

    total = compute_sum(order_price_data)
    average = compute_average(order_price_data)

    display_results(total, average)


passing_data_with_taskflow_api()
