from django.contrib import admin
from . import models
# Register your models here.

class MemberInstanceInline(admin.TabularInline):
    model = models.Member
    extra=3
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','team', 'gander', 'type')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league','usern', 'Affiliation', 'City','country','Status')
    list_filter = ('league','Status',)
    inlines= [MemberInstanceInline]

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name','chair','category')
    list_filter = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','price',)

class ChairAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname','email', 'phone')

class MembertypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category','price')

class TCAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','league')
    list_filter = ('league',)

class OrganiserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)

class ChampionsAdmin(admin.ModelAdmin):
    list_display = ('title',)

class CertificateAdmin(admin.ModelAdmin):
    list_display = ('championsTitle','league','team',)

admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.League, LeagueAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Chair, ChairAdmin)
admin.site.register(models.Membertype, MembertypeAdmin)
admin.site.register(models.TC,TCAdmin)
admin.site.register(models.Organiser,OrganiserAdmin)
admin.site.register(models.Champions,ChampionsAdmin)
admin.site.register(models.Certificate,CertificateAdmin)
