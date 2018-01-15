from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse

from taar import recommenders
from taar.profile_fetcher import ProfileFetcher
from taar.hbase_client import HBaseClient

# Cache the recommendation manager for 24hrs (in seconds).
CACHE_EXPIRATION = 24 * 60 * 60
VALID_BRANCHES = set(['linear', 'ensemble', 'control'])


def recommendations(request, client_id):
    """Return a list of recommendations provided a telemetry client_id."""
    branch = request.GET.get('branch', '')

    if branch not in VALID_BRANCHES:
        # Force branch to be a control branch if an invalid request
        # comes in.
        branch = 'control'

    recommendation_manager = cache.get("recommendation_manager")

    extra_data = {'branch': branch}

    locale = request.GET.get('locale', None)
    if locale is not None:
        extra_data['locale'] = locale

    platform = request.GET.get('platform', None)
    if platform is not None:
        extra_data['platform'] = platform

    if recommendation_manager is None:
        hbase_client = HBaseClient(settings.HBASE_HOST)
        profile_fetcher = ProfileFetcher(hbase_client)
        recommendation_manager = recommenders.RecommendationManager(profile_fetcher)
        cache.set("recommendation_manager",
                  recommendation_manager,
                  CACHE_EXPIRATION)
    recommendations = recommendation_manager.recommend(client_id,
                                                       limit=settings.TAAR_MAX_RESULTS,
                                                       extra_data=extra_data)
    return JsonResponse({"results": recommendations})
