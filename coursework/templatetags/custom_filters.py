import os
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    # Check if the first argument is a dictionary
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    else:
        # Handle the case where the input is not a dictionary
        return f"Expected a dictionary, got {type(dictionary).__name__}"


@register.filter
def basename(value):
    return os.path.basename(value.name)


@register.filter(name='get_grade')
def get_grade(value, arg):
    """Retrieve value from the dictionary using a variable key."""
    return value.get(arg, 'No grade')

@register.filter(name='calculate_status')
def calculate_status(assignment):
    if assignment.not_available:
        return 'not_available'
    elif assignment.is_late:
        return 'late'
    elif assignment.submitted:
        return 'completed'
    else:
        return 'not_completed'
