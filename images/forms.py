from django import forms
from .models import Image
# Переопределение метода save() модельной формы
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests  # новое , устанавливаем бибилиотеку, для раб с изобр загрузки


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput, }

    # Проверяем что б ссылка была  с ['jpg', 'jpeg']
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('Указанный URL-адрес не соответствует допустимым расширениям изображений..')
        return url

    # Переопределение метода save() модельной формы
    def save(self, force_insert=False, force_update=False, commit=True):
        # создает объект image, вызвав метод save() с аргументом commit=False;
        image = super().save(commit=False) # super(ImageCreateForm, self).save(commit=False)
        # получает URL из атрибута cleaned_data формы;
        image_url = self.cleaned_data['url']
        # генерирует название изображения, совмещая слаг и расширение картинки;
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'   #'{}.{}'.format(slugify(image.title),image_url.rsplit('.', 1)[1].lower())
        # Скачиваем изображение по указанному адресу.
        # использует Python-пакет urllib, чтобы скачать файл картинки, и вызывает метод save() поля изображения, передавая в него объект скачанного
        # файла, ContentFile. Также используется аргумент commit=False, чтобы пока
        # не сохранять объект в базу данных;
        #response = request.urlopen(image_url)
        response = requests.get(image_url)
        image.image.save(image_name,ContentFile(response.content), save=False)  # ContentFile(response.content), save=False) #ContentFile(response.read()), save=False)
        #при переопределении метода важно оставить стандартное поведение,
        #поэтому сохраняем объект изображения в базу данных только в том случае, если commit равен True.
        if commit:
            image.save()
        return image