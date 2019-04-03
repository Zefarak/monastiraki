from django.urls import reverse
from django.utils.html import format_html

def admin_change_url(obj):
    app_label = obj._meta.app_label
    model_name = obj._meta.model_name.lower()
    return reverse(f'admin:{app_label}_{model_name}_change', args=(obj.pk,))


def admin_link(attr, short_description, empty_description="-"):
    "Decorator"
    
    def wrap(func):
        def field_func(self, obj):
            related_obj = getattr(obj, attr)
            if related_obj is None:
                return empty_description
            url = admin_change_url(related_obj)
            return format_html(
                '<a href="{}">{}</a>',
                url,
                func(self, related_obj)
            )
        field_func.short_description = short_description
        field_func.allow_tags = True
        return field_func
    return wrap
