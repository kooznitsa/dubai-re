from django.forms import ModelForm
from django import forms

from .models import Project


all_fields = ['highlights', 'building', 'district', 'neighborhood', \
        'price', 'surface', 'beds', 'baths', 'amenities', 'url']
tag_fields = ['cheap', 'condition', 'discounted', 'distressed', \
        'furnished', 'investment', 'luxury', 'metro', 'tenanted', \
        'upgraded', 'vacant', 'views']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = all_fields + tag_fields

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['highlights'].required = True

        for name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': name.capitalize()})

        def create_checkbox(self, field_name):
            self.fields[field_name] = forms.ChoiceField(
                widget=forms.RadioSelect,
                choices=(
                    (1, field_name),
                ),
                label = '',
                required=False,
            )

            self.fields[field_name].widget.attrs.update(
                {'type': 'checkbox'})

        for i in tag_fields:
            create_checkbox(self, i)

        for i in all_fields:
            self.fields[i].label = False
            self.fields['cheap'].label = 'SELECT TAGS:'