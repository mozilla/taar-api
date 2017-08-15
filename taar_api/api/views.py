from django.conf import settings
from django.http import JsonResponse

from taar.recommenders import RecommendationManager


def recommendations(request, client_id):
    recommendations = []
    # Use addon recommender.
    recommendation_manager = RecommendationManager()
    recommendations = recommendation_manager.recommend(client_id, settings.TAAR_MAX_RESULTS)
    return JsonResponse({"results": recommendations})
