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

    def recommend(self, *args, **kwargs):
        return []


class StaticRecommendationManager(FakeRecommendationManager):

    def recommend(self, *args, **kwargs):
        return [
            'addon-1',
            'addon-2',
            'addon-N',
        ]


class LocaleRecommendationManager(FakeRecommendationManager):

    def recommend(self, *args, **kwargs):
        assert len(args) >= 3
        if args[2].get('locale', None) == "en-US":
            return ['addon-Locale']
        return []


class PlatformRecommendationManager(FakeRecommendationManager):

    def recommend(self, *args, **kwargs):
        assert len(args) >= 3
        if args[2].get('platform', None) == "WOW64":
            return ['addon-WOW64']
        return []


@pytest.fixture
def empty_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar.recommenders.RecommendationManager', EmptyRecommendationManager)


@pytest.fixture
def static_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar.recommenders.RecommendationManager', StaticRecommendationManager)


@pytest.fixture
def locale_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar.recommenders.RecommendationManager', LocaleRecommendationManager)


@pytest.fixture
def platform_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar.recommenders.RecommendationManager', PlatformRecommendationManager)


def test_empty_recommendation(dummy_cache, client, empty_recommendation_manager):
    response = client.get(reverse('recommendations', kwargs={'client_id': str(uuid.uuid4())}))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": []}'


def test_static_recommendation(dummy_cache, client, static_recommendation_manager):
    response = client.get(reverse('recommendations', kwargs={'client_id': str(uuid.uuid4())}))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response.content == b'{"results": ["addon-1", "addon-2", "addon-N"]}'


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
