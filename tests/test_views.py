# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
from flask import url_for
import pytest
import uuid

from taar_api.app import app as flask_app


@pytest.fixture
def app():
    return flask_app


class EmptyRecommendationManager:
    def recommend(self, client_data, limit):
        return []


class NormalRecommendationManager:
    def recommend(self, client_data, limit):
        return [("some_guid", 20),
                ("another_guid", 10),
                ("another_guid1", 5),
                ("another_guid2", 1)]


class ShortRecommendationManager:
    def recommend(self, client_data, limit):
        return [("some_guid", 2), ("another_guid", 1)]


@pytest.fixture
def empty_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar_api.app.PROXY_MANAGER._resource',
                        EmptyRecommendationManager())


@pytest.fixture
def normal_recommendation_manager(monkeypatch):
    """ A recommendation manager that only returns 2 results (less
    than MAX of 4)
    """
    monkeypatch.setattr('taar_api.app.PROXY_MANAGER._resource',
                        NormalRecommendationManager())


@pytest.fixture
def short_recommendation_manager(monkeypatch):
    """ A recommendation manager that only returns 2 results (less
    than MAX of 4)
    """
    monkeypatch.setattr('taar_api.app.PROXY_MANAGER._resource',
                        ShortRecommendationManager())


def test_minimal_request(client, empty_recommendation_manager):
    response = client.get(url_for('recommendations', guid=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": []}'


def test_short_request_limit(client, short_recommendation_manager):
    """Recommendations that return less than the max number of results
    should truncate the result list to the empty list.
    """
    response = client.get(url_for('recommendations', guid=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": []}'


def test_normal_request_limit(client, normal_recommendation_manager):
    response = client.get(url_for('recommendations', guid=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    results = json.loads(response.data.decode('utf8'))['results']
    assert len(results) == 4
