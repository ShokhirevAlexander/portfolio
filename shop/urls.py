from django.urls import path

from olga.views import ProductsView, IndexView, single

app_name = 'olga'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<int:category_id>/', ProductsView.as_view(), name='category'),
    path('page/<int:page>/', ProductsView.as_view(), name='paginator'),
    path('products/<slug:products_slug>/', single, name='single'),
]
