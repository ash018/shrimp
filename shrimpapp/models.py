from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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

    # objects = MyUserManager()
    #
    # USERNAME_FIELD = "UserId"
    # REQUIRED_FIELDS = ['Status']

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
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    ShrimpTypeId = models.ForeignKey(ShrimpType, db_column='ShrimpTypeId', on_delete=models.CASCADE, default=100)
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'ShrimpItem'

class Weightment(models.Model):
    Id = models.AutoField(primary_key=True, db_column='WgId')
    FarmerId = models.ForeignKey(Farmer, db_column='FarmerId', on_delete=models.CASCADE, default=100)
    SupplierId = models.ForeignKey(Supplier, db_column='SupplierId', on_delete=models.CASCADE, default=100)
    WgDate = models.DateTimeField(auto_now_add=True, db_column='WgDate')
    IsQcPass = models.CharField(max_length=100, db_column='IsQcPass')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'Weightment'

class WeightmentDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='WgDtlId')
    WgId = models.ForeignKey(Weightment, db_column='WgId', on_delete=models.CASCADE, default=100)
    CngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='CngCount', default=0.0)
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)
    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')
    MeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='MeasurQnty', default=0.0)
    Rate = models.DecimalField(max_digits=18, decimal_places=2, db_column='Rate', default=0.0)
    Remarks = models.CharField(max_length=100, db_column='Remarks')

    class Meta:
        managed = False
        db_table = 'WeightmentDetail'

class LogWeightment(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LgWgId')
    WgId = models.ForeignKey(Weightment, db_column='WgId', on_delete=models.CASCADE, default=100)
    FarmerId = models.ForeignKey(Farmer, db_column='FarmerId', on_delete=models.CASCADE, default=100)
    SupplierId = models.ForeignKey(Supplier, db_column='SupplierId', on_delete=models.CASCADE, default=100)
    WgDate = models.DateTimeField(auto_now_add=True, db_column='WgDate')
    IsQcPass = models.CharField(max_length=100, db_column='IsQcPass')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'LogWeightment'

class LogWeightmentDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogWgDtlId')
    LgWgId = models.ForeignKey(LogWeightment, db_column='LgWgId', on_delete=models.CASCADE, default=100)
    WgId = models.ForeignKey(Weightment, db_column='WgId', on_delete=models.CASCADE, default=100)
    CngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='CngCount', default=0.0)
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)
    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')
    MeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='MeasurQnty', default=0.0)
    Rate = models.DecimalField(max_digits=18, decimal_places=2, db_column='Rate', default=0.0)
    Remarks = models.CharField(max_length=100, db_column='Remarks')

    class Meta:
        managed = False
        db_table = 'LogWeightmentDetail'


class QCWeightment(models.Model):
    Id = models.AutoField(primary_key=True, db_column='QCWgId')
    FarmerId = models.ForeignKey(Farmer, db_column='FarmerId', on_delete=models.CASCADE, default=100)
    SupplierId = models.ForeignKey(Supplier, db_column='SupplierId', on_delete=models.CASCADE, default=100)
    WgDate = models.DateTimeField(auto_now_add=True, db_column='WgDate')
    IsQcPass = models.CharField(max_length=10, db_column='IsQcPass')
    IsProductionUsed = models.CharField(max_length=10, db_column='IsProductionUsed')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)
    WgId = models.ForeignKey(Weightment, db_column='WgId', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'QCWeightment'


class QCWeightmentDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='WgDtlId')
    WgId = models.ForeignKey(Weightment, db_column='WgId', on_delete=models.CASCADE, default=100)
    GivenCngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='GivenCngCount', default=0.0)
    QCCngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCCngCount', default=0.0)
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)
    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')
    MeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='MeasurQnty', default=0.0)
    QCMeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCMeasurQnty', default=0.0)
    Rate = models.DecimalField(max_digits=18, decimal_places=2, db_column='Rate', default=0.0)
    Remarks = models.CharField(max_length=100, db_column='Remarks',default='N/A')
    QCRemarks = models.CharField(max_length=100, db_column='QCRemarks', default='N/A')

    class Meta:
        managed = False
        db_table = 'QCWeightmentDetail'

class LogQCWeightment(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogQcId')
    FarmerId = models.ForeignKey(Farmer, db_column='FarmerId', on_delete=models.CASCADE, default=100)
    SupplierId = models.ForeignKey(Supplier, db_column='SupplierId', on_delete=models.CASCADE, default=100)
    WgDate = models.DateTimeField(auto_now_add=True, db_column='WgDate')
    IsQcPass = models.CharField(max_length=100, db_column='IsQcPass')
    IsProductionUsed = models.CharField(max_length=10, db_column='IsProductionUsed')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)
    QCWgId = models.ForeignKey(QCWeightment, db_column='QCWgId', on_delete=models.CASCADE, default=100)
    WgId = models.ForeignKey(Weightment, db_column='WgId', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'LogQCWeightment'

class LogQCWeightmentDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogQcDId')
    LogQcId = models.ForeignKey(LogQCWeightment, db_column='LogQcId', on_delete=models.CASCADE, default=100)
    QCWgId = models.ForeignKey(QCWeightment, db_column='QCWgId', on_delete=models.CASCADE, default=100)
    WgId = models.ForeignKey(Weightment, db_column='WgId', on_delete=models.CASCADE, default=100)
    GivenCngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='GivenCngCount', default=0.0)
    QCCngCount = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCCngCount', default=0.0)
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)
    MeasurUnit = models.CharField(max_length=10, db_column='MeasurUnit')
    MeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='MeasurQnty', default=0.0)
    QCMeasurQnty = models.DecimalField(max_digits=18, decimal_places=2, db_column='QCMeasurQnty', default=0.0)
    Rate = models.DecimalField(max_digits=18, decimal_places=2, db_column='Rate', default=0.0)
    Remarks = models.CharField(max_length=100, db_column='Remarks', default='N/A')
    QCRemarks = models.CharField(max_length=100, db_column='QCRemarks', default='N/A')

    class Meta:
        managed = False
        db_table = 'LogQCWeightmentDetail'
