from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    #ordering = ('level', 'id',)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    #ordering = ('level', 'id',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'discounted_price', 'price', 'get_html_photo')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def __init__(self, *args, **kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)
        self.category_slug = None

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50')

    get_html_photo.short_description = 'Изображение'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Subcategory.objects.filter(slug=self.category_slug), empty_label=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(ProductAdmin):
    def __init__(self, *args, **kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)
        self.category_slug = 'smartfony'


class TabletAdmin(ProductAdmin):
    def __init__(self, *args, **kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)
        self.category_slug = 'planshety'


class SmartphoneAccessoryAdmin(ProductAdmin):
    def __init__(self, *args, **kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)
        self.category_slug = 'aksessuary-dlya-smartfonov'


class TabletAccessoryAdmin(ProductAdmin):
    def __init__(self, *args, **kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)
        self.category_slug = 'aksessuary-dlya-planshetov'


class NotebookAdmin(ProductAdmin):
    def __init__(self, *args, **kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)
        self.category_slug = 'noutbuki'


class MonitorAdmin(ProductAdmin):
    def __init__(self, *args, **kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)
        self.category_slug = 'monitory'


class MonoblockAdmin(ProductAdmin):
    def __init__(self, *args, **kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)
        self.category_slug = 'monobloki'


class SystemUnitAdmin(ProductAdmin):
    def __init__(self, *args, **kwargs):
        super(ProductAdmin, self).__init__(*args, **kwargs)
        self.category_slug = 'sistemnye-bloki'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)


admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Tablet, TabletAdmin)
admin.site.register(SmartphoneAccessory, SmartphoneAccessoryAdmin)
admin.site.register(TabletAccessory, TabletAccessoryAdmin)

admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Monitor, MonitorAdmin)
admin.site.register(Monoblock, MonoblockAdmin)
admin.site.register(SystemUnit, SystemUnitAdmin)


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)