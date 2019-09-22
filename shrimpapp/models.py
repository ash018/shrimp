from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, User
#python manage.py makemigrations shrimpapp
#python manage.py migrate
#Todays Last push

class RowStatus(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    Name = models.CharField(max_length=50, db_column='Name')

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'RowStatus'

class IsFarmerStatus(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    Name = models.CharField(max_length=50, db_column='Name')

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'IsFarmerStatus'

class Department(models.Model):
    Id = models.AutoField(primary_key=True, db_column='DepartmentId')
    DepartmentCode = models.CharField(max_length=50, db_column='DepartmentCode')
    DepartmentName = models.CharField(max_length=100, db_column='DepartmentName')

    def __str__(self):
        return self.DepartmentName

    class Meta:
        managed = False
        db_table = 'Department'

class Designation(models.Model):
    Id = models.AutoField(primary_key=True, db_column='DesignatioId')
    DesignatioCode = models.CharField(max_length=50, db_column='DesignatioCode')
    DesignatioName = models.CharField(max_length=100, db_column='DesignatioName')

    def __str__(self):
        return self.DesignatioName

    class Meta:
        managed = False
        db_table = 'Designation'

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    # python manage.py createsuperuser
    def create_superuser(self, UserId, is_staff, Password):
        user = self.model(
            email=UserId,
            is_staff=is_staff,
        )
        user.set_password(Password)
        user.save(using=self._db)
        return user


class UserManager(models.Model):
#class UserManager(AbstractBaseUser):
    Id = models.AutoField(primary_key=True, db_column='Id')
    UserId = models.CharField(max_length=255, db_column='UserId', unique=True)
    UserName = models.CharField(max_length=255, db_column='UserName')
    Password = models.CharField(max_length=255, db_column='Password')
    Status =  models.ForeignKey(RowStatus, db_column='Status', on_delete=models.CASCADE)
    StaffId = models.CharField(max_length=100, db_column='StaffId')
    Mobile = models.CharField(max_length=100, db_column='Mobile')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    DepartmentId = models.ForeignKey(Department, db_column='DepartmentId', on_delete=models.CASCADE)
    DesignationId = models.ForeignKey(Designation, db_column='DesignatioId', on_delete=models.CASCADE)

    def __str__(self):
        return self.UserId

    def get_full_name(self):
        return self.UserName

    def get_full_Departmen(self):
        return self.DepartmentId.DepartmentName

    def get_full_Departmen(self):
        return self.DesignationId.DesignatioName

    class Meta:
        managed = False
        db_table = 'UserManager'

class Farmer(models.Model):
    Id = models.AutoField(primary_key=True, db_column='FrId')
    FarmerName = models.CharField(max_length=100, db_column='FarmerName')
    FarmerCode = models.CharField(max_length=50, db_column='FarmerCode')
    FarmerMobile = models.CharField(max_length=20, db_column='FarmerMobile')
    Address = models.CharField(max_length=100, db_column='Address')
    IsActive = models.ForeignKey(RowStatus, db_column='IsActive', on_delete=models.CASCADE)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.FarmerName
    class Meta:
        managed = False
        db_table = 'Farmer'

class Supplier(models.Model):
    Id = models.AutoField(primary_key=True, db_column='SupId')
    SupplierName = models.CharField(max_length=100, db_column='SupplierName')
    SupplierCode = models.CharField(max_length=50, db_column='SupplierCode')
    SupplierMobile = models.CharField(max_length=20, db_column='SupplierMobile')
    Address = models.CharField(max_length=100, db_column='Address')
    IsActive = models.ForeignKey(RowStatus, db_column='IsActive', on_delete=models.CASCADE)
    IsFarmer = models.ForeignKey(IsFarmerStatus, db_column='IsFarmer', on_delete=models.CASCADE)
    FarmerId = models.ManyToManyField(Farmer, db_column='FarmerId')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    def __str__(self):
        return self.SupplierName

    class Meta:
        managed = False
        db_table = 'Supplier'

class SupplierFarmer(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    SupplierId = models.ForeignKey(Supplier, db_column='SupplierId', on_delete=models.CASCADE)
    FarmerId = models.ManyToManyField(Farmer, db_column='FarmerId')

    class Meta:
        managed = True
        db_table = 'SupplierFarmer'


class ShrimpType(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TypeId')
    Name = models.CharField(max_length=100, db_column='Name')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'ShrimpType'

class ShrimpItem(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ItemId')
    Name = models.CharField(max_length=100, db_column='Name')
    ItemCount = models.IntegerField(db_column='ItemCount', default=0)
    MeasurUnit = models.CharField(max_length=100, db_column='MeasurUnit')
    Price = models.DecimalField(max_digits=18, decimal_places=2, db_column='Price', default=0.0)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    ShrimpTypeId = models.ForeignKey(ShrimpType, db_column='ShrimpTypeId', on_delete=models.CASCADE, default=100)
    EntryBy = models.ForeignKey(User, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'Shrimp Collect Item'
        managed = False
        db_table = 'ShrimpItem'

class LogShrimpItem(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ItemId')
    Name = models.CharField(max_length=100, db_column='Name')
    ItemCount = models.IntegerField(db_column='ItemCount', default=0)
    MeasurUnit = models.CharField(max_length=100, db_column='MeasurUnit')
    Price = models.DecimalField(max_digits=18, decimal_places=2, db_column='Price', default=0.0)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    ShrimpTypeId = models.ForeignKey(ShrimpType, db_column='ShrimpTypeId', on_delete=models.CASCADE, default=100)
    ShrimpItemId = models.ForeignKey(ShrimpItem, db_column='ShrimpItemId', on_delete=models.CASCADE, default=100)
    EntryBy = models.ForeignKey(User, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    def __str__(self):
        return self.Name

    class Meta:
        #verbose_name = 'Shrimp Collect Item'
        managed = False
        db_table = 'LogShrimpItem'


class GradingType(models.Model):
    Id = models.AutoField(primary_key=True, db_column='GrdTypeId')
    Name = models.CharField(max_length=100, db_column='Name')

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'GradingType'

class ReceiveType(models.Model):
    Id = models.AutoField(primary_key=True, db_column='RcvTypeId')
    Name = models.CharField(max_length=100, db_column='Name')

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'ReceiveType'

class Abstraction(models.Model):
    Id = models.AutoField(primary_key=True, db_column='AbsId')
    RcvTypeId = models.ForeignKey(ReceiveType, db_column='RcvTypeId', on_delete=models.CASCADE, default=100)

    AbsCreateDate = models.DateTimeField(auto_now_add=True, db_column='AbsCreateDate')
    TotalKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalKg', default=0.0)
    TotalLb = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalLb', default=0.0)
    IsQcPass = models.CharField(max_length=100, db_column='IsQcPass', default='N')
    IsProductionUsed = models.CharField(max_length=100, db_column='IsProductionUsed', default='N')

    LocDate = models.CharField(max_length=100, db_column='LocDate', default='2019-08-30')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'Abstraction'

class Weightment(models.Model):
    Id = models.AutoField(primary_key=True, db_column='WgId')
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    FarmerId = models.ForeignKey(Farmer, db_column='FarmerId', on_delete=models.CASCADE, default=100)
    SupplierId = models.ForeignKey(Supplier, db_column='SupplierId', on_delete=models.CASCADE, default=100)
    GrdTypeId = models.ForeignKey(GradingType, db_column='GrdTypeId', on_delete=models.CASCADE, default=100)

    WgDate = models.DateTimeField(auto_now_add=True, db_column='WgDate')
    IsQcPass = models.CharField(max_length=100, db_column='IsQcPass', default='N')
    Total = models.DecimalField(max_digits=18, decimal_places=2, db_column='Total', default=0.0)
    TotalSmpQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalSmpQnty', default=0.0)
    MeasurUnit =  models.CharField(max_length=100, db_column='MeasurUnit', default='Kg')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'Weightment'

class WeightmentDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='WgDtlId')
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    WgId = models.ForeignKey(Weightment, db_column='WgId', on_delete=models.CASCADE, default=100)
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)

    CngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='CngCount', default=0.0)
    SmpQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='SmpQnty', default=0.0)
    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')
    MeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='MeasurQnty', default=0.0)
    Rate = models.DecimalField(max_digits=18, decimal_places=2, db_column='Rate', default=0.0)
    Price = models.DecimalField(max_digits=18, decimal_places=2, db_column='Price', default=0.0)
    Remarks = models.CharField(max_length=100, db_column='Remarks')

    class Meta:
        managed = False
        db_table = 'WeightmentDetail'

class LogAbstraction(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogAbsId')
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    RcvTypeId = models.ForeignKey(ReceiveType, db_column='RcvTypeId', on_delete=models.CASCADE, default=100)

    AbsCreateDate = models.DateTimeField(auto_now_add=True, db_column='AbsCreateDate')
    TotalKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalKg', default=0.0)
    TotalLb = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalLb', default=0.0)
    IsQcPass = models.CharField(max_length=100, db_column='IsQcPass', default='N')
    IsProductionUsed = models.CharField(max_length=100, db_column='IsProductionUsed', default='N')

    LocDate = models.CharField(max_length=100, db_column='LocDate', default='2019-08-30')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'LogAbstraction'


class LogWeightment(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LgWgId')
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    WgId = models.IntegerField(db_column='WgId', default=100)
    FarmerId = models.ForeignKey(Farmer, db_column='FarmerId', on_delete=models.CASCADE, default=100)
    SupplierId = models.ForeignKey(Supplier, db_column='SupplierId', on_delete=models.CASCADE, default=100)
    GrdTypeId = models.ForeignKey(GradingType, db_column='GrdTypeId', on_delete=models.CASCADE, default=100)

    WgDate = models.DateTimeField(auto_now_add=True, db_column='WgDate')
    IsQcPass = models.CharField(max_length=100, db_column='IsQcPass', default='N')
    Total = models.DecimalField(max_digits=18, decimal_places=2, db_column='Total', default=0.0)
    TotalSmpQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalSmpQnty', default=0.0)
    MeasurUnit = models.CharField(max_length=100, db_column='MeasurUnit', default='N')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'LogWeightment'

class LogWeightmentDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogWgDtlId')
    LgWgId = models.ForeignKey(LogWeightment, db_column='LgWgId', on_delete=models.CASCADE, default=100)
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    WgId = models.IntegerField( db_column='WgId', default=100)
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)

    CngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='CngCount', default=0.0)
    SmpQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='SmpQnty', default=0.0)
    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')
    MeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='MeasurQnty', default=0.0)

    Rate = models.DecimalField(max_digits=18, decimal_places=2, db_column='Rate', default=0.0)
    Price = models.DecimalField(max_digits=18, decimal_places=2, db_column='Price', default=0.0)

    Remarks = models.CharField(max_length=100, db_column='Remarks')

    class Meta:
        managed = False
        db_table = 'LogWeightmentDetail'

class QCAbstraction(models.Model):
    Id = models.AutoField(primary_key=True, db_column='QCAbsId')
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    RcvTypeId = models.ForeignKey(ReceiveType, db_column='RcvTypeId', on_delete=models.CASCADE, default=100)

    QCDate = models.DateTimeField(auto_now_add=True, db_column='QCDate')
    QCTotalKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCTotalKg', default=0.0)
    QCTotalLb = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCTotalLb', default=0.0)

    IsProductionUsed = models.CharField(max_length=100, db_column='IsProductionUsed', default='N')
    IsQcPass = models.CharField(max_length=100, db_column='IsQcPass', default='N')
    LocDate = models.CharField(max_length=100, db_column='LocDate', default='2019-08-30')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'QCAbstraction'

class QCWeightment(models.Model):
    Id = models.AutoField(primary_key=True, db_column='QCWgId')
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    QCAbsId = models.ForeignKey(QCAbstraction, db_column='QCAbsId', on_delete=models.CASCADE, default=100)
    FarmerId = models.ForeignKey(Farmer, db_column='FarmerId', on_delete=models.CASCADE, default=100)
    SupplierId = models.ForeignKey(Supplier, db_column='SupplierId', on_delete=models.CASCADE, default=100)
    GrdTypeId = models.ForeignKey(GradingType, db_column='GrdTypeId', on_delete=models.CASCADE, default=100)

    QCDate = models.DateTimeField(auto_now_add=True, db_column='QCDate')
    Total = models.DecimalField(max_digits=18, decimal_places=2, db_column='Total', default=0.0)
    TotalSmpQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalSmpQnty', default=0.0)
    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'QCWeightment'

class QCWeightmentDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='QcWgDtlId')
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    QCAbsId = models.ForeignKey(QCAbstraction, db_column='QCAbsId', on_delete=models.CASCADE, default=100)
    QCWgId = models.ForeignKey(QCWeightment, db_column='QCWgId', on_delete=models.CASCADE, default=100)
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)

    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')
    QCCngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCCngCount', default=0.0)
    QCSmpQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCSmpQnty', default=0.0)

    QCMeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCMeasurQnty', default=0.0)
    QCRemarks = models.CharField(max_length=100, db_column='QCRemarks', default='N/A')

    class Meta:
        managed = False
        db_table = 'QCWeightmentDetail'


class LogQCAbstraction(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogQcAbsId')
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    QCAbsId = models.ForeignKey(QCAbstraction, db_column='QCAbsId', on_delete=models.CASCADE, default=100)
    RcvTypeId = models.ForeignKey(ReceiveType, db_column='RcvTypeId', on_delete=models.CASCADE, default=100)

    QCDate = models.DateTimeField(auto_now_add=True, db_column='QCDate')
    QCTotalKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCTotalKg', default=0.0)
    QCTotalLb = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCTotalLb', default=0.0)

    IsProductionUsed = models.CharField(max_length=100, db_column='IsProductionUsed', default='N')
    IsQcPass = models.CharField(max_length=100, db_column='IsQcPass', default='N')
    LocDate = models.CharField(max_length=100, db_column='LocDate', default='2019-08-30')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'LogQCAbstraction'

class LogQCWeightment(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogQcId')

    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    QCAbsId = models.ForeignKey(QCAbstraction, db_column='QCAbsId', on_delete=models.CASCADE, default=100)
    LogQcAbsId = models.ForeignKey(LogQCAbstraction, db_column='LogQcAbsId', on_delete=models.CASCADE, default=100)
    QCWgId = models.IntegerField(db_column='QCWgId', default=100)

    FarmerId = models.ForeignKey(Farmer, db_column='FarmerId', on_delete=models.CASCADE, default=100)
    SupplierId = models.ForeignKey(Supplier, db_column='SupplierId', on_delete=models.CASCADE, default=100)
    GrdTypeId = models.ForeignKey(GradingType, db_column='GrdTypeId', on_delete=models.CASCADE, default=100)

    QCDate = models.DateTimeField(auto_now_add=True, db_column='QCDate')
    Total = models.DecimalField(max_digits=18, decimal_places=2, db_column='Total', default=0.0)
    TotalSmpQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalSmpQnty', default=0.0)
    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'LogQCWeightment'

class LogQCWeightmentDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogQcWgDtlId')
    AbsId = models.ForeignKey(Abstraction, db_column='AbsId', on_delete=models.CASCADE, default=100)
    QCAbsId = models.ForeignKey(QCAbstraction, db_column='QCAbsId', on_delete=models.CASCADE, default=100)
    LogQcAbsId = models.ForeignKey(LogQCAbstraction, db_column='LogQcAbsId', on_delete=models.CASCADE, default=100)
    LogQcWegId = models.ForeignKey(LogQCWeightment, db_column='LogQcWegId', on_delete=models.CASCADE, default=100)

    QCWgId = models.IntegerField(db_column='QCWgId', default=100)
    QcWgDtlId = models.IntegerField(db_column='QcWgDtlId', default=100)
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)

    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')
    QCCngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCCngCount', default=0.0)
    QCSmpQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCSmpQnty', default=0.0)

    QCMeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCMeasurQnty', default=0.0)
    QCRemarks = models.CharField(max_length=100, db_column='QCRemarks', default='N/A')

    class Meta:
        managed = False
        db_table = 'LogQCWeightmentDetail'


class Author(models.Model):
    Id = models.AutoField(primary_key=True, db_column='AuthorId')
    name = models.CharField(max_length=100, db_column='Name')

    class Meta:
        managed = False
        db_table = 'Author'


class Book(models.Model):
    Id = models.AutoField(primary_key=True, db_column='BookId')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='AuthorId')
    Title = models.CharField(max_length=100, db_column='Title')

    class Meta:
        managed = False
        db_table = 'Book'