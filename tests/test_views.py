from flask import url_for
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


@pytest.mark.skip("move this to taar library")
def test_empty_recommendation(client, empty_recommendation_manager):
    response = client.get(url_for('recommendations', uuid_client_id=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": []}'


@pytest.mark.skip("move this to taar library")
def test_locale_recommendation(client, locale_recommendation_manager):
    response = client.get(url_for('recommendations', uuid_client_id=uuid.uuid4())+"?locale=en-US")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": ["addon-Locale"]}'

    response = client.get(url_for('recommendations', uuid_client_id=uuid.uuid4()))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == b'{"results": []}'


@pytest.mark.skip("move this to taar library")
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


@pytest.mark.skip("move this to taar library")
def test_intervention_a(client, static_recommendation_manager):
    url = url_for('recommendations', uuid_client_id=uuid.uuid4())
    response = client.get(url + "?branch=intervention-a")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    expected = b'{"results": ["intervention-a-addon-1", "intervention-a-addon-2", "intervention-a-addon-N"]}'
    assert response.data == expected


@pytest.mark.skip("move this to taar library")
def test_intervention_b(client, static_recommendation_manager):
    url = url_for('recommendations', uuid_client_id=uuid.uuid4())
    response = client.get(url + "?branch=intervention_b")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    expected = b'{"results": ["intervention_b-addon-1", "intervention_b-addon-2", "intervention_b-addon-N"]}'
    assert response.data == expected


@pytest.mark.skip("move this to taar library")
def test_control_branch(client, static_recommendation_manager):
    url = url_for('recommendations', uuid_client_id=uuid.uuid4())
    response = client.get(url + "?branch=control")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    expected = b'{"results": ["control-addon-1", "control-addon-2", "control-addon-N"]}'
    assert response.data == expected
