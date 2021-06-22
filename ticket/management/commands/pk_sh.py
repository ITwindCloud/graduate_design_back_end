from django.core.management.base import BaseCommand,CommandError
from ticket.models import AoyouTicket
import pandas as pd
import datetime

class Command(BaseCommand):
  help = "获取北京到上海的所有机票，并且保存到csv文件中"
  def handle(self,*args,**options):
    start = "北京"
    end = "上海"
    today = datetime.date.today()
    tickets = AoyouTicket.objects.filter(start_airport__name__contains=start,\
      end_airport__name__contains=end).values("date","start_airport__name","end_airport__name","price")

    df = pd.DataFrame(tickets,columns=["date","start_airport__name","end_airport__name","price"])
    df.to_csv("beijin-shanghai.csv",index=None,encoding="utf-8")