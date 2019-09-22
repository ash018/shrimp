from django.contrib import admin
from django.contrib.auth.models import Group, User
from django import forms
from .models import Department, Designation, Farmer,\
    Supplier, SupplierFarmer, ShrimpType, ShrimpItem, \
    UserManager, RowStatus, Author, Book, LogShrimpItem


from .inventorymodel import ShrimpProdItem, \
    PackagingMaterial, FinishProductCode, \
    BasicShrimpType, ProdType, SoakingType,\
    GlazinType, BlockType, CountType, ProdItem
# Register your models here.

admin.site.site_header = 'Shrimp Administration'
admin.site.site_title = 'Shrimp Admin'
admin.site.index_title = 'Shrimp Admin Portal'




admin.site.register(BasicShrimpType)
admin.site.register(ProdType)
admin.site.register(SoakingType)

admin.site.register(GlazinType)
admin.site.register(BlockType)
admin.site.register(CountType)


class ProdItemAdmin(admin.ModelAdmin):
    list_display = ('Name', 'BasicShrimpTypeId', 'PrTyId', 'SoakingTypeId', 'GlazinTypeId', 'BlockTypeId', 'CountTypeId', )
    search_fields = ['PrTyId']
    list_filter = ['GlazinTypeId', 'PrTyId', 'CountTypeId']
    ordering = ['-Id']
    list_per_page = 20

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ["Name"]
        #kwargs['widgets'] = {'Notes': forms.Textarea}
        form = super(ProdItemAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        #obj.user = request.user
        pItem = ProdItem.objects.filter(BasicShrimpTypeId=obj.BasicShrimpTypeId,
                                        PrTyId=obj.PrTyId,
                                        SoakingTypeId=obj.SoakingTypeId,
                                        GlazinTypeId=obj.GlazinTypeId,
                                        BlockTypeId=obj.BlockTypeId,
                                        CountTypeId=obj.CountTypeId)
        if pItem:
            return
        else:
            #print("=="+str(obj.BasicShrimpTypeId))
            obj.Name = str(obj.BasicShrimpTypeId)+' '+str(obj.PrTyId)+' '+str(obj.SoakingTypeId)+' '+str(obj.GlazinTypeId)+'Glazin '+str(obj.BlockTypeId)+' '+str(obj.CountTypeId)
            return super(ProdItemAdmin, self).save_model(request, obj, form, change)

admin.site.register(ProdItem, ProdItemAdmin)




#admin.site.register(Department)
#admin.site.register(Designation)

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
    list_display = ('SupplierName', 'SupplierCode', 'SupplierMobile', 'Address', 'IsActive', 'IsFarmer')
    filter_horizontal = ['FarmerId']
    search_fields = ['SupplierName', 'SupplierCode', 'SupplierMobile']
    list_filter = ['SupplierCode', 'SupplierMobile']
    list_per_page = 20

admin.site.register(UserManager, UserManagerAdmin)
admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ShrimpType)

class ShrimpItemAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ItemCount', 'MeasurUnit','Price')
    search_fields = ['Name', 'Price']
    list_filter = ['Name', 'Price']
    list_per_page = 20

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ["EntryBy"]
        #kwargs['widgets'] = {'Notes': forms.Textarea}
        form = super(ShrimpItemAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        obj.EntryBy = request.user
        obj.save()

        LogShrimpItem(Name=obj.Name, ItemCount=obj.ItemCount,
                      MeasurUnit=obj.MeasurUnit, Price=obj.Price,
                      ShrimpTypeId=obj.ShrimpTypeId, ShrimpItemId=obj,
                      EntryBy=request.user).save()
        #return super(ShrimpItemAdmin, self).save_model(request, obj, form, change)
        return obj


admin.site.register(ShrimpItem, ShrimpItemAdmin)


admin.site.register(ShrimpProdItem)

class PackagingMaterialAdmin(admin.ModelAdmin):
    list_display = ('Name', 'PackSize', 'Stock',)
    search_fields = ['Name', 'PackSize']
    list_filter = ['Name', 'PackSize']
    list_per_page = 20

    def get_queryset(self, request):
        qs = super(PackagingMaterialAdmin, self).get_queryset(request)
        #return qs.filter(Id=request.user)
        return qs.exclude(Id=1)

admin.site.register(PackagingMaterial, PackagingMaterialAdmin)

admin.site.register(FinishProductCode)




admin.site.unregister(Group)
admin.site.unregister(User)


# class BookInline(admin.TabularInline):
#     model = Book
#
# class AuthorAdmin(admin.ModelAdmin):
#     inlines = [
#         BookInline,
#     ]
#
# admin.site.register(Author, AuthorAdmin)



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
