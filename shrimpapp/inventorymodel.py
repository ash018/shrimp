from django.db import models
from .models import *
#Todays Last push

class PackagingMaterial(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    Name = models.CharField(max_length=100, db_column='Name')
    PackSize = models.CharField(max_length=100, db_column='PackSize')

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'PackagingMaterial'


class ShrimpProdItem(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    Name = models.CharField(max_length=100, db_column='Name')

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'ShrimpProdItem'


class ProdType(models.Model):
    Id = models.AutoField(primary_key=True, db_column='PrTyId')
    Name = models.CharField(max_length=100, db_column='Name')

    class Meta:
        managed = False
        db_table = 'ProdType'

class ProdItem(models.Model):
    Id = models.AutoField(primary_key=True, db_column='PrItmId')
    PrTyId = models.ForeignKey(ProdType, db_column='PrTyId', on_delete=models.CASCADE, default=100)
    Name = models.CharField(max_length=100, db_column='Name')

    class Meta:
        managed = False
        db_table = 'ProdItem'

class Production(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ProdId')
    QCWgId = models.ForeignKey(QCWeightment, db_column='QCWgId', on_delete=models.CASCADE, default=100)
    IsFinishGood = models.CharField(max_length=10, db_column='IsFinishGood')
    ProductionDate = models.DateTimeField(auto_now_add=True, db_column='ProductionDate')
    ReceivDate = models.DateTimeField(auto_now_add=True, db_column='ReceivDate')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'Production'

class ProductionDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ProDtlId')
    ProdId = models.ForeignKey(Production, db_column='ProdId', on_delete=models.CASCADE, default=100)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')

    SmpProdId = models.ForeignKey(ShrimpProdItem, db_column='SmpProdId', on_delete=models.CASCADE, default=100)
    PrItmId = models.ForeignKey(ProdItem, db_column='PrItmId', on_delete=models.CASCADE, default=100)
    ProdItemPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdItemPcs', default=0.0)
    ProdItemUnit = models.CharField(max_length=10, db_column='ProdItemUnit')
    ProdAmount = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdAmount', default=0.0)

    PakMatId = models.ForeignKey(PackagingMaterial, db_column='PakMatId', on_delete=models.CASCADE, default=100)
    PakMatPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='PakMatPcs', default=0.0)

    class Meta:
        managed = False
        db_table = 'ProductionDetail'


class LogProduction(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogProdId')
    ProdId = models.ForeignKey(Production, db_column='ProdId', on_delete=models.CASCADE, default=100)
    QCWgId = models.ForeignKey(QCWeightment, db_column='QCWgId', on_delete=models.CASCADE, default=100)
    IsFinishGood = models.CharField(max_length=10, db_column='IsFinishGood')
    ProductionDate = models.DateTimeField(auto_now_add=True, db_column='ProductionDate')
    ReceivDate = models.DateTimeField(auto_now_add=True, db_column='ReceivDate')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'LogProduction'

class LogProductionDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogProDtlId')
    LogProdId = models.ForeignKey(LogProduction, db_column='LogProdId', on_delete=models.CASCADE, default=100)
    ProdId = models.ForeignKey(Production, db_column='ProdId', on_delete=models.CASCADE, default=100)
    SmpProdId = models.ForeignKey(ShrimpProdItem, db_column='SmpProdId', on_delete=models.CASCADE, default=100)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')

    PrItmId = models.ForeignKey(ProdItem, db_column='PrItmId', on_delete=models.CASCADE, default=100)
    ProdItemPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdItemPcs', default=0.0)
    ProdItemUnit = models.CharField(max_length=10, db_column='ProdItemUnit')
    ProdAmount = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdAmount', default=0.0)

    PakMatId = models.ForeignKey(PackagingMaterial, db_column='PakMatId', on_delete=models.CASCADE, default=100)
    PakMatPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='PakMatPcs', default=0.0)

    class Meta:
        managed = False
        db_table = 'LogProductionDetail'



