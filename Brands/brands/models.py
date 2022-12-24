from django.db import models

class Brands(models.Model):
    Bname = models.CharField(max_length=250,null=True,blank=True,verbose_name='Brand Name')
    Bdescription = models.TextField(null=True,blank=True,verbose_name='Description')
    
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        
    def __str__(self):
        return self.Bname