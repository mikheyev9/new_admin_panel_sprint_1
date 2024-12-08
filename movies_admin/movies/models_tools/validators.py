from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


RATING_VALIDATORS = [
    MinValueValidator(0, _("Rating cannot be less than 0.")),
    MaxValueValidator(100, _("Rating cannot be greater than 100.")),
]