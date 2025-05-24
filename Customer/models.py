
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone
 



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


def upload_to_customer(instance, filename):
    return f'customers/{instance.user.username}/{filename}'

def upload_to_staff(instance, filename):
    return f'staff/{instance.user.username}/{filename}'


class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ration_card_number = models.CharField(max_length=20, unique=True)
    family_members_count = models.PositiveIntegerField()
    ration_type = models.CharField(max_length=10, choices=(('APL', 'APL'), ('BPL', 'BPL')))

    # New address fields
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
   

    # New image field
    image = models.ImageField(upload_to=upload_to_customer, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Customer"


class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    center_assigned = models.CharField(max_length=100)

    # New address fields
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    # New image field
    image = models.ImageField(upload_to=upload_to_staff, blank=True, null=True)

    noOfTokenBooked=models.IntegerField(default=0)
    tokenUsed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Staff"
    

class Token(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_tokens')
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='staff_tokens')
    token_number = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    in_queue=models.BooleanField(default=False)
    is_used=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return f"Token #{self.token_number} for {self.customer.username} with {self.staff.username}"

