from django import template

register = template.Library()

@register.filter(name='millions')
def millions(number, decimals=2):
    """
    Convert an integer to its million representation and format it.
    """
    if number is not None:
        number = float(number)
        number /= 1_000_000
        return f"${number:,.{decimals}f}M"
    return "$0.00M"
