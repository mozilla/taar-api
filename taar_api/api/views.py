from django.conf import settings
from django.http import JsonResponse

from taar import recommenders
from taar.profile_fetcher import ProfileFetcher
from taar import ProfileController

# Cache the recommendation manager for 24hrs (in seconds).
VALID_BRANCHES = set(['linear', 'ensemble', 'control'])


class ResourceProxy(object):
    def __init__(self):
        self._resource = None

    def setResource(self, rsrc):
        self._resource = rsrc

    def getResource(self):
        return self._resource


PROXY_MANAGER = ResourceProxy()


def recommendations(request, client_id):
    """Return a list of recommendations provided a telemetry client_id."""
    # Use the module global PROXY_MANAGER
    global PROXY_MANAGER

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

    if PROXY_MANAGER.getResource() is None:
        dynamo_client = ProfileController(region_name=settings.DYNAMO_REGION,
                                          table_name=settings.DYNAMO_TABLE_NAME)
        profile_fetcher = ProfileFetcher(dynamo_client)
        r_factory = recommenders.RecommenderFactory()
        instance = recommenders.RecommendationManager(r_factory, profile_fetcher)
        PROXY_MANAGER.setResource(instance)

    instance = PROXY_MANAGER.getResource()
    recommendations = instance.recommend(client_id=client_id,
                                         limit=settings.TAAR_MAX_RESULTS,
                                         extra_data=extra_data)
    # Strip out weights from TAAR results to maintain compatibility
    # with TAAR 1.0
    return JsonResponse({"results": [x[0] for x in recommendations]})
