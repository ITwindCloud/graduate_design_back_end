from django.contrib import admin
from .models import User,AoyouTicket,Airport,Advertisement
from django.db.models import F
# Register your models here.
import datetime
def date_display(obj):
    return obj.date.strftime("%Y-%m-%d")
def start_time_display(obj):
    return obj.start_time.strftime("%H:%M")
date_display.short_description = "起飞日期"
start_time_display.short_description = "起飞时间"

@admin.register(AoyouTicket)
class TicketAdmin(admin.ModelAdmin):
  date_hierarchy = 'date'
  # fields = ("id",("date","start_time","end_time"),("start_airport","end_airport"),("price","discount"))
  fieldsets = (
    # (None,{"fields":("id",)}),
    ("Time",{"fields":("date","start_time","end_time")}),
    ("Airport",{"fields":("start_airport","end_airport")}),
    ("Price",{"fields":("price","discount")}),
  )
  list_display = ["id",date_display,start_time_display,"start_airport","end_airport"]
  # list_editable = ["date",]
  list_filter = ["date","start_airport","end_airport"]
  list_select_related = ["start_airport","end_airport"]
  search_fields = ["date","start_airport__name","end_airport__name","move_two_days_back"]

  list_per_page = 40
  actions = ["move_one_day","move_two_days","move_one_day_back","move_two_days_back","move_three_days"]

  def move_one_day(self,request,queryset):
    AoyouTicket.objects.all().update(date=F("date") + datetime.timedelta(days=1))
  move_one_day.short_description = "全体前移一天"
  def move_two_days(self,request,queryset):
    AoyouTicket.objects.all().update(date=F("date") + datetime.timedelta(days=2))
  move_two_days.short_description = "全体前移两天"

  def move_three_days(self,request,queryset):
    AoyouTicket.objects.all().update(date=F("date") + datetime.timedelta(days=3))
  move_three_days.short_description = "全体前移三天"

  def move_one_day_back(self,request,queryset):
    AoyouTicket.objects.all().update(date=F("date") - datetime.timedelta(days=1))
  move_one_day_back.short_description = "全体后移一天"
  def move_two_days_back(self,request,queryset):
    AoyouTicket.objects.all().update(date=F("date") - datetime.timedelta(days=2))
  move_two_days_back.short_description = "全体后移两天"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ["id","tel","name","email","gender"]
  # fields = ["tel","name","email","gender","password","addr","user_tickets"]
  fieldsets = (("User Info",{"fields":("tel","name","email","gender","password","addr")}),("Orders",{"fields":("user_tickets","money")}))#("Orders",{"fields":("user_tickets",)})
  readonly_fields = ["tel","password"]
  raw_id_fields = ["user_tickets"]

# admin.site.register(User)

@admin.register(Airport)
class AirportAmdin(admin.ModelAdmin):
  list_display = ["flag","name","city","pinyin"]
  fields = ["flag","name","city","pinyin"]
  list_editable = ["name"]
  search_fields = ["name","city"]


  