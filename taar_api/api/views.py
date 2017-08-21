from django.conf import settings
from django.http import JsonResponse

from taar.recommenders import RecommendationManager
from taar.profile_fetcher import ProfileFetcher
from taar.hbase_client import HBaseClient


def recommendations(request, client_id):
    """Return a list of recommendations provided a telemetry client_id."""
    hbase_client = HBaseClient(settings.HBASE_HOST)
    profile_fetcher = ProfileFetcher(hbase_client)
    recommendation_manager = RecommendationManager(profile_fetcher)
    recommendations = recommendation_manager.recommend(client_id, settings.TAAR_MAX_RESULTS)
    return JsonResponse({"results": recommendations})
