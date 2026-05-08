from django.shortcuts import render,get_object_or_404,redirect
from hotel.models import Hotel,Booking,Activitylog,StaffOnDuty,Room,RoomType,HotelFags,HotelFeatures,HotelGallery,HotelCartItem
from .forms import UpdateQuantityForm
from .forms import BookingForm






# Create your views here.

def index(request):
    hotels = Hotel.objects.filter(status="Live")
    
    context={'hotels': hotels}
    
    return render(request, "hotel/hotel.html", context)


def rooms(request):
    hotels = Hotel.objects.all()
    context={'hotels': hotels,}
    
    return render(request, "hotel/rooms.html", context)

def about(request):

    return render(request, "hotel/about.html")

def hotel_detail(request,slug):
    hotel = Hotel.objects.get( slug=slug)
    hotels = Hotel.objects.filter(slug=slug)
    room_types = RoomType.objects.filter(hotel=hotel)
    hotel_features = HotelFeatures.objects.filter(hotel=hotel)
    hotel_faqs = HotelFags.objects.filter(hotel=hotel)

    context={
        'hotel': hotel,
        'hotels': hotels,
        'room_types': room_types,
        'hotel_features': hotel_features,
        'hotel_faqs': hotel_faqs,
    }
    return render(request, "hotel/hotel_detail.html", context)

def view_cart(request):
    cart_items = HotelCartItem.objects.filter(user=request.user)
    total_price = sum(item.room_type.price * item.quantity for item in cart_items)
    
   
    return render(request, 'hotel/newcart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_hotel_to_cart(request, hotel_slug):
    hotel = Hotel.objects.get(slug=hotel_slug)
    room_types = RoomType.objects.filter(hotel=hotel)
    
    
    for room_type in room_types:
        user_id = request.user.id
        cart_item, created = HotelCartItem.objects.get_or_create(room_type=room_type, user_id=user_id)
        cart_item.quantity += 1
        cart_item.save()

    return redirect('hotel:view_cart')

def remove_from_cart(request, item_id):
	cart_item = HotelCartItem.objects.get(id=item_id)
	cart_item.delete()
	return redirect('hotel:view_cart')


def update_quantity(request, item_id):
    item = HotelCartItem.objects.get(pk=item_id)

    if request.method == 'POST':
        form = UpdateQuantityForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            item.quantity = new_quantity
            item.save()
            # Redirect to the cart page after updating the quantity
            return redirect('hotel:view_cart')
    else:
        form = UpdateQuantityForm(initial={'quantity': item.quantity})

    return render(request, 'hotel/newcart.html', {'form': form, 'item': item})





def create_booking(request, slug):
    hotel = Hotel.objects.get(slug=slug)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Set the hotel field of the form to the current hotel
            form.instance.hotel = hotel

            # Save the form data to the database
            booking_instance = form.save()

            # Redirect to the hotel detail page with the same slug
            return redirect('hotel:hotel-detail', slug=slug)
    else:
        form = BookingForm()

    return render(request, 'hotel/create_booking.html', {'form': form, 'hotel': hotel})


















