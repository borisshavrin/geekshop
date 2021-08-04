from django.contrib import admin

from products.models import ProductCategory, Product

# Register your models here.
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Отображение доп полей в разделе Products
    list_display = ('name', 'price', 'quantity', 'category', 'is_active')

    # Отображение внутри товара
    fields = ('name', 'images', 'description', ('price', 'quantity'), 'category', 'is_active')

    readonly_fields = ('description',)
    ordering = ('price',)
    search_fields = ('name', 'price')
