
from django.urls import path
from .views import SimulationDetailView, SimulationsListView

urlpatterns = [
    # path('<int:pk>', PtFlowSimRudView.as_view()),
    path('', SimulationsListView.as_view(template_name='sim/sims_list.html'), name='sims'),
    path('<int:pk>', SimulationDetailView.as_view(template_name='sim/dashboard.html'), name='sims'),
]

