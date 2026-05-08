from django.urls import path

from hotel import views

app_name = "hotel"

urlpatterns = [
    path("", views.index, name="index"),
    path("rooms/", views.rooms, name="rooms"),
    path("about/", views.about, name="about"),
    path("detail/<slug>/", views.hotel_detail, name="hotel-detail"),
    path("detail/<slug>/", views.hotel_detail, name="hotel-detail"),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('add_hotel_to_cart/<slug:hotel_slug>/', views.add_hotel_to_cart, name='add_hotel_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('booking/<slug:slug>', views.create_booking, name='create_booking'),

]