# Base task set for reusable tasks
from http import HTTPStatus
from locust import TaskSet


class BaseTasks(TaskSet):
    """Base task set with common task utilities."""
    
    def get_resource(self, url: str, name: str):
        """Reusable GET request handler."""
        with self.client.get(
            url=url,
            headers=self.parent.headers,
            name=name,
            catch_response=True
        ) as response:
            if response.status_code == HTTPStatus.OK:
                try:
                    json_response = response.json()
                    print(f"GET {name.upper()} RESPONSE: {json_response}")
                    assert "results" in json_response
                    assert json_response["count"] >= 1
                    response.success()
                except AssertionError as e:
                    response.failure(f"Assertion error: {str(e)}")
            else:
                response.failure(f"Failed with status {response.status_code}")