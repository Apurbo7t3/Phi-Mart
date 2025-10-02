from django.core.exceptions import ValidationError

def validate_file(file):
    max_size=2
    max_size_in_bytes=max_size * 1024 *1024

    if file.size>max_size_in_bytes:
        raise ValidationError(f'Your file size can not be bigger than {max_size} MB!')