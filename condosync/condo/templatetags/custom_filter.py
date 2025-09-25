from django import template

register = template.Library()

def sortSectionByDayOfWeek(sections):
    for section in sections:
        section.day_of_week_num = section.dayOfWeek()
    return sections

def formatPhoneNumber(value):
    if len(value) <= 10:
        number = f"{value[:3]}-{value[3:6]}-{value[6:]}"
    else:
        number = value
    return number

register.filter("sortSectionByDayOfWeek", sortSectionByDayOfWeek)
register.filter("formatPhoneNumber", formatPhoneNumber)
