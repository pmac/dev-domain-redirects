import pytest

import app


@pytest.fixture
def api():
    return app.api


def test_routes(api):
    resp = api.requests.get("/", allow_redirects=False, headers={
        'host': 'pmac.thepy.dev',
    })
    assert resp.status_code == 301
    assert resp.headers['location'] == 'https://pmac.io/'

    resp = api.requests.get("/", allow_redirects=False, headers={
        'host': 'pmac.mozillian.dev',
    })
    assert resp.status_code == 301
    assert resp.headers['location'] == 'https://mozillians.org/u/pmac/'

    # apex domain is an actual page
    resp = api.requests.get("/", allow_redirects=False, headers={
        'host': 'thepy.dev',
    })
    assert resp.status_code == 200

    # only one level of subdomain supported
    resp = api.requests.get("/", allow_redirects=False, headers={
        'host': 'too.many.thepy.dev',
    })
    assert resp.status_code == 404

    # subdomain not in config
    resp = api.requests.get("/", allow_redirects=False, headers={
        'host': 'unknown-one.thepy.dev',
    })
    assert resp.status_code == 404

    # no host
    resp = api.requests.get("/", allow_redirects=False)
    assert resp.status_code == 404
