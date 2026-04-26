from django import template

register = template.Library()


@register.filter
def format_price(value):
    """Formatea un precio con separadores de miles según locale es-CO."""
    try:
        number = float(value)
        return f"${number:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return value