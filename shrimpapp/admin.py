from django.contrib import admin
from django.contrib.auth.models import Group, User
from django import forms
from .models import Department, Designation, Farmer, Supplier, SupplierFarmer, ShrimpType, ShrimpItem, UserManager
from .inventorymodel import ShrimpProdItem, PackagingMaterial
# Register your models here.

admin.site.site_header = 'Shrimp Administration'
admin.site.site_title = "Shrimp Admin"
admin.site.index_title = "Shrimp Admin Portal"

admin.site.register(Department)
admin.site.register(Designation)

#https://www.dev2qa.com/how-to-manage-models-in-django-admin-site/
#https://books.agiliq.com/projects/django-admin-cookbook/en/latest/filter_fk_dropdown.html
# .values('UserName')
#https://books.agiliq.com/projects/django-admin-cookbook/en/latest/many_to_many.html
#https://reinout.vanrees.org/weblog/2011/11/29/many-to-many-field-save-method.html
#https://www.pythoncircle.com/post/28/creating-custom-user-model-and-custom-authentication-in-django/
#https://automationstepbystep.com/jenkins/



class UserManagerAdmin(admin.ModelAdmin):
    list_display = ['UserId', 'UserName', 'Password','StaffId','Mobile', 'DepartmentId', 'DesignationId']
    search_fields = ['UserId', 'StaffId', 'Mobile']
    list_filter = ['UserId', 'StaffId', 'Mobile']
    list_per_page = 20

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "DepartmentId":
            kwargs["queryset"] = Department.objects.all()
        if db_field.name == "DesignationId":
            kwargs["queryset"] = Designation.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class FarmerAdmin(admin.ModelAdmin):
    list_display = ('FarmerName', 'FarmerCode', 'FarmerMobile', 'Address', 'IsActive')
    search_fields = ['FarmerName', 'FarmerCode', 'FarmerMobile']
    list_filter = ['FarmerCode', 'FarmerMobile']
    list_per_page = 20


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('SupplierName', 'SupplierCode', 'SupplierMobile', 'Address', 'IsActive')
    filter_horizontal = ['FarmerId']
    search_fields = ['SupplierName', 'SupplierCode', 'SupplierMobile']
    list_filter = ['SupplierCode', 'SupplierMobile']
    list_per_page = 20


admin.site.register(UserManager, UserManagerAdmin)
admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ShrimpType)
admin.site.register(ShrimpItem)
admin.site.register(ShrimpProdItem)
admin.site.register(PackagingMaterial)


admin.site.unregister(Group)
admin.site.unregister(User)

# class FarmerAdminForm(forms.ModelForm):
#     tags = forms.ModelMultipleChoiceField(
#         Farmer.objects.all(),
#         widget=admin.widgets.FilteredSelectMultiple('Tags', False),
#         required=False,
#     )
#
#     def __init__(self, *args, **kwargs):
#         super(FarmerAdminForm, self).__init__(*args, **kwargs)
#         if self.instance.pk:
#             self.initial['tags'] = self.instance.tags.values_list('pk', flat=True)
#
#     def save(self, *args, **kwargs):
#         instance = super(FarmerAdminForm, self).save(*args, **kwargs)
#         if instance.pk:
#             instance.tags.clear()
#             instance.tags.add(*self.cleaned_data['tags'])
#         return instance
#
# class SupplierFarmerAdmin(admin.ModelAdmin):
#     form = FarmerAdminForm
#     search_fields = ['SupplierId']

#admin.site.register(SupplierFarmer, SupplierFarmerAdmin)
#admin.site.register(SupplierFarmer)
