from django.db import models
from .models import *
#Todays Last push

class PackagingMaterial(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    Name = models.CharField(max_length=100, db_column='Name')
    PackSize = models.CharField(max_length=100, db_column='PackSize')
    Stock = models.IntegerField(db_column='Stock')

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
    #QCWgId = models.ForeignKey(QCWeightment, db_column='QCWgId', on_delete=models.CASCADE, default=100)

    #AbstractionId = models.ManyToManyField(Abstraction, db_column='AbstractionId')
    #AbstractionId = models.ManyToManyField(Abstraction, db_column='abstraction_id')

    IsFinishGood = models.CharField(max_length=10, db_column='IsFinishGood')
    ProductionDate = models.DateTimeField(auto_now_add=True, db_column='ProductionDate')
    ReceivDate = models.DateTimeField(auto_now_add=True, db_column='ReceivDate')
    LocDate = models.CharField(max_length=100, db_column='LocDate', default='2019-09-03')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = True
        db_table = 'Production'

class ProductionDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ProDtlId')
    ProdId = models.ForeignKey(Production, db_column='ProdId', on_delete=models.CASCADE, default=100)
    SmpProdId = models.ForeignKey(ShrimpProdItem, db_column='SmpProdId', on_delete=models.CASCADE, default=100)

    PrTyId = models.ForeignKey(ProdType, db_column='PrTyId', on_delete=models.CASCADE, default=100)
    PrItmId = models.ForeignKey(ProdItem, db_column='PrItmId', on_delete=models.CASCADE, default=100)
    ProdItemPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdItemPcs', default=0.0)
    ProdItemUnit = models.CharField(max_length=10, db_column='ProdItemUnit')
    ProdAmount = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdAmount', default=0.0)

    #PakMatId = models.ForeignKey(PackagingMaterial, db_column='PakMatId', on_delete=models.CASCADE, default=100)
    #PakMatPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='PakMatPcs', default=0.0)

    class Meta:
        managed = False
        db_table = 'ProductionDetail'


class ProdDtlPkgMaterial(models.Model):
    Id = models.AutoField(primary_key=True, db_column='PrDePkId')
    ProdId = models.ForeignKey(Production, db_column='ProdId', on_delete=models.CASCADE, default=100)
    ProDtlId = models.ForeignKey(ProductionDetail, db_column='ProDtlId', on_delete=models.CASCADE, default=100)
    PkgMatId = models.ForeignKey(PackagingMaterial, db_column='PkgMatId', on_delete=models.CASCADE, default=100)
    Qnty = models.IntegerField( db_column='Qnty', default=100)

    class Meta:
        managed = False
        db_table = 'ProdDtlPkgMaterial'


class LogProduction(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogProdId')
    ProdId = models.ForeignKey(Production, db_column='ProdId', on_delete=models.CASCADE, default=100)
    #QCWgId = models.ForeignKey(QCWeightment, db_column='QCWgId', on_delete=models.CASCADE, default=100)
    IsFinishGood = models.CharField(max_length=10, db_column='IsFinishGood')
    ProductionDate = models.DateTimeField(auto_now_add=True, db_column='ProductionDate')
    ReceivDate = models.DateTimeField(auto_now_add=True, db_column='ReceivDate')
    LocDate = models.CharField(max_length=100, db_column='LocDate', default='2019-09-03')

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

    PrTyId = models.ForeignKey(ProdType, db_column='PrTyId', on_delete=models.CASCADE, default=100)
    PrItmId = models.ForeignKey(ProdItem, db_column='PrItmId', on_delete=models.CASCADE, default=100)
    ProdItemPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdItemPcs', default=0.0)
    ProdItemUnit = models.CharField(max_length=10, db_column='ProdItemUnit')
    ProdAmount = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdAmount', default=0.0)

    #PakMatId = models.ForeignKey(PackagingMaterial, db_column='PakMatId', on_delete=models.CASCADE, default=100)
    #PakMatPcs = models.DecimalField(max_digits=18, decimal_places=2, db_column='PakMatPcs', default=0.0)

    class Meta:
        managed = False
        db_table = 'LogProductionDetail'

class ProductionAbstraction(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ProAbsId')
    ProductionId = models.ForeignKey(Production, db_column='ProductionId', on_delete=models.CASCADE)
    AbstractionId = models.ForeignKey(Abstraction, db_column='AbstractionId', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'ProductionAbstraction'

class GrnPrint(models.Model):
    Id = models.AutoField(primary_key=True, db_column='GrnPrId')
    AbstractionId = models.ForeignKey(Abstraction, db_column='AbstractionId', on_delete=models.CASCADE)

    TotalPrice = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalPrice', default=0.0)
    TotalAbsMeasur = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalAbsMeasur', default=0.0)
    TotalQcMeasur = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalQcMeasur', default=0.0)
    IsFullPaymentDone = models.CharField(max_length=10, db_column='IsFullPaymentDone', default='Y')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'GrnPrint'

class CostDistributionMaster(models.Model):
    Id = models.AutoField(primary_key=True, db_column='CstDisId')
    IsUsed = models.CharField(max_length=10, db_column='IsUsed', default='N')
    LocDate = models.CharField(max_length=50, db_column='LocDate', default='2019-01-01')
    DeheadingLoss = models.DecimalField(max_digits=18, decimal_places=2, db_column='DeheadingLoss', default=0.0)
    TotalKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalKg', default=0.0)


    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'CostDistributionMaster'

class CostDistributionDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='CstDisDtlId')
    CstDisId = models.ForeignKey(CostDistributionMaster, db_column='CstDisId', on_delete=models.CASCADE, default=100)
    ShrimpItemId = models.ForeignKey(ShrimpItem, db_column='ShrimpItemId', on_delete=models.CASCADE, default=100)
    ProdItemId = models.ForeignKey(ProdItem, db_column='ProdItemId', on_delete=models.CASCADE, default=100)

    ProdPercentage = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdPercentage', default=0.0)
    ProdWegKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdWegKg', default=0.0)
    ProdWegLb = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdWegLb', default=0.0)
    ColCostOfProdItemTk = models.DecimalField(max_digits=18, decimal_places=2, db_column='ColCostOfProdItemTk', default=0.0)

    class Meta:
        managed = False
        db_table = 'CostDistributionDetail'

class LogCostDistributionMaster(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogCstDisId')
    CstDisId = models.ForeignKey(CostDistributionMaster, db_column='CstDisId', on_delete=models.CASCADE, default=100)
    IsUsed = models.CharField(max_length=10, db_column='IsUsed', default='N')
    LocDate = models.CharField(max_length=50, db_column='LocDate', default='2019-01-01')
    DeheadingLoss = models.DecimalField(max_digits=18, decimal_places=2, db_column='DeheadingLoss', default=0.0)
    TotalKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalKg', default=0.0)

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'LogCostDistributionMaster'


class LogCostDistributionDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogCstDtlId')
    CstDisId = models.ForeignKey(CostDistributionMaster, db_column='CstDisId', on_delete=models.CASCADE, default=100)
    LogCstDisId = models.ForeignKey(LogCostDistributionMaster, db_column='LogCstDisId', on_delete=models.CASCADE, default=100)
    ShrimpItemId = models.ForeignKey(ShrimpItem, db_column='ShrimpItemId', on_delete=models.CASCADE, default=100)
    ProdItemId = models.ForeignKey(ProdItem, db_column='ProdItemId', on_delete=models.CASCADE, default=100)

    ProdPercentage = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdPercentage', default=0.0)
    ProdWegKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdWegKg', default=0.0)
    ProdWegLb = models.DecimalField(max_digits=18, decimal_places=2, db_column='ProdWegLb', default=0.0)
    ColCostOfProdItemTk = models.DecimalField(max_digits=18, decimal_places=2, db_column='ColCostOfProdItemTk', default=0.0)

    class Meta:
        managed = False
        db_table = 'LogCostDistributionDetail'


class PCode(models.Model):
    Id = models.AutoField(primary_key=True, db_column='GrnPrId')
    ProductCode = models.CharField(max_length=10, db_column='ProductCode')

    class Meta:
        managed = False
        db_table = 'PCode'

class WareHouse(models.Model):
    Id = models.AutoField(primary_key=True, db_column='WaHsId')
    ProdId = models.ForeignKey(Production, db_column='ProdId', on_delete=models.CASCADE)
    LocDate = models.CharField(max_length=50, db_column='LocDate')
    IssueNo = models.CharField(max_length=50, db_column='IssueNo')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'WareHouse'

class WareHouseDetail(models.Model):
    Id = models.AutoField(primary_key=True, db_column='WHDtId')
    ProdId = models.ForeignKey(Production, db_column='ProdId', on_delete=models.CASCADE)
    LocDate = models.CharField(max_length=50, db_column='LocDate')
    IssueNo = models.CharField(max_length=50, db_column='IssueNo')

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'WareHouse'