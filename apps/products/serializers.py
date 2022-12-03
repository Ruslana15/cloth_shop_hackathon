from rest_framework import serializers
from .models import Product, ProductImage, Category
from apps.review.serializers import CommentSerializer
from apps.like.serializers import LikeSerializer


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise serializers.ValidationError('Количество не может быть отрицательным')
        return quantity

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments_count'] = instance.comments.all().count()
        representation['comments'] = CommentSerializer(
            instance.comments.all(), many=True
        ).data
        representation['carousel'] = ProductImageSerializer(
            instance.product_images.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['liked_by'] = LikeSerializer(
            instance.likes.all().only('user'), many=True).data
        # rating = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        # if rating:
        #     representation['rating'] = round(rating, 1)
        # else:
        #     representation['rating'] = 0.0
        # {'rating__avg': 3.4}
        return representation


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug', 'parent_category')


class ProductFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title')


# {
#     'user': 
#     'title': 123123,
#     'priuce': 12341234
# }


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = 'image',