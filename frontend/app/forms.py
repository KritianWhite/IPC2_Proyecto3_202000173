from django import forms


class FileForm(forms.Form):
    file = forms.FileField(label='file')


class DateForm(forms.Form):
    date = forms.DateField(label='Fecha')
    empresa = forms.DateField(label='empresa')

class DateForm2(forms.Form):
    date1 = forms.DateField(label='Fecha1')
    date2 = forms.DateField(label='Fecha2')
    empresa = forms.DateField(label='empresa')
