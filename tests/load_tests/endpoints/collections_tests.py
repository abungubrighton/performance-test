from http import HTTPStatus
from locust import HttpUser, TaskSet, task, between
import os
from tests.load_tests.base.auth_mixin import AuthMixin
from tests.load_tests.base.load_shapes import CustomLoadShape


class CollectionsTasks(TaskSet):
    @task
    def get_collections(self):
        with self.client.get(
            url="/api/collections/",
            headers=self.parent.headers,
            catch_response=True
        ) as response:
            if response.status_code == HTTPStatus.OK:
                try:
                    json_response = response.json()
                    print(f"COLLECTIONS RESPONSE:{json_response["count"]}")
                    assert "results" in json_response
                    assert json_response["count"] >=1
                    response.success()
                except AssertionError:
                    print("ASSERTION ERROR")
                    response.failure("Response does not contain 'collections'")
            else:
                response.failure(f"Failed with status {response.status_code}")

    # @task
    # def create_collection(self):
    #     payload = {"name": "Sample Collection", "description": "Test collection"}
    #     self.client.post("/collections", json=payload)

class CollectionsUser(AuthMixin, HttpUser):
    host = os.environ.get("ENV","https://uat.ibuqa.io")
    tasks = [CollectionsTasks]
    wait_time = between(1, 3)  # Simulate user think time

