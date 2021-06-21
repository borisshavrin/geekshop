from django.contrib import admin

from products.models import ProductCategory, Product

# Register your models here.
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')    # Отображение доп полей в разделе Products
    fields = ('name', 'images', 'description', ('price', 'quantity'), 'category')  # Отображение внутри товара
    readonly_fields = ('description',)
    ordering = ('price',)
    search_fields = ('name', 'price')
