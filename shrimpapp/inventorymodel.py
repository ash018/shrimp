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

    HOSO20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HOSO20FC', default=0.0)
    HOSO25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HOSO25FC', default=0.0)
    HOSO30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HOSO30FC', default=0.0)
    HOSO40FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HOSO40FC', default=0.0)

    PDTO20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO20RC', default=0.0)
    PDTO25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO25RC', default=0.0)
    PDTO20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO20FC', default=0.0)
    PDTO25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO25FC', default=0.0)
    PDTO30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO30FC', default=0.0)

    PnD20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD20RC', default=0.0)
    PnD25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD25RC', default=0.0)
    PnD20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD20FC', default=0.0)
    PnD25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD25FC', default=0.0)
    PnD30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD30FC', default=0.0)

    HLSO20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO20RC', default=0.0)
    HLSO25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO25RC', default=0.0)
    HLSO20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO20FC', default=0.0)
    HLSO25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO25FC', default=0.0)
    HLSO30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO30FC', default=0.0)
    HLSO11FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO11FC', default=0.0)

    HLSONT20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT20RC', default=0.0)
    HLSONT25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT25RC', default=0.0)
    HLSONT20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT20FC', default=0.0)
    HLSONT25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT25FC', default=0.0)
    HLSONT30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT30FC', default=0.0)

    EZP20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP20RC', default=0.0)
    EZP25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP25RC', default=0.0)
    EZP20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP20FC', default=0.0)
    EZP25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP25FC', default=0.0)
    EZP30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP30FC', default=0.0)

    DC20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC20RC', default=0.0)
    DC25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC25RC', default=0.0)
    DC20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC20FC', default=0.0)
    DC25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC25FC', default=0.0)
    DC30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC30FC', default=0.0)

    CPDTO20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO20RC', default=0.0)
    CPDTO25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO25RC', default=0.0)
    CPDTO20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO20FC', default=0.0)
    CPDTO25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO25FC', default=0.0)
    CPDTO30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO30FC', default=0.0)

    CPD20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD20RC', default=0.0)
    CPD25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD25RC', default=0.0)
    CPD20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD20FC', default=0.0)
    CPD25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD25FC', default=0.0)
    CPD30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD30FC', default=0.0)

    PD20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD20RC', default=0.0)
    PD25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD25RC', default=0.0)
    PD20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD20FC', default=0.0)
    PD25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD25FC', default=0.0)
    PD30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD30FC', default=0.0)

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

    HOSO20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HOSO20FC', default=0.0)
    HOSO25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HOSO25FC', default=0.0)
    HOSO30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HOSO30FC', default=0.0)
    HOSO40FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HOSO40FC', default=0.0)

    PDTO20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO20RC', default=0.0)
    PDTO25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO25RC', default=0.0)
    PDTO20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO20FC', default=0.0)
    PDTO25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO25FC', default=0.0)
    PDTO30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PDTO30FC', default=0.0)

    PnD20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD20RC', default=0.0)
    PnD25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD25RC', default=0.0)
    PnD20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD20FC', default=0.0)
    PnD25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD25FC', default=0.0)
    PnD30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PnD30FC', default=0.0)

    HLSO20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO20RC', default=0.0)
    HLSO25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO25RC', default=0.0)
    HLSO20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO20FC', default=0.0)
    HLSO25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO25FC', default=0.0)
    HLSO30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO30FC', default=0.0)
    HLSO11FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSO11FC', default=0.0)

    HLSONT20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT20RC', default=0.0)
    HLSONT25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT25RC', default=0.0)
    HLSONT20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT20FC', default=0.0)
    HLSONT25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT25FC', default=0.0)
    HLSONT30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='HLSONT30FC', default=0.0)

    EZP20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP20RC', default=0.0)
    EZP25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP25RC', default=0.0)
    EZP20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP20FC', default=0.0)
    EZP25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP25FC', default=0.0)
    EZP30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='EZP30FC', default=0.0)

    DC20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC20RC', default=0.0)
    DC25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC25RC', default=0.0)
    DC20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC20FC', default=0.0)
    DC25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC25FC', default=0.0)
    DC30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='DC30FC', default=0.0)

    CPDTO20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO20RC', default=0.0)
    CPDTO25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO25RC', default=0.0)
    CPDTO20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO20FC', default=0.0)
    CPDTO25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO25FC', default=0.0)
    CPDTO30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPDTO30FC', default=0.0)

    CPD20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD20RC', default=0.0)
    CPD25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD25RC', default=0.0)
    CPD20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD20FC', default=0.0)
    CPD25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD25FC', default=0.0)
    CPD30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='CPD30FC', default=0.0)

    PD20RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD20RC', default=0.0)
    PD25RC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD25RC', default=0.0)
    PD20FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD20FC', default=0.0)
    PD25FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD25FC', default=0.0)
    PD30FC = models.DecimalField(max_digits=18, decimal_places=2, db_column='PD30FC', default=0.0)

    class Meta:
        managed = False
        db_table = 'LogProductionDetail'

class FinishedItemTypes(models.Model):
    Id = models.AutoField(primary_key=True, db_column='FinItmId')
    Name = models.CharField(max_length=100, db_column='Name', null=False)

    class Meta:
        managed = False
        db_table = 'FinishedItemTypes'


class FinishedItemGrade(models.Model):
    Id = models.AutoField(primary_key=True, db_column='FinItmGrdId')
    Name = models.CharField(max_length=100, db_column='Name', null=False)

    class Meta:
        managed = False
        db_table = 'FinishedItemGrade'


class BTFG(models.Model):
    Id = models.AutoField(primary_key=True, db_column='BTFGId')
    BTFGCreateDate = models.DateTimeField(auto_now_add=True, db_column='BTFGCreateDate')
    FinItmId = models.ForeignKey(FinishedItemTypes, db_column='FinItmId', on_delete=models.CASCADE, default=100)
    FinItmGrdId = models.ForeignKey(FinishedItemGrade, db_column='FinItmGrdId', on_delete=models.CASCADE, default=100)
    PackingType = models.CharField(max_length=10, db_column='PackingType')
    IssueNo = models.IntegerField(db_column='IssueNo', default=0)
    CostPerLBTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='CostPerLBTK', default=0.0)
    Reference = models.CharField(max_length=100, db_column='Reference')
    DFPisEqualS = models.DecimalField(max_digits=18, decimal_places=2, db_column='DFPisEqualS', default=0.0)
    DFSisEqualP = models.DecimalField(max_digits=18, decimal_places=2, db_column='DFSisEqualP', default=0.0)
    ReciveDate = models.DateTimeField(auto_now_add=True, db_column='ReciveDate')
    PrductionDate = models.DateTimeField(auto_now_add=True, db_column='PrductionDate')

    OBInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='OBInCartoon', default=0.0)
    OBInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='OBInLbs', default=0.0)
    OBInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='OBInKg', default=0.0)
    OBValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='OBValueTK', default=0.0)

    RQInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='RQInCartoon', default=0.0)
    RQInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='RQInLbs', default=0.0)
    RQInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='RQInKg', default=0.0)
    RQValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='RQValueTK', default=0.0)

    IssSaOutInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssSaOutInCartoon', default=0.0)
    IssSaOutInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssSaOutInLbs', default=0.0)
    IssSaOutInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssSaOutInKg', default=0.0)
    IssSaOutValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssSaOutValueTK', default=0.0)

    IssToRePrcsInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssToRePrcsInCartoon', default=0.0)
    IssToRePrcsInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssToRePrcsInLbs', default=0.0)
    IssToRePrcsInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssToRePrcsInKg', default=0.0)
    IssToRePrcsValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssToRePrcsValueTK', default=0.0)

    RtnFrmRePrcsInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='RtnFrmRePrcsInCartoon', default=0.0)
    RtnFrmRePrcsInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='RtnFrmRePrcsInLbs', default=0.0)
    RtnFrmRePrcsInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='RtnFrmRePrcsInKg', default=0.0)
    RtnFrmRePrcsValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='RtnFrmRePrcsValueTK', default=0.0)

    ClsBlnInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='ClsBlnInCartoon', default=0.0)
    ClsBlnInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='ClsBlnInLbs', default=0.0)
    ClsBlnInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='ClsBlnInKg', default=0.0)
    ClsBlnValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='ClsBlnValueTK', default=0.0)

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'BTFG'


class LogBTFG(models.Model):
    Id = models.AutoField(primary_key=True, db_column='LogBTFGId')
    BTFGId = models.ForeignKey(BTFG, db_column='BTFGId', on_delete=models.CASCADE, default=100)
    BTFGCreateDate = models.DateTimeField(auto_now_add=True, db_column='BTFGCreateDate')
    FinItmId = models.ForeignKey(FinishedItemTypes, db_column='FinItmId', on_delete=models.CASCADE, default=100)
    FinItmGrdId = models.ForeignKey(FinishedItemGrade, db_column='FinItmGrdId', on_delete=models.CASCADE, default=100)
    PackingType = models.CharField(max_length=10, db_column='PackingType')
    IssueNo = models.IntegerField(db_column='IssueNo', default=0)
    CostPerLBTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='CostPerLBTK', default=0.0)
    Reference = models.CharField(max_length=100, db_column='Reference')
    DFPisEqualS = models.DecimalField(max_digits=18, decimal_places=2, db_column='DFPisEqualS', default=0.0)
    DFSisEqualP = models.DecimalField(max_digits=18, decimal_places=2, db_column='DFSisEqualP', default=0.0)
    ReciveDate = models.DateTimeField(auto_now_add=True, db_column='ReciveDate')
    PrductionDate = models.DateTimeField(auto_now_add=True, db_column='PrductionDate')

    OBInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='OBInCartoon', default=0.0)
    OBInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='OBInLbs', default=0.0)
    OBInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='OBInKg', default=0.0)
    OBValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='OBValueTK', default=0.0)

    RQInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='RQInCartoon', default=0.0)
    RQInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='RQInLbs', default=0.0)
    RQInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='RQInKg', default=0.0)
    RQValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='RQValueTK', default=0.0)

    IssSaOutInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssSaOutInCartoon', default=0.0)
    IssSaOutInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssSaOutInLbs', default=0.0)
    IssSaOutInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssSaOutInKg', default=0.0)
    IssSaOutValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssSaOutValueTK', default=0.0)

    IssToRePrcsInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssToRePrcsInCartoon', default=0.0)
    IssToRePrcsInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssToRePrcsInLbs', default=0.0)
    IssToRePrcsInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssToRePrcsInKg', default=0.0)
    IssToRePrcsValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='IssToRePrcsValueTK', default=0.0)

    RtnFrmRePrcsInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='RtnFrmRePrcsInCartoon', default=0.0)
    RtnFrmRePrcsInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='RtnFrmRePrcsInLbs', default=0.0)
    RtnFrmRePrcsInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='RtnFrmRePrcsInKg', default=0.0)
    RtnFrmRePrcsValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='RtnFrmRePrcsValueTK', default=0.0)

    ClsBlnInCartoon = models.DecimalField(max_digits=18, decimal_places=2, db_column='ClsBlnInCartoon', default=0.0)
    ClsBlnInLbs = models.DecimalField(max_digits=18, decimal_places=2, db_column='ClsBlnInLbs', default=0.0)
    ClsBlnInKg = models.DecimalField(max_digits=18, decimal_places=2, db_column='ClsBlnInKg', default=0.0)
    ClsBlnValueTK = models.DecimalField(max_digits=18, decimal_places=2, db_column='ClsBlnValueTK', default=0.0)

    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE, default=100)

    class Meta:
        managed = False
        db_table = 'LogBTFG'

