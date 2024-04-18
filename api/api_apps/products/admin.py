from django.contrib import admin

from api_apps.products.models import Category, SubCategory, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    class SubCategoryInline(admin.TabularInline):
        model = SubCategory
        extra = 0
        can_delete = False
        show_change_link = True

    list_display = ["name"]
    inlines = [SubCategoryInline]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    class SubCategoryInline(admin.TabularInline):
        model = Product
        extra = 0
        can_delete = False
        show_change_link = True

    list_display = ["name"]
    inlines = [SubCategoryInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
