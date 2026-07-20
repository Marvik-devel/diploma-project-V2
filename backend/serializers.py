from rest_framework import serializers
from backend.models import User, ProductInfo
from backend.models import OrderItem


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


class OrderItemSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer(read_only=True)

    # Заменяем IntegerField на PrimaryKeyRelatedField!
    # Теперь DRF сам проверит наличие товара в базе
    product_info_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductInfo.objects.all(),
        source='product_info',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'product_info_id', 'quantity', 'order')
        extra_kwargs = {
            'order': {'read_only': True}
        }

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество товара должно быть больше 0.")
        return value