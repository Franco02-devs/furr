from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def diferencia_fecha(fecha_inicio, fecha_fin):
    if fecha_inicio and fecha_fin:
        diferencia = fecha_fin - fecha_inicio
        horas = diferencia.days * 24 + diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        return f'{horas}H\t{minutos}m'
    return None

@register.filter
def float_to_hms(hours_float):
    hours = int(hours_float)
    minutes = int((hours_float - hours) * 60)
    seconds = int((((hours_float - hours) * 60) - minutes) * 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"
