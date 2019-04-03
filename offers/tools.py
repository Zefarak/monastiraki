from django.core.exceptions import ValidationError

MAX_SIZE_FILE = 1024*1024/2


def upload_location(instance, filename):
    try:
        return f'offers/{instance.title}/{filename}'
    except:
        return f'offers/{instance.id}/{filename}'


def check_size(value):
    if value.file.size > MAX_SIZE_FILE:
        return ValidationError('This file is bigger then 0.5 mb')