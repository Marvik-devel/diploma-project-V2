from itertools import product

from backend.models import Product
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.serializers import UserRegisterSerializer, ProductInfoSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from backend.models import ProductInfo
from backend.models import Order, OrderItem
from backend.serializers import OrderSerializer, OrderItemSerializer
from django.http import JsonResponse


class RegisterView(APIView):
    def post(self, request):

            # 1. Передай входящие данные (они лежат в request.data) в наш сериализатор:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductInfoView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        products = ProductInfo.objects.all()
        serializer = ProductInfoSerializer (products, many=True)
        return Response(serializer.data)


class BasketView(APIView):
    # 1. Получить товары из корзины
    def get(self, request, *args, **kwargs):
        basket = Order.objects.filter(user=request.user, state='basket').first()
        if not basket:
            return JsonResponse({'Status': False, 'Error': 'Корзина пуста'}, status=404)

        serializer = OrderSerializer(basket)
        return Response(serializer.data)

    # 2. Добавить товар в корзину
    def post(self, request, *args, **kwargs):
        product_info_id = request.data.get('product_info_id')
        quantity = request.data.get('quantity', 1)

        if not product_info_id:
            return JsonResponse({'Status': False, 'Error': 'Не указан product_info_id'}, status=400)

        basket, _ = Order.objects.get_or_create(user=request.user, state='basket')
        product_info = ProductInfo.objects.get(id=product_info_id)

        order_item, created = OrderItem.objects.get_or_create(
            order=basket,
            product_info=product_info,
            defaults={'quantity': quantity}
        )

        if not created:
            order_item.quantity += int(quantity)
            order_item.save()

        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data, status=201)

    # 3. Обновить количество товара в корзине
    def put(self, request, *args, **kwargs):
        items_dict = request.data
        if not isinstance(items_dict, list):
            items_dict = [items_dict]

        basket = Order.objects.filter(user=request.user, state='basket').first()
        if not basket:
            return JsonResponse({'Status': False, 'Error': 'Корзина пуста'}, status=404)

        objects_updated = 0
        for item in items_dict:
            item_id = item.get('id')
            quantity = item.get('quantity')

            if item_id and quantity:
                updated_count = OrderItem.objects.filter(
                    order=basket,
                    id=item_id
                ).update(quantity=quantity)

                objects_updated += updated_count

        return JsonResponse({'Status': True, 'Updated objects': objects_updated})

    # 4. Удалить товар из корзины
    def delete(self, request, *args, **kwargs):
        items_dict = request.data
        if not isinstance(items_dict, list):
            items_dict = [items_dict]

        basket = Order.objects.filter(user=request.user, state='basket').first()
        if not basket:
            return JsonResponse({'Status': False, 'Error': 'Корзина не найдена'}, status=404)

        deleted_count = 0
        for item in items_dict:
            item_id = item.get('id')
            if item_id:
                deleted, _ = OrderItem.objects.filter(
                    order=basket,
                    id=item_id
                ).delete()
                deleted_count += deleted

        return JsonResponse({'Status': True, 'Deleted objects': deleted_count})