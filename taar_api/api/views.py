from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse

from taar import recommenders
from taar.profile_fetcher import ProfileFetcher
from taar.hbase_client import HBaseClient

# Cache the recommendation manager for 24hrs (in seconds).
CACHE_EXPIRATION = 24 * 60 * 60


def recommendations(request, client_id):
    """Return a list of recommendations provided a telemetry client_id."""
    recommendation_manager = cache.get("recommendation_manager")
    if recommendation_manager is None:
        hbase_client = HBaseClient(settings.HBASE_HOST)
        profile_fetcher = ProfileFetcher(hbase_client)
        recommendation_manager = recommenders.RecommendationManager(profile_fetcher)
        cache.set("recommendation_manager",
                  recommendation_manager,
                  CACHE_EXPIRATION)
    recommendations = recommendation_manager.recommend(client_id, settings.TAAR_MAX_RESULTS)
    return JsonResponse({"results": recommendations})
