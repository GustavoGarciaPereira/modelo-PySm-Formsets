
from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import Cliente, Dependente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ('slug',)


class DependenteForm(forms.ModelForm):
    class Meta:
        model = Dependente
        exclude = ()

    tel_celular = forms.CharField(label="Telefone Celular", widget=forms.TextInput(
            attrs={'class': 'form-control mask_tel_celular'}), max_length=13, required=False)


DependenteFormSet = inlineformset_factory(Cliente, Dependente,
                                              fields=('nome','tel_celular','email'),
                                              form=DependenteForm, extra=1)
