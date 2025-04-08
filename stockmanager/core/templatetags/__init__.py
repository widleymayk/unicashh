from django.template import Library
from .form_filters import addclass

register = Library()
register.filter('addclass', addclass)