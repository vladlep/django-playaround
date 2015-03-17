from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest_framework.routers import SimpleRouter
from costs.api_views import CostViewSet

admin.autodiscover()

api_v1 = SimpleRouter()
api_v1.register('costs', CostViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'playaround.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_v1.urls)),
)
