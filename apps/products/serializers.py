from rest_framework import serializers
from .models import Product, ProductImage, Category

from .permissions import IsStaff

from apps.review.serializers import CommentSerializer

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
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['comments_count'] = instance.comments.all().count()
        return rep


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments_count'] = instance.comments.all().count()
        return rep


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
        # exclude = ('tag', )

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
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title')


class HomepageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('user', 'title', 'image', 'slug', 'views_count')
        # Article.objects.filter(max('views_count'))

    # def to_representation(self, instance):
    #     instance = super().to_representation(instance)
    #     print(instance)
    #     return instance


class ProductSerializerTop(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('user_id', 'title', 'image', 'slug', 'views_count')

# {
#     'user': 
#     'title': 123123,
#     'priuce': 12341234
# }