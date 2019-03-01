import pytest

import app


@pytest.fixture
def api():
    return app.api


def test_routes(api):
    resp = api.requests.get("/", allow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers['location'] == 'https://pmac.io/'

    resp = api.requests.get("/dude", allow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers['location'] == 'https://pmac.io/'

    resp = api.requests.get("/dude/", allow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers['location'] == 'https://pmac.io/'
