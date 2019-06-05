from django import forms


class SettimanaForm(forms.Form):
	gruppo_lunedi = forms.ChoiceField()
	gruppo_martedi = forms.ChoiceField()
	gruppo_mercoledi = forms.ChoiceField()
	gruppo_giovedi = forms.ChoiceField()
	gruppo_venerdi = forms.ChoiceField()
