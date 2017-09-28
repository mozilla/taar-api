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


@pytest.fixture
def empty_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar.recommenders.RecommendationManager', EmptyRecommendationManager)


@pytest.fixture
def static_recommendation_manager(monkeypatch):
    monkeypatch.setattr('taar.recommenders.RecommendationManager', StaticRecommendationManager)


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
