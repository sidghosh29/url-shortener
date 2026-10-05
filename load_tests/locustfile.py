from locust import HttpUser, between, task


class UrlShortenerUser(HttpUser):
    wait_time = between(0.9, 1.1)

    @task
    def create_short_url(self):
        response = self.client.post(
            "/shorten",
            json={
                "url": "https://www.google.com",
            },
            name="POST /shorten",
        )

        if response.status_code != 201:
            response.failure(f"Expected 201, got {response.status_code}")
