"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


"""To serialize speific recipe model use ModelSerializer"""
class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    """tags used as a field in RecipeSerializer,
    TagSerializer inside RecipeSerializer [nested Serializer]
    A recipe can have multiple tags, so many=True but tag not mandatory for a recipe"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    """specify the model we are going to use"""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags', 'ingredients']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""

        """get the current logged in user"""
        auth_user = self.context['request'].user
        for tag in tags:
            """First check the tag exists, if not exists then create in Tag table
            if tag exist then just get that tag from db.
            Then save passed tags in recipe tag field"""
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients as needed."""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    """While creating a new recipe, check the tags in that recipe
    (if provided) to avoid duplication"""
    def create(self, validated_data):
        """Create a recipe."""

        """collect the tags from the request"""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])

        """create the recipe (without tags, later will add
        this field in _get_or_create_tags().)"""
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    """Update all the previous Tags/Ingradients for this recipe
    with the ones passed now"""
    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


"""RecipeDetailSerializer is based from RecipeSerializer
becaus eits almost same and we are going add few more fields to it"""
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


