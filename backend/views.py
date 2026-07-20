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
from rest_framework.permissions import IsAuthenticated  # Для фейсконтроля по токену
from backend.models import Order, OrderItem
from backend.serializers import OrderItemSerializer


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

class BaseView(APIView):
    permission_classes = [IsAuthenticated]


class BasketView(APIView):
    #  токен! (401 Unauthorized)
    permission_classes = [IsAuthenticated]

    # --- ПОЛУЧЕНИЕ КОРЗИНЫ (GET) ---
    def get(self, request):
        #корзину текущего пользователя
        basket = Order.objects.filter(user=request.user, state='basket').first()

        if not basket:
            return Response([])

        items = OrderItem.objects.filter(order=basket)
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)

    # добавление товара в корзину
    def post(self, request):
        # Находим корзину или создаем новую, если у юзера её еще нет
        basket, created = Order.objects.get_or_create(user=request.user, state='basket')

        serializer = OrderItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(order=basket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
