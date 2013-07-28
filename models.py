from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

# phone number regex
pnum_pattern = re.compile(r'[0-9]{10}')

def validate_pnum(pnum):
    """Raise validation error if not a 10 digit phone number"""
    if not re.match(pnum_pattern, pnum):
        raise ValidationError(u'%s is not a valid phone number'%pnum)

class Carrier(models.Model):
    """Model connecting cellular SMS providers to email addresses"""
    name = models.CharField(max_length=32)
    gateway = models.CharField(max_length=64)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name

class User(models.Model):
    """Model describing a user of the Pester app"""
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(
        validators=[validate_pnum],
        unique=True,
        max_length=10)
    carrier = models.ForeignKey(Carrier)

    def __unicode__(self):
        return (self.last_name+', '+self.first_name+
                ' -- e['+self.email+'] p['+self.phone_number+']')

class Recipient(models.Model):
    """Model decribing a potential recipient of a pester"""
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        validators=[validate_pnum],
        unique=True,
        max_length=10)                    
    carrier = models.ForeignKey(Carrier)
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return (self.last_name+', '+self.first_name+
                ' -- e['+self.email+'] p['+self.phone_number+']')

class Pattern(models.Model):
    """Model describing a sending pattern for a Pestering"""
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

class Pestering(models.Model):
    """Model describing a pestering from User to Recipient"""
    user = models.ForeignKey(User)
    recipient = models.ForeignKey(Recipient)
    search_term = models.CharField(max_length=64)
    pattern = models.ForeignKey(Pattern)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    EMAIL = 'E'
    TEXT = 'T'
    BOTH = 'B'
    NOTIFY_METHODS = (
        (EMAIL, 'By Email'),
        (TEXT, 'By Text'),
        (BOTH, 'By Text and Email'),
    )
    notify_user_method = models.CharField(
        max_length=1,
        choices=NOTIFY_METHODS,
        default=EMAIL)
    notify_recipient_method = models.CharField(
        max_length=1,
        choices=NOTIFY_METHODS,
        default=EMAIL)

    def __unicode__(self):
        return ''.join((str(self.user.first_name),
                        ' -> ',
                        str(self.recipient.first_name),
                        ' | ',
                        str(self.pattern)))
    
    def is_pestering(self):
        return (self.start_time <= timezone.now() and 
                timezone.now() <= self.end_time)

class Image(models.Model):
    """Model describing """
    search_term = models.CharField(max_length=64)
    url = models.URLField(unique=True)

    def __unicode__(self):
        return self.search_term+' ('+self.url+')'

class SentPestering(models.Model):
    """Model to record sent Pesterings"""
    pestering = models.ForeignKey(Pestering)
    image = models.ForeignKey(Image)
    send_time = models.DateTimeField()
    success = models.NullBooleanField()
    notes = models.CharField(max_length=64)

    def __unicode__(self):
        return self.pestering+' sent at '+self.sent_time
