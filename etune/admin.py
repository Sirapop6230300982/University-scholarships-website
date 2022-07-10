from django.contrib import admin
from etune.models import *

# Register your models here
#.
class DesignScholar_info(admin.ModelAdmin):
    list_display = ["si_name","id"]



admin.site.register(File_Models)
admin.site.register(Scholar_news)
admin.site.register(Scholar_info,DesignScholar_info)
admin.site.register(Scholar_weight_score)
admin.site.register(add_commit)
admin.site.register(Scholar_profile)
admin.site.register(add_scholar_Commit)
admin.site.register(Scholar_app)
admin.site.register(avatar_profile)
admin.site.register(Log_score)