from django.core.management.base import CommandError,BaseCommand
from ticket.models import AoyouTicket
from django.db.models import Q
import pandas as pd
import datetime

class Command(BaseCommand):
  help = "Get transferring cases from Beijin to Shanghai"
  def handle(self,*args,**option):
    start = "北京"
    end = "上海"
    date = datetime.date(year=2021,month=5,day=20)
    tickets = AoyouTicket.objects.filter(Q(date=date) & (Q(start_airport__name__contains=start) | Q(end_airport__name__contains=end))).values(\
      "id","date","start_time","end_time","start_airport__city","end_airport__city","price")

    data = pd.DataFrame(tickets)
    data.to_csv("transferring_cases2.csv",index=False,encoding="utf-8")