from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Returns True if the user belongs to the given group, else False.
    """
    group_names = group_name.split(',')
    # return user.groups.filter(name=group_names).exists()
    return user.groups.filter(name__in=group_names).exists()