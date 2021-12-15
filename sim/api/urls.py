
from django.urls import path
from .views import PtFlowSimRudView, PtFlowSimAPIView, RunSimulationAPIView, ErlangPdfAPIView, CreateCsvAPIView,\
    SaveSimAPIView

urlpatterns = [
    path('<int:pk>', PtFlowSimRudView.as_view()),
    path('', PtFlowSimAPIView.as_view()),
    # path('', SaveSimAPIView.as_view()),
    path('runsim', RunSimulationAPIView.as_view()),
    path('erlangpdf', ErlangPdfAPIView.as_view()),
    path('outputToCsv', CreateCsvAPIView.as_view()),
]

