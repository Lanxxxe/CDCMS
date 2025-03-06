from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def secure_image_url(enrollment, field_name):
    return reverse('serve_secure_image', kwargs={'enrollment_id': enrollment.id, 'image_field': field_name})