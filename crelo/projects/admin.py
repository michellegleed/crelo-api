from django.contrib import admin

# Register your models here.
from .models import Project
from .models import Pledge
from .models import ProgressUpdate
from .models import ProjectCategory
from .models import Pledgetype
# from .models import Badge
from .models import Location
from .models import Activity

    
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['email', 'username', 'is_admin', 'location']

admin.site.register(Project)
admin.site.register(Pledge)
admin.site.register(ProgressUpdate)
admin.site.register(ProjectCategory)
admin.site.register(Pledgetype)
# admin.site.register(Badge)
admin.site.register(Location)
admin.site.register(Activity)