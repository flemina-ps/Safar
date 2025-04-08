# safar_app/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views  # Make sure you have views defined in safar_app/views.py

urlpatterns = [

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='safar_app/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Main Pages
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Destinations
    path('destinations/', views.destinations, name='destinations'),
    path('destination_detail/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    path('add-destination/', views.add_destination, name='add_destination'),

    # Trip Planning
    path('plan_trip/', views.plan_trip, name='plan_trip'),
    path('add-trip/', views.add_trip, name='add_trip'),

    # Itineraries
    path('itinerary/', views.itinerary_list, name='itinerary'),
    path('add-itinerary/', views.add_itinerary, name='add_itinerary'),

    # Search
    path('search/', views.search_view, name='search'),

    # Activity
    path('add-activity/<int:activity_id>/', views.add_activity_to_trip, name='add_activity'),

    path('itinerary/<int:trip_id>/', views.view_itinerary, name='view_itinerary'),

    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),

    path('add-to-trip/<int:activity_id>/<int:trip_id>/', views.add_to_trip, name='add_to_trip'),

    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)