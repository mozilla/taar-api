import uuid

import pytest
from django.core.urlresolvers import reverse


@pytest.fixture
def dummy_cache(settings):
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


class FakeRecommendationManager(object):

    def __init__(self, *args, **kwargs):
        pass


class EmptyRecommendationManager(FakeRecommendationManager):

    def recommend(self, client_id, limit, extra_data={}):
        return []


class StaticRecommendationManager(FakeRecommendationManager):

    def recommend(self, client_id, limit, extra_data={}):
        branch_id = extra_data.get('branch', 'control')
        data = {'branch': branch_id}
        return [
            '%(branch)s-addon-1' % data,
            '%(branch)s-addon-2' % data,
            '%(branch)s-addon-N' % data,
        ]


class LocaleRecommendationManager(FakeRecommendationManager):

    def recommend(self, client_id, limit, extra_data={}):
        if extra_data.get('locale', None) == "en-US":
            return ['addon-Locale']
        return []


class PlatformRecommendationManager(FakeRecommendationManager):

    def recommend(self, client_id, limit, extra_data={}):
        if extra_data.get('platform', None) == "WOW64":
            return ['addon-WOW64']
        return []


@pytest.fixture
def empty_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar_api.api.views.PROXY_MANAGER._resource',
                        EmptyRecommendationManager())


@pytest.fixture
def static_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar_api.api.views.PROXY_MANAGER._resource',
                        StaticRecommendationManager())


@pytest.fixture
def locale_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar_api.api.views.PROXY_MANAGER._resource',
                        LocaleRecommendationManager())


@pytest.fixture
def platform_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar_api.api.views.PROXY_MANAGER._resource',
                        PlatformRecommendationManager())


def test_empty_recommendation(dummy_cache, client, empty_recommendation_manager):
    response = client.get(reverse('recommendations', kwargs={'client_id': str(uuid.uuid4())}))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": []}'


def test_static_recommendation(dummy_cache, client, static_recommendation_manager):
    response = client.get(reverse('recommendations', kwargs={'client_id': str(uuid.uuid4())}))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": ["control-addon-1", "control-addon-2", "control-addon-N"]}'


def test_locale_recommendation(dummy_cache, client, locale_recommendation_manager):
    kwargs = {'client_id': str(uuid.uuid4())}
    response = client.get(reverse('recommendations', kwargs=kwargs), {'locale': 'en-US'})
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": ["addon-Locale"]}'

    kwargs = {'client_id': str(uuid.uuid4())}
    response = client.get(reverse('recommendations', kwargs=kwargs))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": []}'


def test_platform_recommendation(dummy_cache, client, platform_recommendation_manager):
    kwargs = {'client_id': str(uuid.uuid4())}
    response = client.get(reverse('recommendations', kwargs=kwargs), {'platform': 'WOW64'})
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": ["addon-WOW64"]}'

    kwargs = {'client_id': str(uuid.uuid4())}
    response = client.get(reverse('recommendations', kwargs=kwargs))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": []}'


def test_linear_branch(dummy_cache, client, static_recommendation_manager):
    url = reverse('recommendations', kwargs={'client_id': str(uuid.uuid4())})
    response = client.get(url + "?branch=linear")
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": ["linear-addon-1", "linear-addon-2", "linear-addon-N"]}'


def test_ensemble_branch(dummy_cache, client, static_recommendation_manager):
    url = reverse('recommendations', kwargs={'client_id': str(uuid.uuid4())})
    response = client.get(url + "?branch=ensemble")
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": ["ensemble-addon-1", "ensemble-addon-2", "ensemble-addon-N"]}'


def test_control_branch(dummy_cache, client, static_recommendation_manager):
    url = reverse('recommendations', kwargs={'client_id': str(uuid.uuid4())})
    response = client.get(url + "?branch=control")
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": ["control-addon-1", "control-addon-2", "control-addon-N"]}'
