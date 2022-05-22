from tkinter import Widget
from django import forms

class CustomModelMultipleChoiceField(forms.widgets.SelectMultiple):
    class Media:
        css = {}
        js = ('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/js/select2.min.js')

    def __init__(self, attrs=None,*args, **kwargs) -> None:

        attrs = attrs or {}

        default_options = {}

        super().__init__(attrs)


        
class Select2Mixin():
    def fix_class(self, attrs):
                class_name = attrs.pop('class', '')
                if class_name: 
                    attrs['class'] = '{} {}'.format(
                        class_name, 'custom-select2-widget'
                    )
                else: 
                    attrs['class'] = 'custom-select2-widget'
    