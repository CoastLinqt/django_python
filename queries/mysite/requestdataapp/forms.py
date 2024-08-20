from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForms(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label="Your age", min_value=1, max_value=120)
    bio = forms.CharField(label="Biography", widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile):
    if file.name and "virus" in file.name:
        raise ValidationError("file name should not contain")


def validate_size_name(file: InMemoryUploadedFile):
    limit = 2 * 1024 * 1024
    file_size = file.size
    if file_size > limit:
        raise ValidationError("file size more than 1 Mb")


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name, validate_size_name])