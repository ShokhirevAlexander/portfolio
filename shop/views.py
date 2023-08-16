from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView

from olga.models import CategoryModel, ProductsModel


class IndexView(TemplateView):
    template_name = 'olga/index.html'


class ProductsView(ListView):
    template_name = 'olga/products.html'
    model = ProductsModel
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsView, self).get_context_data()
        context['categories'] = CategoryModel.objects.all()
        context['baskets'] = CategoryModel.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductsView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


def single(request, products_slug):
    product_single = get_object_or_404(ProductsModel, slug=products_slug)
    product = ProductsModel.objects.filter(slug=products_slug)
    context = {'product_single': product_single,
               'products': product}
    return render(request, 'olga/single.html', context)
