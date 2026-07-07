from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.serializers import UserRegisterSerializer


class RegisterView(APIView):
    def post(self, request):

            # 1. Передай входящие данные (они лежат в request.data) в наш сериализатор:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # 2. Проверь данные на валидность. У сериализатора есть метод is_valid().
            # Если данные валидны:
            #    а) вызови метод serializer.save() (он создаст пользователя)
            #    б) верни Response с данными пользователя (serializer.data) и статусом status.HTTP_201_CREATED

            # 3. Если данные НЕ валидны:
            #    а) верни Response с ошибками (serializer.errors) и статусом status.HTTP_400_BAD_REQUEST

            # Твой код ниже:


# Create your views here.
