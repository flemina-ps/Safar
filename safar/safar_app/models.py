from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Destination Model
class Destination(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='destination_images/')
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    tagline = models.CharField(max_length=150, blank=True)
    rating = models.FloatField(default=4.5)
    review_count = models.IntegerField(default=0)
    history = models.TextField(blank=True)
    tips = models.TextField(blank=True)
    weather = models.TextField(blank=True)
    best_time_to_visit = models.TextField(blank=True)
    category = models.CharField(max_length=100, choices=[
        ('Adventure', 'Adventure'),
        ('Relaxation', 'Relaxation'),
        ('Food', 'Food'),
        ('Culture', 'Culture'),
    ])
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
# Trip Model
class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s trip to {self.destination.name}"
    

# Iternary Model
class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="itineraries")
    day = models.IntegerField()
    activities = models.TextField()

    def __str__(self):
        return f"Day {self.day} - {self.trip.destination.name}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending')])

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='activity_images/', blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class TripActivity(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.activity.title} in {self.trip}"

class Review(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}★"
