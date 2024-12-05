from locust import LoadTestShape
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomLoadShape(LoadTestShape):
    """
        CustomLoadShape defines a load test with three stages:
        - Ramp-up: Gradually increase the number of users.
        - Steady: Maintain a constant number of users.
        - Ramp-down: Gradually decrease the number of users.

        Attributes:
            stages (list of dict): Defines the stages of the load test. Each stage includes:
                - duration (int): The duration of the stage in seconds.
                - users (int): The number of users active during the stage.
                - spawn_rate (float): The rate at which users are added or removed (users per second).

        Methods:
            tick(): Determines the current stage of the test based on elapsed runtime and returns the user count and spawn rate.
    """
    stages = [
        {"duration": 60, "users": 30, "spawn_rate": 1},  # Ramp-up: Add 10 users to the system gradually over 1 minute (1 user per second).
        {"duration": 300, "users": 30, "spawn_rate": 0}, # Steady: Keep 10 users active in the system for 5 minutes, with no new users joining.
        {"duration": 60, "users": 0, "spawn_rate": 2},   # Ramp-down: Remove all users from the system over 1 minute (2 users per second).
    ]

    def tick(self):
        run_time = self.get_run_time()

        for index, stage in enumerate(self.stages):
            if run_time < stage["duration"]:
                users, spawn_rate = stage["users"], stage["spawn_rate"]
                logger.info(f"[{run_time:.2f}s] Stage {index + 1}: {users} users, spawn_rate={spawn_rate}/s")
                return users, spawn_rate
            run_time -= stage["duration"]

        return None
