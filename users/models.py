from django.db import models
from django.contrib.auth.models import User as authUser
from sorl.thumbnail import ImageField
import uuid
from solutioner.users.country_field import COUNTRIES2 as COUNTRY_CHOICES
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class OwnershipManager(models.Manager):
  def create_ownership(self, owner_inst, object_inst):
    owner_ct = ContentType.objects.get_for_model(owner_inst)
    owner_id = owner_inst.id
    object_ct = ContentType.objects.get_for_model(object_inst)
    object_id = object_inst.id
    
    return Ownership.objects.create(owner_ct=owner_ct, owner_id=owner_id, object_ct=object_ct, object_id=object_id)

  def get_or_create_ownership(self, owner_inst, object_inst):
    try:
      return Ownership.objects.get(object_ct = ContentType.objects.get_for_model(object_inst), object_id = object_inst.id), False
    except:
      owner_ct = ContentType.objects.get_for_model(owner_inst)
      owner_id = owner_inst.id
      object_ct = ContentType.objects.get_for_model(object_inst)
      object_id = object_inst.id
      return Ownership.objects.create(owner_ct=owner_ct, owner_id=owner_id, object_ct=object_ct, object_id=object_id), True
    
  
  def get_ownership(self, object_inst):
    try:
      return Ownership.objects.get(object_ct = ContentType.objects.get_for_model(object_inst), object_id = object_inst.id)
    except:
      return None
      
  def get_ownership_ct_id(self, object_inst):
    try:
      owner = Ownership.objects.get(object_ct = ContentType.objects.get_for_model(object_inst), object_id = object_inst.id)
      return owner.owner_ct, owner.owner_id
    except:
      return None
    
class Ownership(models.Model):
  owner_ct = models.ForeignKey(ContentType, related_name='ownership_owner')
  owner_id = models.PositiveIntegerField()
  object_ct = models.ForeignKey(ContentType, related_name='ownership_object')
  object_id = models.PositiveIntegerField()
  is_suspended = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)

  owner = generic.GenericForeignKey('owner_ct', 'owner_id')
  object = generic.GenericForeignKey('object_ct', 'object_id')

  objects = OwnershipManager()
  
  class Meta:
    unique_together = ('object_ct', 'object_id')
   
  def __unicode__(self):
    return '%s | %s | %s' % (self.owner, self.object)


class License(models.Model):
  license = models.CharField(max_length=100)
  license_url = models.CharField(max_length=10000)

  def __unicode__(self):
    return '%s'%(self.license)

class Source(models.Model):
  source = models.CharField(max_length=100)
  url = models.CharField(max_length=200)
  image = models.CharField(max_length=200)
  description = models.CharField(max_length=1000)
  like = models.ManyToManyField(authUser, blank=True, null=True, default=None, related_name='sourceslike_users')
  licenses = models.ManyToManyField(License, blank=True, null=True, default=None, related_name='licenses_users')
  viewed = models.BigIntegerField(blank=True, null=True, default=0)
  is_deleted = models.BooleanField(default=False)
  
  def __unicode__(self):
    return '%s'%(self.source)

def content_file_name(instance, filename):
  ext = filename.split('.')[-1]
  filename = "%s.%s" % (uuid.uuid4(), ext)
  return '/'.join(['profiles/pictures', filename])

GENDER_CHOICES = (
  ('N', '-'),
  ('M', 'Male'),
  ('F', 'Female'),
)


class User(models.Model):
  user = models.ForeignKey(authUser)
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
  image = models.ImageField(upload_to=content_file_name)
  location = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default='N')
  birthdate = models.DateField(blank=True, null=True)
  website = models.CharField(blank=True, null=True, max_length=1000)
  following = models.ManyToManyField(authUser, blank=True, null=True, default=None, related_name='users_usersfollowing')
  last_checked_id = models.BigIntegerField(default=0)
  is_suspended = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)
  
  def __unicode__(self):
    return '%s'%(self.user)
    
class NotificationSettings(models.Model):
  user = models.ForeignKey(authUser)
  comment_on_desk = models.BooleanField(default=True)
  comment_on_solution = models.BooleanField(default=True)
  is_deleted = models.BooleanField(default=False)
  
  def __unicode__(self):
    return '%s'%(self.user)

 
class ExternalUser(models.Model):
  source = models.ForeignKey(Source)
  username = models.CharField(max_length=100)
  image = models.CharField(blank=True, max_length=1000)
  url = models.CharField(blank=True, max_length=1000)
  is_suspended = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)
  
  def __unicode__(self):
    return '%s'%(self.username)
    


