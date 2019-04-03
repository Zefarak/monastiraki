from django.core.exceptions import ValidationError


def validate_size(value):
    if value.file.size > 0.4*1024*1024:
        raise ValidationError('This file is bigger than 0.7mb!')


def upload_location(instance, filename):
    return 'first_page/%s/%s' % (instance.title, filename)


def upload_banner(instance, filename):
    return 'banner/%s/%s' % (instance.title, filename)


def validate_positive_decimal(value):
    if value < 0:
        return ValidationError('This number is negative!')
    return value


def category_site_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'category_site/{0}/{1}'.format(instance.name, filename)
