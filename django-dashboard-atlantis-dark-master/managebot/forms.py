from django.forms import ModelForm
from .models import Custom_Command


class CustomCommandForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['command'].widget.attrs.update({'class': 'form-control'})
        self.fields['response'].widget.attrs.update({'class': 'form-control',"size":45,"rows":3})
    class Meta:
        model = Custom_Command
        fields = [
            "command",
            "response",
            "dm_response",
        ]
