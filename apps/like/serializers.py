from rest_framework import serializers
from .models import Like


class CurrentPostDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['products']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    products = serializers.HiddenField(default=CurrentPostDefault())
    
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        products = self.context.get('post').pk
        like = Like.objects.filter(user=user, products=products).first()
        if like:
            raise serializers.ValidationError('Already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        products = self.context.get('post').pk
        like = Like.objects.filter(user=user, products=products).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('Not liked yet')