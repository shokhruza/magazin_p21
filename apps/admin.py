from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mptt.admin import DraggableMPTTAdmin
from django.utils.translation import gettext_lazy as _
from apps.models import Category, Product, ProductImage, Review, Tag, User


@admin.register(Category)
class CategoryDraggableMPTTAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20


class ProductImageStackedInline(admin.StackedInline):
    model = ProductImage
    min_num = 0
    extra = 2


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageStackedInline]
    list_display = ['name', 'price', 'category']


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserModel(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "image")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
