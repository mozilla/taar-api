from flask import url_for
from taar_api.app import app as flask_app
import taar_api.app
import pytest
import uuid


@pytest.fixture
def app():
    return flask_app


class FakeRecommendationManager(object):
    def __init__(self, *args, **kwargs):
        pass


class EmptyRecommendationManager(FakeRecommendationManager):
    def recommend(self, client_id, limit, extra_data={}):
        return []


class StaticRecommendationManager(FakeRecommendationManager):

    # Recommenders must return a list of 2-tuple results
    # with (GUID, weight)
    def recommend(self, client_id, limit, extra_data={}):
        branch_id = extra_data.get('branch', 'control')
        data = {'branch': branch_id}
        result = [
            ('%(branch)s-addon-1' % data, 1.0),
            ('%(branch)s-addon-2' % data, 1.0),
            ('%(branch)s-addon-N' % data, 1.0),
        ]
        return result


class LocaleRecommendationManager(FakeRecommendationManager):

    def recommend(self, client_id, limit, extra_data={}):
        if extra_data.get('locale', None) == "en-US":
            return [('addon-Locale', 1.0)]
        return []


class PlatformRecommendationManager(FakeRecommendationManager):

    def recommend(self, client_id, limit, extra_data={}):
        if extra_data.get('platform', None) == "WOW64":
            return [('addon-WOW64', 1.0)]
        return []


@pytest.fixture
def empty_recommendation_manager(monkeypatch):
    taar_api.app.APP_WRAPPER.set({'PROXY_RESOURCE': EmptyRecommendationManager()})

@pytest.fixture
def static_recommendation_manager(monkeypatch):
    taar_api.app.APP_WRAPPER.set({'PROXY_RESOURCE': StaticRecommendationManager()})


@pytest.fixture
def locale_recommendation_manager(monkeypatch):
    taar_api.app.APP_WRAPPER.set({'PROXY_RESOURCE': LocaleRecommendationManager()})


@pytest.fixture
def platform_recommendation_manager(monkeypatch):
    taar_api.app.APP_WRAPPER.set({'PROXY_RESOURCE': PlatformRecommendationManager()})


def test_empty_recommendation(client, empty_recommendation_manager):
    response = client.get(url_for('recommendations', uuid_client_id=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": []}'


def test_static_recommendation(client, static_recommendation_manager):
    response = client.get(url_for('recommendations', uuid_client_id=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    expected = b'{"results": ["control-addon-1", "control-addon-2", "control-addon-N"]}'
    assert response.data == expected


def test_locale_recommendation(client, locale_recommendation_manager):
    response = client.get(url_for('recommendations', uuid_client_id=uuid.uuid4())+"?locale=en-US")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": ["addon-Locale"]}'

    response = client.get(url_for('recommendations', uuid_client_id=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": []}'


def test_platform_recommendation(client, platform_recommendation_manager):
    uri = url_for('recommendations', uuid_client_id=str(uuid.uuid4()))+"?platform=WOW64"
    response = client.get(uri)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": ["addon-WOW64"]}'

    response = client.get(url_for('recommendations', uuid_client_id=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": []}'


def test_linear_branch(client, static_recommendation_manager):
    url = url_for('recommendations', uuid_client_id=uuid.uuid4())
    response = client.get(url + "?branch=linear")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    expected = b'{"results": ["linear-addon-1", "linear-addon-2", "linear-addon-N"]}'
    assert response.data == expected

    response = client.get(url + "?branch=linear-taar")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    expected = b'{"results": ["linear-addon-1", "linear-addon-2", "linear-addon-N"]}'
    assert response.data == expected


def test_ensemble_branch(client, static_recommendation_manager):
    url = url_for('recommendations', uuid_client_id=uuid.uuid4())
    response = client.get(url + "?branch=ensemble")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    expected = b'{"results": ["ensemble-addon-1", "ensemble-addon-2", "ensemble-addon-N"]}'
    assert response.data == expected

    url = url_for('recommendations', uuid_client_id=uuid.uuid4())
    response = client.get(url + "?branch=ensemble-taar")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    expected = b'{"results": ["ensemble-addon-1", "ensemble-addon-2", "ensemble-addon-N"]}'
    assert response.data == expected


def test_control_branch(client, static_recommendation_manager):
    url = url_for('recommendations', uuid_client_id=uuid.uuid4())
    response = client.get(url + "?branch=control")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    expected = b'{"results": ["control-addon-1", "control-addon-2", "control-addon-N"]}'
    assert response.data == expected
