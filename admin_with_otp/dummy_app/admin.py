from django.contrib import admin
from custom_admin.sites import admin_site
from dummy_app.models import Article, Reporter




class ArticleAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'pub_date',)
    fields = ('reporter', 'headline', 'pub_date',)
    search_fields = ('reporter',)
    ordering = ('pub_date',)
    
    
# admin.site.register(Article, ArticleAdmin)
admin_site.register(Article, ArticleAdmin) #! custom admin instance



class ReporterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    fields = ('first_name', 'last_name', 'email',)
    search_fields = ('first_name', 'last_name', 'email',)
    ordering = ('last_name',)
    
    
# admin.site.register(Reporter, ReporterAdmin)
admin_site.register(Reporter, ReporterAdmin) #! custom admin instance




# ! Register any third-party model such as celery models, ...
# ? EXAMLE: admin_site.register(TaskResult)
# ? EXAMLE:  admin_site.register(PeriodicTasks)
# ? EXAMLE:  admin_site.register(PeriodicTask)