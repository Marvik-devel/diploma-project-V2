from rest_framework import serializers
from backend.models import User, ProductInfo


class UserRegisterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop ('password', None)
        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'company', 'position', 'type')
        extra_kwargs = {'password': {'write_only': True}}

class ProductInfoSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'external_id', 'shop', 'product', 'price', 'price_rrt', 'quantity')
