from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Destination, Trip, Itinerary
from .forms import DestinationForm, TripForm, ItineraryForm
from django.contrib import messages
from .forms import UserRegisterForm,ReviewForm
from .models import Destination, Activity, Review
from .models import Trip, Activity, TripActivity
from django.utils import timezone

# Home Page
def home(request):
    destinations = Destination.objects.all()
    featured_destinations = Destination.objects.filter(is_featured=True)
    return render(request, 'safar_app/home.html', {'featured_destinations': featured_destinations})


def search_view(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Destination.objects.filter(name__icontains=query)
        return render(request, 'safar_app/search_results.html', {
        'query': query,
        'results': results
    })

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'safar_app/login.html')

# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'safar_app/register.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("✅ Registration successful")
            return redirect('dashboard')
        else:
            print("❌ Form is invalid:", form.errors)
    else:
        form = UserRegisterForm()

    return render(request, 'safar_app/register.html', {'form': form})

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')

# Destination Listing
def destinations(request):
    destinations = Destination.objects.all()
    return render(request, 'safar_app/destinations.html', {'destinations': destinations})

# Destination Detail
def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    activities = Activity.objects.filter(destination=destination)
    reviews = Review.objects.filter(destination=destination).order_by('-date_posted')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.destination = destination
            review.save()
            return redirect('destination_detail', destination_id=destination.id)
    else:
        form = ReviewForm()

    return render(request, 'destination_detail.html', {
        'destination': destination,
        'activities': activities,
        'reviews': reviews,
        'form': form,
    })


# Trip Planning Page
@login_required
def plan_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('dashboard')
    else:
        form = TripForm()
    return render(request, 'safar_app/plan_trip.html', {'form': form})

@login_required
def add_activity_to_trip(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    try:
        trip = Trip.objects.filter(user=request.user, destination=activity.destination).latest('id')
    except Trip.DoesNotExist:
        return redirect('add_trip')  # Ask them to create a trip first

    TripActivity.objects.create(trip=trip, activity=activity)
    return redirect('destination_detail', destination_id=activity.destination.id)

@login_required
def view_itinerary(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    activities = TripActivity.objects.filter(trip=trip)
    return render(request, 'safar_app/itinerary.html', {'trip': trip, 'activities': activities})

# User Dashboard
@login_required
def dashboard(request):
    today = timezone.now().date()
    trips = Trip.objects.filter(user=request.user)

    upcoming_trips = trips.filter(start_date__gte=today)
    past_trips = trips.filter(end_date__lt=today)

    context = {
        'upcoming_trips': upcoming_trips,
        'past_trips': past_trips,
        'total_trips': trips.count(),
    }
    return render(request, 'safar_app/dashboard.html', context)


# Itinerary Page
@login_required
def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user)
    return render(request, 'safar_app/itinerary.html', {'itineraries': itineraries})

# Add a New Destination
@login_required
def add_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('destinations')
    else:
        form = DestinationForm()
    return render(request, 'safar_app/add_destination.html', {'form': form})

# Add a New Trip
@login_required
def add_trip(request):
    destination_id = request.GET.get('destination_id')
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('dashboard')
    else:
        initial_data = {}
        if destination_id:
            try:
                destination = Destination.objects.get(id=destination_id)
                initial_data['destination'] = destination
            except Destination.DoesNotExist:
                pass
        form = TripForm(initial=initial_data)
    return render(request, 'safar_app/add_trip.html', {'form': form})

# List Trips for the Logged-in User
@login_required
def trip_list(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'safar_app/trips.html', {'trips': trips})

@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    available_activities = Activity.objects.filter(destination=trip.destination)
    selected_activities = TripActivity.objects.filter(trip=trip).select_related('activity')

    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        activity = get_object_or_404(Activity, id=activity_id)
        TripActivity.objects.get_or_create(trip=trip, activity=activity)
        return redirect('trip_detail', trip_id=trip.id)

    return render(request, 'safar_app/trip_detail.html', {
        'trip': trip,
        'available_activities': available_activities,
        'selected_activities': selected_activities,
    })

@login_required
def add_to_trip(request, activity_id, trip_id):
    activity = get_object_or_404(Activity, id=activity_id)
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    # Check if already added
    exists = TripActivity.objects.filter(trip=trip, activity=activity).exists()
    if not exists:
        TripActivity.objects.create(trip=trip, activity=activity)
        messages.success(request, "Activity added to your trip!")
    else:
        messages.info(request, "Activity is already in your trip plan.")

    return redirect('trip_detail', trip_id=trip.id)

# Add a New Itinerary Entry
@login_required
def add_itinerary(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard or trip detail
    else:
        form = ItineraryForm()
    return render(request, 'safar_app/add_itinerary.html', {'form': form})
