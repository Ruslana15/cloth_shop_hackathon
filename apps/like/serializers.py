from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Like
        fields = '__all__'

    def created(self):
        user = self.context.get('request').user
        product = self.context.get('request').data.get('product')
        # like = Like.objects.filter(user=user).first()
        like = Like.objects.filter(user=user, product=product).first()
        if like:
            raise serializers.ValidationError('Already liked')
        return Like.objects.create(product=product, user=user)
        
    def unlike(self):
        user = self.context.get('request').user
        product = self.context.get('request').data.get('product')
        like = Like.objects.filter(user=user, product=product).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('Not liked yet')