from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def diferencia_fecha(fecha_inicio, fecha_fin):
    if fecha_inicio and fecha_fin:
        # Calculamos la diferencia entre las fechas
        diferencia = fecha_fin - fecha_inicio

        # Extraemos las horas, minutos y segundos
        horas = diferencia.days * 24 + diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        # Devuelves la diferencia en horas, minutos y segundos
        return f'{horas}H\t{minutos}m'
    return None
