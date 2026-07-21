from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from backend.models import Category, Shop, Product, ProductInfo, Order, OrderItem

User = get_user_model()


class BasketAPITestCase(APITestCase):
    def setUp(self):
        # 1. Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.client.force_authenticate(user=self.user)

        # 2. Создаем тестовые данные
        self.category = Category.objects.create(name='Тестовая категория')
        self.shop = Shop.objects.create(name='Тестовый магазин', state=True)
        self.product = Product.objects.create(name='Тестовый товар', category=self.category)

        # Передаем external_id, так как поле обязательное в базе
        self.product_info = ProductInfo.objects.create(
            product=self.product,
            shop=self.shop,
            external_id=1,
            price=1000,
            price_rrc=1200,
            quantity=10
        )

        self.url = reverse('basket')

    def test_post_add_to_basket(self):
        """Тест добавления товара в корзину (POST)"""
        data = {
            'product_info_id': self.product_info.id,
            'quantity': 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(OrderItem.objects.get().quantity, 2)

    def test_get_basket(self):
        """Тест получения содержимого корзины (GET)"""
        # Сначала создаем корзину с товаром
        basket = Order.objects.create(user=self.user, state='basket')
        OrderItem.objects.create(order=basket, product_info=self.product_info, quantity=3)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('order_items', response.data)

    def test_put_update_basket_item(self):
        """Тест изменения количества товара (PUT)"""
        basket = Order.objects.create(user=self.user, state='basket')
        item = OrderItem.objects.create(order=basket, product_info=self.product_info, quantity=1)

        data = [{'id': item.id, 'quantity': 5}]
        response = self.client.put(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)

    def test_delete_basket_item(self):
        """Тест удаления товара из корзины (DELETE)"""
        basket = Order.objects.create(user=self.user, state='basket')
        item = OrderItem.objects.create(order=basket, product_info=self.product_info, quantity=1)

        data = [{'id': item.id}]
        response = self.client.delete(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderItem.objects.count(), 0)