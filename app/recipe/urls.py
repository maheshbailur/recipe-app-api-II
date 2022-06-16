"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

"""creating and registering app to default router
"""
router = DefaultRouter()
"""This will create all the end points for each CRUD operation
prefixed with recipes"""
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)

"""Below line used for the creation of reverse url used for testing"""
app_name = 'recipe'

"""to include all the urls created by router
which are available for processing request at endpoint"""
urlpatterns = [
    path('', include(router.urls)),
]