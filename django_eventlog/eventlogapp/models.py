from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import URLValidator, MinValueValidator
from eventlog.models import log


class Milestone(models.Model):

    MILESTONE_STATUS=(
        ('Achieved','Achieved'),
        ('Remained','Remained'),
    )
    title = models.CharField(max_length=100, null = True, blank = True)
    date = models.DateField(null = True, blank = True)
    modified_date = models.DateField(null = True, blank = True)
    feedback = models.TextField(null = True, blank = True)
    status = models.CharField(max_length=30, choices = MILESTONE_STATUS, null = True, blank = True)
    created_by = models.ForeignKey(User, related_name = 'milestone_created_by', null = True, blank = True)
    updated_by = models.ForeignKey(User, related_name = 'milestone_updated_by', null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    #for milestone log
    def save(self, **kwargs):
        if not self.id:
            log(user=self.created_by, action='NEW MILESTONE ADDED',
                obj = self,
                extra={"title": self.title,
                        "date":str(self.date),
                        "modified_date":str(self.modified_date),
                        "feedback":self.feedback,
                        "status":self.status,
                        })
        else:
            log(user=self.updated_by, action='MILESTONE UPDATED',
                obj = self,
                extra={"title": self.title,
                        "date":str(self.date),
                        "modified_date":str(self.modified_date),
                        "feedback":self.feedback,
                        "status":self.status,
                        })
        super(Milestone, self).save( kwargs)

    def __str__(self):
        return 'Title: {}, Date: {}'.format(self.title,self.date)


#model for Transaction
class Transaction(models.Model):
    milestone = models.ForeignKey(Milestone, null = True, blank = True)
    date = models.DateField(null = True, blank = True)
    amount = models.FloatField(validators = [MinValueValidator(0)],default = 0, null = True, blank = True)
    provider_org_name = models.CharField(max_length = 70, null = True, blank = True)
    receiver_org_name = models.CharField(max_length = 70, null = True, blank = True)
    changes = models.TextField(null = True, blank = True)
    created_by = models.ForeignKey(User, related_name = 'transaction_created_by', null = True, blank = True)
    updated_by = models.ForeignKey(User, related_name = 'transaction_updated_by', null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def editable(self):
        if self.created_by == self.request.user:
            transaction = Transaction(edit = True)
            self.transaction = transaction
            self.save()
            return self.transaction

    #for transaction log
    def save(self, **kwargs):
        if not self.id:
            log(user=self.created_by, action='NEW TRANSACTION ADDED',
                obj = self,
                extra={"milestone": str(self.milestone),
                        "transaction_date":str(self.date),
                        "transaction_amount":self.amount,
                        "provider_organization_name":self.provider_org_name,
                        "receiver_organization_name":self.receiver_org_name,
                        "amendment_changes":self.changes,
                        })
        else:
            log(user=self.updated_by, action='UPDATED TRANSACTION',
                obj = self,
                extra={"milestone": str(self.milestone),
                        "transaction_date":str(self.date),
                        "transaction_amount":self.amount,
                        "provider_organization_name":self.provider_org_name,
                        "receiver_organization_name":self.receiver_org_name,
                        "changes":self.changes,
                        })
        super(Transaction, self).save( kwargs)

    def __str__(self):
        return 'Milestone: {}, Transaction Amount: {}'.format(self.milestone,self.amount)

