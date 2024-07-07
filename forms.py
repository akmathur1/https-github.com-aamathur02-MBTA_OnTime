from django import forms
from .models import TripInput,Starting_Stop, Ending_Stop

class TripInputForm(forms.ModelForm):
    class Meta:
        model = TripInput
        fields = {'name', 'line', 'starting_stop', 'ending_stop', 'starting_time', 'ending_time'}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['starting_stop'].queryset = Starting_Stop.objects.none()
        self.fields['ending_stop'].queryset  = Ending_Stop.objects.none()

        if 'line' in self.data:
            try:
                line_id = int(self.data.get('line'))
                self.fields['starting_stop'].queryset = Starting_Stop.objects.filter(line_id=line_id).order_by('name')
                self.fields['ending_stop'].queryset = Ending_Stop.objects.filter(line_id=line_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['starting_stop'].queryset = self.instance.line.starting_stop_set.order_by('name')
            self.fields['ending_stop'].queryset = self.instance.line.ending_stop_set.order_by('name')
