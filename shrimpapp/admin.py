from django.contrib import admin
from .models import Department, Designation, Farmer, Supplier, SupplierFarmer, ShrimpType, ShrimpItem, UserManager
# Register your models here.
admin.site.register(Department)
admin.site.register(Designation)

#https://www.dev2qa.com/how-to-manage-models-in-django-admin-site/

class FarmerAdmin(admin.ModelAdmin):
    list_display = ('FarmerName','FarmerCode','FarmerMobile','Address','IsActive','EntryBy__UserName')
    #list_display = ('FarmerName', 'FarmerCode', 'FarmerMobile', 'Address', 'IsActive')

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     #def get_form(self, request, obj=None, **kwargs):
    #     # form = super(FarmerUser, self).get_form(request, obj, **kwargs)
    #     # form.base_fields['get_counterId'].queryset = CounterDetails.objects.all().order_by('-id')
    #     # form.base_fields['get_groupId'].queryset = CounterGroup.objects.all().order_by('-id')
    #
    #     #return form
    #     if db_field.name == "EntryBy":
    #         kwargs['queryset'] = UserManager.objects.all()
    #     #     kwargs['initial'] = request.user
    #     return super(FarmerUser, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # def EntryBy__UserName(self, instance):
    #     return instance.EntryBy.UserName

    # EntryBy__UserName.admin_order_field = 'EntryBy__UserName'
    # EntryBy__UserName.short_description = 'Author Name'



admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Supplier)
admin.site.register(SupplierFarmer)
admin.site.register(ShrimpType)
admin.site.register(ShrimpItem)