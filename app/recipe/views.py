"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import(
    Recipe,
    Tag,
    Ingredient,
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
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class


    """perform_create method is called while creating the object in ModelViewSet
    https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself"""
    def perform_create(self, serializer):
        """Create a new recipe."""

        """This will save the user as current authenticated user,
        when we create a recipe"""
        serializer.save(user=self.request.user)

    """decorator function for handling upload image endpoint
    used with POST request, specific recipe-id(detail) required"""
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes like Tags and Ingradients."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


"""mixin provides additional functionality. ListModelMixin, specific for listing models
GenericViewSet, along with CRUD operations, it provides desired functionality for our api  """
class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()