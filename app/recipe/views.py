"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import(
    Recipe,
    Tag,
)
from recipe import serializers

"""ModelViewSet used with specific model definition like Recipe
ModelViewSet gives already defined logic for CRUD operation"""
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """By default get_queryset returns all the objects in the db
    we have override this function to return only the objects/recipe
    of the logged-in/current user"""
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    """Below method available in django documentation
    which returns serializer class to be used"""
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
            """self.serializer_class = serializers.RecipeSerializer, check this code"""

        return self.serializer_class


    """perform_create method is called while creating the object in ModelViewSet
    https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself"""
    def perform_create(self, serializer):
        """Create a new recipe."""

        """This will save the user as current authenticated user,
        when we create a recipe"""
        serializer.save(user=self.request.user)

"""mixin provides additional functionality. ListModelMixin, specific for listing models
GenericViewSet, along with CRUD operations, it provides desired functionality for our api  """
class TagViewSet(mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
