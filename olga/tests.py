from http import HTTPStatus
from olga.models import ProductsModel, CategoryModel
from django.test import TestCase
from django.urls import reverse


# class IndexViewTestCase(TestCase):
#
#     def test_view(self):
#         response = self.client.get('/')
#         self.assertAlmostEqual(response.status_code, 200)


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def test_list(self):
        path = reverse('olga:products')
        response = self.client.get(path)

        products = ProductsModel.objects.all()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'olga/products.html')
        self.assertEqual(list(response.context_data['objects_list']), list(products[:3]))

    def test_list_category(self):
        category = CategoryModel.objects.first()
        path = reverse('olga:category', kwargs={'category_id': 1})
        response = self.client.get(path)

        products = ProductsModel.objects.all()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'olga/products.html')
        self.assertEqual(
            list(response.context_data['objects_list']),
            list(products.filter(category_id=category.id))
        )
