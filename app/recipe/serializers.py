"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Recipe

"""To serialize speific recipe model use ModelSerializer"""
class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    """specify the model we are going to use"""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


"""RecipeDetailSerializer is based from RecipeSerializer
becaus eits almost same and we are going add few more fields to it"""
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']