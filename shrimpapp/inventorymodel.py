from django.db import models
from .models import *
#Todays Last push

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
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')

    PrItmId = models.ForeignKey(ProdItem, db_column='PrItmId', on_delete=models.CASCADE, default=100)
    ProdItemPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdItemPcs', default=0.0)
    ProdItemUnit = models.CharField(max_length=10, db_column='ProdItemUnit')
    ProdAmount = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdAmount', default=0.0)

    class Meta:
        managed = False
        db_table = 'ProductionDetail'


class LogProduction(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogProdId')
    ProdId = models.ForeignKey(Production, db_column='ProdId', on_delete=models.CASCADE, default=100)
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
    ShrItemId = models.ForeignKey(ShrimpItem, db_column='ShrItemId', on_delete=models.CASCADE, default=100)
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')

    PrItmId = models.ForeignKey(ProdItem, db_column='PrItmId', on_delete=models.CASCADE, default=100)
    ProdItemPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdItemPcs', default=0.0)
    ProdItemUnit = models.CharField(max_length=10, db_column='ProdItemUnit')
    ProdAmount = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdAmount', default=0.0)

    class Meta:
        managed = False
        db_table = 'LogProductionDetail'



