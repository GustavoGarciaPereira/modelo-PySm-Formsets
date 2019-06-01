from django.shortcuts import render
from django.db import transaction
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import Http404, JsonResponse
from django.contrib import messages


from .models import Cliente
from .forms import DependenteForm
from .forms import ClienteForm, DependenteFormSet



class ClienteListView(ListView):
    model = Cliente
    template_name = 'cliente/cliente_list.html'
    paginate_by = 50


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = 'cliente:list'

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['dependente_cliente'] = DependenteFormSet(self.request.POST)
        else:
            context['dependente_cliente'] = DependenteFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_dependente = context['dependente_cliente']

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.save()

            if formset_dependente.is_valid():
                formset_dependente.instance = self.object
                formset_dependente.save()


        return super(ClienteCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Não foi possível cadastrar Cliente (PF). Verifique os campos obrigatórios')
        return super(ClienteCreateView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, 'cadastrado com sucesso!!')
        return reverse(self.success_url)

class ClienteUpdateView(UpdateView):
    model = Cliente

    form_class = ClienteForm
    success_url = 'cliente:list'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        try:
            obj = Cliente.objects.get(slug=slug)
        except:
            raise Http404("Cliente não localizado")
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(ClienteUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['dependente_cliente'] = DependenteFormSet(self.request.POST, instance=self.object)
        else:
            context['dependente_cliente'] = DependenteFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_dependente = context['dependente_cliente']

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.save()

            if formset_dependente.is_valid():
                formset_dependente.instance = self.object
                formset_dependente.save()
        return super(ClienteUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Não foi possível alterar Cliente (PF). Verifique os campos obrigatórios')
        return super(ClienteUpdateView, self).form_invalid(form)  

    def get_success_url(self):
        messages.success(self.request, 'Cliente alterado com sucesso')
        return reverse(self.success_url)