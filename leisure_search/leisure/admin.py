from django.contrib import admin
from django.apps import apps

Category = apps.get_model('leisure', 'Category')
City = apps.get_model('leisure', 'City')
Institution = apps.get_model('leisure', 'Institution')
Like = apps.get_model('leisure', 'Like')
Stat = apps.get_model('leisure', 'Stat')
TempPhoto = apps.get_model('leisure', 'TempPhoto')

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'published']
    list_editable = ('published',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'rank', 'institution']


class StatAdmin(admin.ModelAdmin):
    list_display = ['id', 'rank_for_search']


admin.site.register(Category, CategoryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Stat, StatAdmin)
admin.site.register(TempPhoto)
