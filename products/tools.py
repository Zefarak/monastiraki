import os
from django.core.validators import ValidationError


def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    title = instance.title
    return 'product/{0}/{1}'.format(instance.product.id, filename)



def upload_location(instance, filename):
    return "%s%s" %(instance.id, filename)


def my_awesome_upload_function(instance, filename):
    """ this function has to return the location to upload the file """
    return os.path.join('/media_cdn/%s/' % instance.id, filename)


def check_size(value):
    if value.file.size > 1024*1024/2:
        return ValidationError('File is bigger than 0.5mb')