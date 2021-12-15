from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OutputForm, SaveForm, AllUserInputForm
from .models import Sim as SimModel

def home(request, *args, **kwargs):
    initial = {field: 1 for field in AllUserInputForm.Meta.fields}  # if field not in ('daysEcmo_cat2', 'daysEcmo_cat3',
                                                                    #              'daysVent_cat1', 'daysVent_cat3')}
    initial['daysEcmo_cat2'] = 0
    initial['daysEcmo_cat3'] = 0
    initial['daysVent_cat1'] = 3
    initial['daysVent_cat3'] = 0
    allUserInputForm = AllUserInputForm(initial=initial)
    outputForm = OutputForm()
    saveForm = SaveForm()
    context = {
        "allUserInputForm": allUserInputForm,
        "outputForm": outputForm,
        "saveForm": saveForm,
        "dashboard": True
    }
    return render(request, "sim/dashboard.html", context)


class SimulationDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'sims'
    def get_queryset(self):
        return SimModel.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['allUserInputForm'] = AllUserInputForm(instance=self.get_object())
        context['outputForm'] = OutputForm(instance=self.get_object())
        context['saveForm'] = SaveForm()
        context['dashboard'] = True
        return context


class SimulationsListView(LoginRequiredMixin, ListView):
    context_object_name = 'sims'
    def get_queryset(self):
        return SimModel.objects.filter(author=self.request.user).order_by('-date_created')