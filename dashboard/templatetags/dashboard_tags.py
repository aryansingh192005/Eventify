from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Returns dictionary[key] if it exists.
    """

    if dictionary is None:
        return []

    return dictionary.get(key, [])