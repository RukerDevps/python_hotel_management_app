from django.db import models
from django.utils.text import slugify 
from django.utils.html import mark_safe
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

# Create your models here.

HOTEL_STATUS =(
    ('Draft', 'Draft'),
    ('Disable', 'Disable'),
    ('Rejected', 'Rejected'),
    ('In Review', 'In Review'),
    ('Live', 'Live'),
)

ICON_TYPE =(
    ('Bootsrap Icons', 'Bootsrap Icons'),
    ('Fontawesome Icons', 'Fontawesome Icons'),
    ('Box Icons', 'Box Icons'),
    ('Remi Icons', 'Remi Icons'),
    ('Flat Icons', 'Flat Icons'),
)

PAYMENT_STATUS =(
    ('Paid', 'Paid'),
    ('Pending', 'Pending'),
    ('Rejected', 'Rejected'),
    ('Processing', 'Processing'),
    ('cancelled', 'cancelled'),
    ('failed', 'failed'),
    ('refunding', 'refunding'),
    ('refunded', 'refunded'),
    ('unpaid', 'unpaid'),
    ('expired', 'expired'),
    
)


class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = CKEditor5Field(null=True, blank=True, config_name='extends')
    address = models.CharField(max_length=256)
    image = models.FileField(upload_to = "hotel_gallery")
    mobile = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=HOTEL_STATUS, default = "Live")

    tags = TaggableManager( blank=True)
    views = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    hid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz" )
    slug = models.SlugField(unique=True)
    date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0, blank=True, null=True)
      

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniquied = uuid_key[:4]
            self.slug = slugify(self.name) + '-' + str(uniquied.lower())

        super(Hotel, self).save(*args, **kwargs)  

    def thumbnail(self):
        return mark_safe("<img src='%s' width='50' height='50' style='object-fit: cover; border-radius: 6px' />" % self.image.url) 

    def hotel_gallery(self):
        return HotelGallery.objects.filter(hotel=self)   
    
    def get_star_icons(self):
        if self.rating is not None:
            return f'<i class="bi bi-star-fill"></i>' * self.rating
        return ''

    def __str__(self):
        return self.name    


class HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.FileField(upload_to="hotel_gallery")
    hgid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz" )

    def __str__(self):
        return str(self.hotel.name)
    
    class Meta:
        verbose_name_plural = "Hotel Gallery"

class HotelFeatures(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    icon_type = models.CharField(max_length=100, null=True , blank=True, choices=ICON_TYPE)   
    icon = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Hotel Features"

class HotelFags(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)   
    answer = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return str(self.question)
    
    class Meta:
        verbose_name_plural = "Hotel FAQS"


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)   
    price = models.DecimalField(max_digits=12, decimal_places=2 , default=0.00)
    number_of_beds = models.PositiveIntegerField(default=0)
    room_capacity = models.PositiveIntegerField(default=0)
    rtid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")
    slug = models.SlugField(unique=True)
    date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"{self.type} - {self.hotel.name} "
    
    class Meta:
        verbose_name_plural = "Room Type"

    def rooms_count(self):
        Room.objects.filters(room_type=self).count()

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniquied = uuid_key[:4]
            self.slug = slugify(self.name) + '-' + str(uniquied.lower())

        super(RoomType, self).save(*args, **kwargs) 

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=1000)
    is_available = models.BooleanField(default=True)
    rid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_type} - {self.hotel.name} - {self.price()}"

    class Meta:
        verbose_name_plural = "Rooms"

    def price(self):
        return self.room_type.price

    def number_of_beds(self):
        return self.room_type.number_of_beds



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_user')
    payment_status = models.CharField(max_length=100, null=True, blank=True, choices=PAYMENT_STATUS)

    full_name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    phone = models.CharField(max_length=1000)

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings_hotel')
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ManyToManyField(Room)

    before_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    total_days = models.PositiveIntegerField(default=0)
    num_adults = models.PositiveIntegerField(default=0)
    num_children = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=False)

    check_in_date_tracker = models.BooleanField(default=False)
    check_out_date_tracker = models.BooleanField(default=False)

    booking_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")
    date = models.DateTimeField(auto_now_add=True)
    success_id = models.CharField(max_length=1000, null=True, blank=True)
    stripe_payment_intent = models.CharField(max_length=1000, null=True, blank=True)
    

    def __str__(self):
        return f"{self.booking_id}"    
    
    def __str__(self):
        return self.room.all().count()  
    def __str__(self):
        return f"{self.full_name} - {str(self.booking_id)}"
 
    
class Activitylog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    guess_out = models.DateTimeField()    
    guess_in = models.DateTimeField()
    discribtion = models.TextField(null=True, blank = True)
    date = models.DateTimeField(auto_now_add=True)        

    def __str__(self):
        return f"{self.booking}" 

class StaffOnDuty(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=100,null=True, blank = True )
    date = models.DateTimeField(auto_now_add=True)           

    def __str__(self):
        return f"{self.staff_id}" 
    
 
class HotelCartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    imagecart = models.ImageField(upload_to='cart_image', default='default_image.jpg')
    price = models.DecimalField(max_digits=12, decimal_places=2 , default=0.00)


    # Add other fields if needed

    def __str__(self):
        return f"{self.quantity} x {self.room_type} in cart for {self.user.username}" 


