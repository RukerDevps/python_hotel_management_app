from django.contrib import admin
from hotel.models import Hotel,Booking,Activitylog,StaffOnDuty,Room,RoomType,HotelFags,HotelFeatures,HotelGallery,HotelCartItem

# Register your models here.

class HotelGalleryInline(admin.TabularInline):
    model= HotelGallery

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelGalleryInline]
    list_display = ['thumbnail', 'name','user','status']
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Hotel, HotelAdmin)    
admin.site.register(Booking)    
admin.site.register(Activitylog)    
admin.site.register(StaffOnDuty)    
admin.site.register(Room)    
admin.site.register(RoomType)    
admin.site.register(HotelGallery)    
admin.site.register(HotelFags)    
admin.site.register(HotelFeatures)    
admin.site.register(HotelCartItem)    
   
 