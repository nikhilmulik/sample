from django.db import models


class MawbDetail(models.Model):
    paLocked = models.NullBooleanField(null=True)
    paLockedByUser = models.CharField(max_length=200, null=True)
    preAlertReceivedDate = models.DateField(auto_now_add=True, null=True)
    preAlertReceivedTime = models.TimeField(auto_now_add=True, null=True)
    lastUpdatedByUser = models.CharField(max_length=200, null=True)
    lastUpdatedDate = models.DateField(auto_now_add=True, null=True)
    lastUpdatedTime = models.TimeField(auto_now_add=True, null=True)
    mawbNum = models.CharField(max_length=200, null=True)  # db_index=True,
    station = models.CharField(max_length=200, null=True)
    consoleNumber = models.DecimalField(max_digits=6, decimal_places=0, null=True)
    customer = models.CharField(max_length=200, null=True)
    etdDate = models.DateField(auto_now_add=True, null=True)
    etdTime = models.TimeField(auto_now_add=True, null=True)
    etaDate = models.DateField(auto_now_add=False, null=True)
    etaTime = models.TimeField(auto_now_add=False, null=True)
    ataDate = models.DateField(auto_now_add=True, null=True)
    ataTime = models.TimeField(auto_now_add=True, null=True)
    flightCode = models.CharField(max_length=20, null=True)
    flightNum = models.CharField(max_length=20, null=True)
    slac = models.DecimalField(max_digits=5, decimal_places=0, null=True)
    chgWeight = models.DecimalField(max_digits=5, decimal_places=0, null=True)
    pmcOrLoose = models.CharField(max_length=200, null=True)
    remarksInClass = models.CharField(max_length=200, null=True)
    shipmentStatus = models.CharField(max_length=200, null=True)
    cobDate = models.DateField(auto_now_add=True, null=True)
    recoveryNum = models.CharField(max_length=200, null=True)
    oneFStatus = models.CharField(max_length=200, null=True)
    oneFStatusComment = models.CharField(max_length=200, null=True)
    ppComments = models.CharField(max_length=200, null=True)
    ppCommentsBy = models.CharField(max_length=200, null=True)
    ppCommentsAt = models.DateTimeField(auto_now=True, null=True)
    totalHblNum = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    pendingHblNum = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    spProStatus = models.CharField(max_length=200, null=True)
    spCommentOfHcl = models.CharField(max_length=200, null=True)
    spCommentOfHclBy = models.CharField(max_length=200, null=True)
    spCommentOfHclAt = models.DateTimeField(auto_now=True, null=True)
    spCommentOfCeva = models.CharField(max_length=200, null=True)
    spCommentOfCevaBy = models.CharField(max_length=200, null=True)
    spCommentOfCevaAt = models.DateTimeField(auto_now=True, null=True)
    recoveryOrBO = models.CharField(max_length=200, null=True)
    aiDesc = models.CharField(max_length=200, null=True)
    papFlag = models.NullBooleanField(null=True)
    pamFlag = models.NullBooleanField(null=True)
    createAIStatus = models.IntegerField(null=True)
    createAIDesc = models.CharField(max_length=200, null=True)
    itInfo = models.CharField(max_length=200, null=True)
    updateTodayFlag = models.NullBooleanField(null=True)
    trackSource = models.CharField(max_length=10, null=True)
    speakWith = models.CharField(max_length=10, null=True)
    updateRemarkStatus = models.IntegerField(null=True)
    getConsoleStatus = models.IntegerField(null=True)
    getConsoleDesc = models.CharField(max_length=200, null=True)
    updateRemarksDesc = models.CharField(max_length=200, null=True)
    deletedFlag = models.NullBooleanField(null=True)

    def __unicode__(self):
        return self.mawbNum


class HawbDetail(models.Model):
    mawbNum = models.CharField(max_length=200)
    hawbNum = models.CharField(max_length=200)
    consignee = models.CharField(max_length=200)
    wpStatus = models.CharField(max_length=200)
    wpComments = models.CharField(max_length=200)
    wpCommentsBy = models.CharField(max_length=200)
    wpCommentsAt = models.DateTimeField(auto_now=False)

    def __unicode__(self):
        return self.hawbNum


class UserCountDetail(models.Model):
    userName = models.CharField(max_length=200)
    totalCounts = models.PositiveSmallIntegerField()
    avgTime = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.userName


class AirLinesDetail(models.Model):
    stnName = models.CharField(max_length=200)
    prefixNum = models.CharField(max_length=200)
    prefix = models.CharField(max_length=200)
    airlineName = models.CharField(max_length=200)
    phoneNum = models.CharField(max_length=200)
    extNum = models.CharField(max_length=200)
    faxNum = models.CharField(max_length=200)
    firms = models.CharField(max_length=200)
    otherNum = models.CharField(max_length=200)
    businessHrs = models.CharField(max_length=200)
    handlingAgent = models.CharField(max_length=200)
    storagePyblTo = models.CharField(max_length=200)
    freeDays = models.CharField(max_length=200)
    iscChgsPyblTo = models.CharField(max_length=200)
    chgsPyblTo = models.CharField(max_length=200)

    def __unicode__(self):
        return self.airlineName
