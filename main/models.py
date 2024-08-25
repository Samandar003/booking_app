from django.db import models
from django.utils import timezone
from users.models import CustomUserModel
# this app is for reserving pitches, pools, billiard, 

class InstitutionModel(models.Model):
    SERVICE_TYPES=(
        ("Massage", "Massage"),
        ("Pool", "Pool"),
        ("Billiard", "Billiard"),
        ("Pitch", "Pitch"),
        ("Barbershop", "Barbershop"),
        ("Football Pitch", "Football Pitch"),
    )
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    street_number=models.CharField(max_length=100, blank=True)
    city=models.CharField(max_length=200, blank=True)
    municipality=models.CharField(max_length=100)
    owner=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    price_hour=models.DecimalField(max_digits=10, decimal_places=2)
    contact=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    type=models.CharField(choices=SERVICE_TYPES, max_length=200)
    description=models.TextField()
    likes=models.PositiveIntegerField(default=0, blank=True)
    dislikes=models.PositiveIntegerField(default=0, blank=True)
    how_many=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.name} {self.owner}"

DAY_CHOICES = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )

class ScheduleModel(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )

    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    day=models.CharField(choices=DAY_CHOICES, max_length=200)
    institution=models.ForeignKey(InstitutionModel, on_delete=models.CASCADE)
    client=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    reservation_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return "Schedule of "+self.institution.name



class PostInstitModel(models.Model):
    institution=models.ForeignKey(InstitutionModel, on_delete=models.CASCADE)
    picture=models.ImageField(upload_to="media/")    
    description=models.TextField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.picture.name+" "+self.description
    
            
class WorkingHoursModel(models.Model):
    day = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    institution=models.ForeignKey(InstitutionModel, on_delete=models.CASCADE, related_name="working_hours")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_day_display()}: {self.open_time.strftime('%I:%M %p')} - {self.close_time.strftime('%I:%M %p')}"


