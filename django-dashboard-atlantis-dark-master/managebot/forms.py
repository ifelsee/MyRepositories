from django.forms import ModelForm
from .models import Custom_Command


class CustomCommandForm(ModelForm):

    class Meta:
        model = Custom_Command
        fields = [
            "command",
            "response",
        ]
