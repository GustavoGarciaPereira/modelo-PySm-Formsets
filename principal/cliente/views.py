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
from .forms import ClienteForm



# Create your views here.
class ClienteListView(ListView):
    model = Cliente
    template_name = 'cliente/cliente_list.html'
    paginate_by = 50

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     empresa = self.request.session['empresa']
    #     if self.request.GET:
    #         context['form'] = ClienteListForm(empresa=empresa, data=self.request.GET)
    #     else:
    #         context['form'] = ClienteListForm(empresa=empresa)
    #     qs = self.get_queryset()
    #     paginator = Paginator(qs, self.paginate_by)
    #     page = self.request.GET.get('page')
    #     params = self.request.GET.copy()
    #     if 'page' in params:
    #         del (params['page'])
    #     get_params = params.urlencode()
    #     try:
    #         qs = paginator.page(page)
    #     except PageNotAnInteger:
    #         qs = paginator.page(1)
    #     except EmptyPage:
    #         qs = paginator.page(paginator.num_pages)
    #     context['object_list'] = qs
    #     context['get_params'] = get_params
    #     return context

    # def get_queryset(self):
    #     empresa = self.request.session['empresa']
    #     if self.request.GET:
    #         form = ClienteListForm(empresa=empresa, data=self.request.GET)
    #         qs = super(ClienteListView, self).get_queryset().filter(empresa=empresa)
    #     else:
    #         form = ClienteListForm(empresa=empresa)
    #         qs = super(ClienteListView, self).get_queryset().filter(empresa=empresa, is_active=True)

    #     if form.is_valid():
    #         palavra_chave = form.cleaned_data['palavra_chave']
    #         tipo = form.cleaned_data['tipo']
    #         situacao = form.cleaned_data['situacao']
    #         categoria = form.cleaned_data['categoria']

    #         palavra_chave_ls = palavra_chave.split(' ')
    #         for palavra_chave in palavra_chave_ls:
    #             if len(palavra_chave) > 3:
    #                 qs = qs.filter(nome__icontains=palavra_chave)

    #         if situacao == 'ATIVOS':
    #             qs = qs.filter(is_active=True)

    #         elif situacao == 'INATIVOS':
    #             qs = qs.filter(is_active=False)

    #         if tipo != 'TODAS':
    #             qs = qs.filter(tipo=tipo)

    #         if categoria:
    #             qs = qs.filter(categorias=categoria)

    #     return qs


class ClienteCreateView(CreateView):
    model = Cliente
    #template_name = 'cliente/cliente_form.html'
    form_class = ClienteForm
    #success_url = 'cliente:list'

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['contatos_cliente'] = DependenteForm(self.request.POST)
        else:
            context['contatos_cliente'] = DependenteForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_contatos = context['contatos_cliente']

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.save()

            if formset_contatos.is_valid():
                formset_contatos.instance = self.object
                formset_contatos.save()


        return super(ClienteCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Não foi possível cadastrar Cliente (PF). Verifique os campos obrigatórios')
        return super(ClienteCreateView, self).form_invalid(form)

    # def get_form(self):
    #     form_class = self.get_form_class()
    #     return form_class(empresa=self.request.session['empresa'], **self.get_form_kwargs())

    # def get_success_url(self):
    #     messages.success(self.request, 'Cliente (PF) Criado com sucesso')
    #     return redirecionar(self, list_url='cliente:list', create_url='cliente:pf_create',
    #                         update_url='cliente:pf_update')