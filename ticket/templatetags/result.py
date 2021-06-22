from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def chinese_weekday(value):
  translate = {
    "1":"一",
    "2":"二",
    "3":"三",
    "4":"四",
    "5":"五",
    "6":"六",
    "7":"日"
  }
  return translate[str(value)]
