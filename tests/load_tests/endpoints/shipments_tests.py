from http import HTTPStatus
from locust import HttpUser, TaskSet, task, between
import os
import logging
from tests.load_tests.base.auth_mixin import AuthMixin
from tests.load_tests.base.load_shapes import CustomLoadShape
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShipmentTasks(TaskSet):
    @task
    def get_shipments(self):
        with self.client.get(
            url="/api/shipment/",
            headers=self.parent.headers,
            catch_response=True
        ) as response:
            if response.status_code == HTTPStatus.OK:
                try:
                    json_response = response.json()
                    logger.info(f"SHIPMENTS RESPONSE: {json_response['count']}")
                    assert "results" in json_response, "Key 'results' is missing"
                    assert json_response["count"] >= 1, "Count is less than 1"
                    response.success()
                except AssertionError as e:
                    logger.error(f"ASSERTION ERROR: {e}")
                    response.failure(str(e))
            else:
                response.failure(f"Failed with status {response.status_code}")

class ShipmentUser(AuthMixin, HttpUser):
    host = os.environ.get("ENV") or "https://uat.ibuqa.io"
    tasks = [ShipmentTasks]
    wait_time = between(1, 5)
