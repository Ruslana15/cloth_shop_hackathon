from rest_framework import serializers
from .models import Product, ProductImage, Category

from .permissions import IsStaff

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
        fields = ('slug', 'image', 'title', 'price', 'likes', 'views_count')


class ProductCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    carousel_img = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )
    permission_classes = [IsStaff]

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        # tag = validated_data.pop('tag')
        product = Product.objects.create(**validated_data)
        # product.tag.set(tag)
        images = []
        for image in carousel_images:
            images.append(ProductImage(article=Product, image=image))
        ProductImage.objects.bulk_create(images)
        return product

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'image', 
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug', 'parent_category')


class ProductFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', )


class HomepageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('user', 'title', 'image', 'slug', 'views_count')
        # Article.objects.filter(max('views_count'))

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        # print(instance)
        return instance


class ProductSerializerTop(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('user_id', 'title', 'image', 'slug', 'views_count')

# {
#     'user': 
#     'title': 123123,
#     'priuce': 12341234
# }