from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
from enum import Enum


class User(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, upload_to='user/%Y/%m')


class gender(models.TextChoices):
    male = 'male'
    female = 'female'


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class receipt_medicine(ModelBase):
    symptom = RichTextField(max_length=255)
    diagnostic = RichTextField(max_length=255)
    medicines = models.ManyToManyField('medicine', through='receipt_medicine_detail', related_name='receipt_madicine', blank=True)
    patient = models.ForeignKey('patient', related_name='receipt_medicine', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.patient)


class examination_schedule(ModelBase):
    date_examination = models.DateTimeField()
    examination_schedule_patient = models.ForeignKey('patient', related_name='examination_schedule', on_delete=models.CASCADE)



class patient(ModelBase):
    user = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = gender = models.CharField(
        max_length=50,
        choices=gender.choices,
        default=gender.male,
    )
    phone = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class medicine(ModelBase):
    name = models.CharField(max_length=100, null=False, unique=True)
    quantity = models.IntegerField()
    price = models.CharField(max_length=255, null=True)
    description = RichTextField(max_length=255, null=True)
    image = models.ImageField(upload_to="medicine/%Y/%m")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class receipt_medicine_detail(ModelBase):
    receipt_medicine = models.ForeignKey(receipt_medicine, related_name='detail', on_delete=models.CASCADE)
    medicine = models.ForeignKey(medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    use = RichTextField(max_length=255)


    def __str__(self):
        return str(self.id)


class category_medicine(ModelBase):
    name = models.CharField(max_length=255)
    medicine = models.ManyToManyField(medicine, related_name='category_medicine', blank=True)

    def __str__(self):
        return self.name


class bill(ModelBase):
    bill_receipt_medicine = models.ForeignKey(receipt_medicine, on_delete=models.CASCADE)
    amount_of_money = models.CharField(max_length=255)
    
    
class Comment(ModelBase):
    content = models.TextField()
    medicine = models.ForeignKey(medicine,   related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class ActionBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(medicine, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = ('user', 'medicine') #chỉ lưu mỗi người 1 lần, lần sau thì đè lên lần trc


class Like(ActionBase):
    active = models.BooleanField(default=False)


class Rating(ActionBase):
    rate = models.SmallIntegerField(default=0)





