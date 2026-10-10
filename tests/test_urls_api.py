def test_create_short_url(client, auth_headers):
    response = client.post(
        "/api/shorten",
        json={"url": "https://www.google.com"},
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert "short_code" in data
    assert "short_url" in data


def test_short_url_redirect(client, auth_headers):
    # First, create a short URL
    response = client.post(
        "/api/shorten",
        json={"url": "https://www.google.com"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    short_code = data["short_code"]

    # Redirect Testing
    redirect_response = client.get(f"/api/{short_code}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://www.google.com/"
