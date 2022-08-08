from django.utils import timezone

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


status_choices = (
    ("NEW", "New"),
    ("PREPAYMENT", "Prepayment"),
    ("InPROGRESS", 'In Progress'),
    ("DONE", 'Done'),
    ("PAID", 'Paid'),
    ("CakeHandedOver", "Cake handed over"),
    ("DECLINED", 'Declined')
)


def validation_min_length(value):
    if len(value) < 5:
        raise ValidationError(
            _('%(value)s is so small'),
            params={'value': value},
        )


def validation_max_value_mark(value):
    if value > 4 or value < 0:
        raise ValidationError(
            _('%(value)s is invalid'),
            params={'value': value},)


def validation_date_time(value):
    if value < timezone.now():
        raise ValidationError(
            _('%(value)s is invalid date. Please, enter the date that will be bigger than now.'),
            params={'value': value},)


class Cake(models.Model):
    title = models.CharField(max_length=50, unique=True, validators=[validation_min_length])
    description = models.CharField(max_length=250, null=True, blank=True)
    cake_img = models.ImageField(null=True, blank=True, upload_to='')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title


class Confectioner(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customer(AbstractUser):
    first_name = models.CharField(max_length=20, default=' ')
    username = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=20, default=' ')
    phone_number = models.IntegerField(default=12356423)
    password = models.CharField(max_length=18)
    email = models.EmailField(max_length=35)

    def __str__(self):
        return self.last_name


class OrderC(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    confectioner = models.ForeignKey(Confectioner, on_delete=models.CASCADE, default=1)
    time_date_order = models.DateTimeField(validators=[validation_date_time])
    prise_sum = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=18, choices=status_choices, default="New")
    # price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    # weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    cakes = models.ManyToManyField(Cake)

    def __str__(self):
        return str(self.id)


# class OrderItem(models.Model):
#     cake_id = models.OneToOneField(Cake, on_delete=models.PROTECT)
#     order_id = models.OneToOneField(OrderC, on_delete=models.CASCADE)
#     # cake_id = models.ForeignKey(Cake, on_delete=models.PROTECT, primary_key=True)
#     # orderc_id = models.ForeignKey(OrderC, on_delete=models.CASCADE, primary_key=True)
#     count = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     weight = models.DecimalField(max_digits=5, decimal_places=2)
#
#     def __str__(self):
#         return self.cake_id.title


class Blog(models.Model):
    confectioner = models.ForeignKey(Confectioner, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    mark = models.IntegerField(validators=[validation_max_value_mark])
    text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.mark)
