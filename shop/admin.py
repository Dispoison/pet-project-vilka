from django.contrib import admin
from django.utils.safestring import mark_safe
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from shop.models import *
from shop.utils.mixins.product_mixin import ProductMixin
from shop.forms import ProductModelForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(PolymorphicParentModelAdmin):
    base_model = Product
    child_models = (Smartphone, Tablet, SmartphoneAccessory, TabletAccessory,
                    Notebook, Monitor, Monoblock, SystemUnit)
    list_display = ('name', 'discounted_price', 'price', 'get_html_photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcategory_slug = None

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50')

    get_html_photo.short_description = 'Изображение'


class SmartphoneAdmin(ProductMixin, PolymorphicChildModelAdmin):
    base_model = Smartphone
    base_form = ProductModelForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcategory_slug = 'smartfony'



class TabletAdmin(ProductMixin, PolymorphicChildModelAdmin):
    base_model = Tablet
    base_form = ProductModelForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcategory_slug = 'planshety'


class SmartphoneAccessoryAdmin(ProductMixin, PolymorphicChildModelAdmin):
    base_model = SmartphoneAccessory
    base_form = ProductModelForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcategory_slug = 'aksessuary-dlya-smartfonov'


class TabletAccessoryAdmin(ProductMixin, PolymorphicChildModelAdmin):
    base_model = TabletAccessory
    base_form = ProductModelForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcategory_slug = 'aksessuary-dlya-planshetov'


class NotebookAdmin(ProductMixin, PolymorphicChildModelAdmin):
    base_model = Notebook
    base_form = ProductModelForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcategory_slug = 'noutbuki'


class MonitorAdmin(ProductMixin, PolymorphicChildModelAdmin):
    base_model = Monitor
    base_form = ProductModelForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcategory_slug = 'monitory'


class MonoblockAdmin(ProductMixin, PolymorphicChildModelAdmin):
    base_model = Monoblock
    base_form = ProductModelForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcategory_slug = 'monobloki'


class SystemUnitAdmin(ProductMixin, PolymorphicChildModelAdmin):
    base_model = SystemUnit
    base_form = ProductModelForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subcategory_slug = 'sistemnye-bloki'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Tablet, TabletAdmin)
admin.site.register(SmartphoneAccessory, SmartphoneAccessoryAdmin)
admin.site.register(TabletAccessory, TabletAccessoryAdmin)

admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Monitor, MonitorAdmin)
admin.site.register(Monoblock, MonoblockAdmin)
admin.site.register(SystemUnit, SystemUnitAdmin)

