# Base mixin for common functionalities
from http import HTTPStatus
import os

from http import HTTPStatus
import os

class AuthMixin:
    """A mixin to handle authentication and common headers."""
    
    def login(self):
        """Logs the user in and sets up authentication headers."""
        data = {
            "username": os.environ.get("API_USERNAME", "brighton"),
            "password": os.environ.get("API_PASSWORD", "Abungu-7383"),
            "longitude": 36.8219,
            "latitude": -1.2921,
            "accuracy_level": 1000.0,
        }
        with self.client.post(
            url="/api/login/",
            name="Login",
            data=data,
            catch_response=True
        ) as response:
            if response.status_code == HTTPStatus.OK:
                token = response.json()["token"]
                print(f"TOKEN:{token}")
                self.headers.update(
                    {
                        "Authorization": f"Token {token}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "X-Branch": response.json()["branches"][0]["id"],
                        "X-Zone": response.json()["branches"][0]["territories"][0]["id"],
                    }
                )
                response.success()
            else:
                response.failure(f"Login failed: {response.status_code}")

    def logout(self):
        """Logs the user out after the test."""
        self.client.post("/api/logout/", headers=self.headers)

    def on_start(self):
        """Set up headers and authenticate at the beginning."""
        self.headers = {}  # Clear headers per user instance
        self.login()

    # def on_stop(self):
    #     """Log out at the end of the test."""
    #     self.logout()
