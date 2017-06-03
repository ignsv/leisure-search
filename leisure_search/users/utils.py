from model_utils.choices import Choices

PASSWORD_FIELD_ERRORS = {
    'min_length': 'Password must contain at least 8 characters'
}

LIKE_RATING_CHOICES = Choices(
    (0, 'ZERO', 'Zero',),
    (1, 'ONE', 'One',),
    (2, 'TWO', 'two',),
    (3, 'THREE', 'three',),
    (4, 'FOUR', 'four',),
    (5, 'Five', 'five',),
)
