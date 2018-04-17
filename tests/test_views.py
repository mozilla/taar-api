from flask import url_for
from taar_api.app import app as flask_app
import pytest
import uuid


@pytest.fixture
def app():
    return flask_app


class EmptyRecommendationManager:
    def recommend(self, client_data, limit):
        return []


@pytest.fixture
def empty_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar_api.app.PROXY_MANAGER._resource',
                        EmptyRecommendationManager())


def test_minimal_request(client, empty_recommendation_manager):
    response = client.get(url_for('recommendations', guid=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": []}'
