from django.contrib import admin

from learning.models import Author, Course, Lesson, Video, Audio

# Register your models here.
admin.site.register(Author, admin.ModelAdmin)
admin.site.register(Course, admin.ModelAdmin)
admin.site.register(Lesson, admin.ModelAdmin)
admin.site.register(Video, admin.ModelAdmin)
admin.site.register(Audio, admin.ModelAdmin)
