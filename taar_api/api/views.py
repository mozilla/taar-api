from django.conf import settings
from django.http import JsonResponse

from taar import recommenders
from taar.profile_fetcher import ProfileFetcher
from taar.dynamo import ProfileController

# Cache the recommendation manager for 24hrs (in seconds).
VALID_BRANCHES = set(['linear', 'ensemble', 'control'])

RECOMMENDATION_MANAGER = None


def recommendations(request, client_id):
    """Return a list of recommendations provided a telemetry client_id."""
    # Use the module global RECOMMENDATION_MANAGER
    global RECOMMENDATION_MANAGER

    branch = request.GET.get('branch', '')

    if branch not in VALID_BRANCHES:
        # Force branch to be a control branch if an invalid request
        # comes in.
        branch = 'control'

    extra_data = {'branch': branch}

    locale = request.GET.get('locale', None)
    if locale is not None:
        extra_data['locale'] = locale

    platform = request.GET.get('platform', None)
    if platform is not None:
        extra_data['platform'] = platform

    if RECOMMENDATION_MANAGER is None:
        dynamo_client = ProfileController(region_name=settings.DYNAMO_REGION,
                                          table_name=settings.DYNAMO_TABLE_NAME)
        profile_fetcher = ProfileFetcher(dynamo_client)
        RECOMMENDATION_MANAGER = recommenders.RecommendationManager(profile_fetcher)
    recommendations = RECOMMENDATION_MANAGER.recommend(client_id,
                                                       limit=settings.TAAR_MAX_RESULTS,
                                                       extra_data=extra_data)
    return JsonResponse({"results": recommendations})
