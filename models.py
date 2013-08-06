import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# phone number regex
pnum_pattern = re.compile(r'[0-9]{10}')

def validate_pnum(pnum):
    """Raise validation error if not a 10 digit phone number"""
    if not re.match(pnum_pattern, pnum):
        raise ValidationError(u'%s is not a valid phone number'%pnum)


class API(models.Model):
    """Model detialing the API params"""
    name = models.CharField(max_length=32)
    key = models.CharField(max_length=200)
    params = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

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
    code = models.CharField(max_length=32)

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
        default=TEXT)
    title = models.CharField(max_length=140)
    OFF, MEDIUM, HIGH = 'O', 'M', 'H'
    ADULT_LEVELS = (
            (OFF, 'Off'),
            (MEDIUM, 'Medium'),
            (HIGH, 'High'))
    adult_safety_level = models.CharField(
            max_length=1,
            choices=ADULT_LEVELS,
            default=MEDIUM)

    def __unicode__(self):
        return ''.join((str(self.user.first_name),
                        ' -> ',
                        str(self.recipient.first_name),
                        ' | ',
                        str(self.search_term),
                        ' | ',
                        str(self.pattern)))

class ImageData(models.Model):
    """Model describing """
    search_term = models.CharField(max_length=64)
    url = models.URLField(unique=True)
    file_type = models.CharField(max_length=64)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    OFF, MEDIUM, HIGH = 'O', 'M', 'H'
    ADULT_LEVELS = (
            (OFF, 'Off'),
            (MEDIUM, 'Medium'),
            (HIGH, 'High'))
    adult_safety_level = models.CharField(
            max_length=1,
            choices=ADULT_LEVELS,
            default=MEDIUM)

    def __unicode__(self):
        return self.search_term+' ('+self.url+')'

class PesteringManagerRun(models.Model):
    """Model to record cron jobs and their success"""
    run_time = models.DateTimeField(auto_now_add=True)
    completed = models.NullBooleanField()

    def __unicode__(self):
        return str(self.run_time)

class PesteringAttempt(models.Model):
    """Model to record attempted Pesterings"""
    pestering = models.ForeignKey(Pestering)
    pestering_manager_run = models.ForeignKey(PesteringManagerRun)
    image = models.ForeignKey(ImageData, null=True, blank=True, default=None)
    attempt_time = models.DateTimeField(auto_now_add=True)
    success = models.NullBooleanField()

    def __unicode__(self):
        return str(self.pestering)+' sent at '+str(self.attempt_time)

class PesteringException(models.Model):
    """Model to record exceptions of Pesterings"""
    pestering_attempt = models.ForeignKey(PesteringAttempt)
    exception_traceback = models.TextField()

    def __unicode__(self):
        return 'Exception for Pestering Attempt '+str(self.pestering_attempt)
