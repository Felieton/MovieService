from django.urls import include, path
from rest_framework import routers
from django.views.generic.base import RedirectView
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'castRoles', views.CastRoleViewSet, basename='cast_role')
router.register(r'castMembers', views.CastMemberViewSet, basename='cast_member')
router.register(r'characters', views.CharacterViewSet, basename='character')
router.register(r'requestLogs', views.RequestLogViewSet, basename='request_log')
router.register(r'people', views.PersonViewSet, basename='person')
router.register(r'personRequests', views.PersonRequestViewSet, basename='person_request')
router.register(r'titles', views.TitleViewSet, basename='title')
router.register(r'titleRequests', views.TitleRequestViewSet, basename='title_request')
router.register(r'languages', views.LangViewSet, basename='lang')
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'countries', views.CountryViewSet, basename='country')
router.register(r'actionLogs', views.ActionLogViewSet, basename='action_log')
router.register(r'episodes', views.EpisodeViewSet, basename='episode')
router.register(r'episodeRequests', views.EpisodeRequestViewSet, basename='episode_request')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'groups', views.GroupViewSet, basename='group')
router.register(r'achievements', views.AchievementViewSet, basename='achievement')
router.register(r'scraperSites', views.ScraperSitesViewSet, basename='scraper_sites')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', RedirectView.as_view(url='api/', permanent=True)),
    path('api/', include(router.urls)),
    # browsable api login; needs session auth backend
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
