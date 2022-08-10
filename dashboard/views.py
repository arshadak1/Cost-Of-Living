from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from dashboard.forms import DataForm, ReviewForm
from .models import Data, Review
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
import json

from .views_helper import _updateProfile, _graph_data,  humanReadableNumber


@login_required(login_url='/login')
def dashboard(request):
    # fetch the details required for graph to plot
    dashboard_context = _graph_data(request)
    return render(request, "dashboard/dashboard.html", dashboard_context)


@login_required(login_url='/login')
def profile(request):

    # current logged in user
    curr_user = request.user

    # data required for JS to populate the fields in th profile section
    datas_for_js = json.dumps({'username': str(curr_user), 'email': str(curr_user.email),
                               'firstname': str(curr_user.first_name), 'lastname': str(curr_user.last_name)})

    # 'form_message' & 'form_msg_class' => the message and class to be used after form submission.if false err msg else success msg
    profile_context = {'username': curr_user, 'email': curr_user.email,
                       'firstname': curr_user.first_name, 'lastname': curr_user.last_name,
                       'emailError': False, 'usernameError': False, 'passSameErr': False, 'passValidErr': '',
                       'emailMsg': '', 'data_inputs': datas_for_js,
                       'form_message': '', 'form_msg_class': 'form-msg hidden'}

    # when the user submits a form we have to update the backend too
    if request.method == 'POST':
        profile_context = _updateProfile(
            request, profile_context, curr_user)  # function that fetch detils for profile form to populate  the form
        return render(request, "dashboard/profile.html", profile_context)

    return render(request, "dashboard/profile.html", profile_context)


@login_required(login_url='/login')
def graphs(request):
    graph_context = _graph_data(request)
    return render(request, "dashboard/graphs.html", graph_context)


@login_required(login_url='/login')
def review(request):

    form = ReviewForm(request.POST or None)
    review_context = {'form':None, 'submitted_once':False}
    
    if form.is_valid():
        form.instance.user = request.user
        form.instance.review_rate = int(request.POST.get('rating-value'))
        form.save()
        form = ReviewForm()
        review_context['submitted_once'] = True
        return render(request, 'dashboard/review.html', review_context)
    review_context['form'] = form
    return render(request, "dashboard/review.html", review_context)


class DataListView(LoginRequiredMixin, ListView):
    model = Data
    template_name = "dashboard/data_list.html"
    context_object_name = 'datas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datas'] = context['datas'].filter(
            user=self.request.user)
        for data in context['datas']:
            if data.per == 'month':
                data.per = 'mo.'
            elif data.per == 'year':
                data.per = 'yr.'
            elif data.per == 'day':
                data.per = 'dy.'
            elif data.per == 'week':
                data.per = 'wk.'

            if data.is_expense == 'Income':
                data.is_expense = False
            else:
                data.is_expense = True

            data.value = humanReadableNumber(data.value)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['datas'] = context['datas'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        context['datas'] = context['datas'][::-1]
        return context


class DataCreateView(LoginRequiredMixin, CreateView):
    model = Data
    form_class = DataForm
    template_name = "dashboard/data_form.html"
    success_url = reverse_lazy('data-create')

    def form_valid(self, form):
        form.instance.user = self.request.user

        if self.request.POST.get('save-form') == 'Save':
            self.success_url = reverse_lazy('data')

        return super().form_valid(form)


class DataUpdateView(LoginRequiredMixin, UpdateView):
    model = Data
    form_class = DataForm
    template_name = "dashboard/data_form.html"
    success_url = reverse_lazy('data-create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isUpdate'] = True
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        if self.request.POST.get('save-form') == 'Save':
            self.success_url = reverse_lazy('data')

        return super().form_valid(form)


class DataDeleteView(LoginRequiredMixin, DeleteView):
    model = Data
    context_object_name = 'data'
    template_name = "dashboard/data_confirm_delete.html"
    success_url = reverse_lazy('data')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class DataDetailView(LoginRequiredMixin, DetailView):
    model = Data
    template_name = "dashboard/data_detail.html"
    context_object_name = 'data'
