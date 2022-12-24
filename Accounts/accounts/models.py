import datetime
from distutils.command.upload import upload
from email.message import EmailMessage
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.forms import ImageField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.conf import settings
from PIL import Image





# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    image = models.ImageField(verbose_name=_("image"),upload_to='profile_img',blank=True,null=True)
    ph_number = models.CharField(max_length=20,verbose_name=_("Phone Number"),blank=True,null=True)
    country = CountryField()
    slug = models.SlugField(blank=True,null=True)
    join_date = models.DateTimeField(verbose_name=_("join_date"),default=datetime.datetime.now)


    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        return super(Profile,self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("Profile_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return str(self.user)


def Email_verification(sender, instance,created, **kwargs):
    if created:
        subject = 'Welcome To E6-Commerce-App'
        body = 'Hi You have been registered successfully, We are glad to have you join us'
        email = (instance.email)
 
        send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER, 
        [email],
        fail_silently=False
)
post_save.connect(Email_verification, sender=User)

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
  
post_save.connect(create_profile, sender=User)


