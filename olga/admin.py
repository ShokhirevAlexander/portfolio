from django.contrib import admin

from olga.models import CategoryModel, ProductsModel


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('category', 'description')
    list_display_links = ('category',)
    search_fields = ('category',)


class ProductsModelAdmin(admin.ModelAdmin):
    list_display = ('products', 'slug', 'price', 'quantity', 'image')
    list_display_links = ('products', 'quantity')
    prepopulated_fields = {
        'slug': ('products',)
    }
    search_fields = ('products',)


admin.site.register(CategoryModel, CategoryModelAdmin)
admin.site.register(ProductsModel, ProductsModelAdmin)
