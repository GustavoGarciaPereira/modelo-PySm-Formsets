
from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import Cliente, Dependente
from .models import Cliente 

# class ClienteListForm(forms.Form):
#     SITUACOES = (
#         ('TODOS', 'Todos'),
#         ('ATIVOS', 'Somente ativos'),
#         ('INATIVOS', 'Somente inativos')
#     )

#     TIPOS = (
#         ('TODAS', 'Todas'),
#         ('PJ', 'Pessoa Jurídica'),
#         ('PF', 'Pessoa Física')
#     )

#     palavra_chave = forms.CharField(label='Pesquisar', widget=forms.TextInput(
#         attrs={'class': 'form-control ', 'placeholder': 'Pesquisar'}), required=False)
#     tipo = forms.ChoiceField(label='Tipo ', choices=TIPOS, initial='TODAS', required=False)
#     situacao = forms.ChoiceField(label='Situação ', choices=SITUACOES, initial='ATIVOS', required=False)

#     def __init__(self, empresa, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['categoria'] = forms.ModelChoiceField(CategoriaCliente.objects.filter(empresa=empresa),
#                                                           empty_label="", required=False)


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ()


class DependenteForm(forms.ModelForm):
    class Meta:
        model = Dependente
        exclude = ()

    tel_fixo = forms.CharField(label="Telefone Fixo", widget=forms.TextInput(
            attrs={'class': 'form-control mask_tel_fixo'}), max_length=13, required=False)

    tel_celular = forms.CharField(label="Telefone Celular", widget=forms.TextInput(
            attrs={'class': 'form-control mask_tel_celular'}), max_length=13, required=False)

    ramal = forms.IntegerField(label='Ramal', required=False)



DependenteFormSet = inlineformset_factory(Cliente, Dependente,
                                              fields=('descricao', 'tel_fixo', 'ramal', 'tel_celular', 'email',),
                                              form=DependenteForm, extra=1)
