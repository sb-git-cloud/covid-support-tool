from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from sim.models import Sim
from .permissions import IsOwnerOrReadOnly
from .serializers import SimulationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .simulation import Simulation as RunSimulation
from .erlang import Erlang
from sim.forms import AllUserInputForm, OutputForm
import csv
import numpy as np
from django.http import HttpResponse
from datetime import date
from collections import ChainMap
from sim.api.simulation import Resources, Medication

class PtFlowSimRudView(generics.RetrieveUpdateDestroyAPIView):
    pass
    lookup_field = 'pk'
    serializer_class = SimulationSerializer
    permission_classes = [IsAuthenticated & (IsOwnerOrReadOnly | IsAdminUser)]
    queryset = Sim.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset

        author_queryset = self.queryset.filter(author=self.request.user)
        return author_queryset

class PtFlowSimAPIView(generics.CreateAPIView):
    pass
    lookup_field = 'pk'
    serializer_class = SimulationSerializer
    queryset = Sim.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RunSimulationAPIView(APIView):
    def get(self, request, *args, **kwargs):

        allUserInput = AllUserInputForm(request.GET)
        if allUserInput.is_valid():
            try:
                print('valid user data')
                allUserInputFormData = allUserInput.cleaned_data
                inputParams = {
                    'availableResources': {key.name: 0 for key in Resources},
                    'availableMedication': {key.name: 0 for key in Medication},
                    'simDays': allUserInputFormData['simDays'],
                    'meanDaysIcu': [allUserInputFormData['daysIcu_cat1'], allUserInputFormData['daysIcu_cat2'],
                                    allUserInputFormData['daysIcu_cat3']],
                    'meanDaysEcmo': [allUserInputFormData['daysEcmo_cat1'], allUserInputFormData['daysEcmo_cat2'],
                                     allUserInputFormData['daysEcmo_cat3']],
                    'meanDaysVent': [allUserInputFormData['daysVent_cat1'], allUserInputFormData['daysVent_cat2'],
                                     allUserInputFormData['daysVent_cat3']],
                    'meanDaysDialysis': [allUserInputFormData['daysDialysis_cat1'],
                                         allUserInputFormData['daysDialysis_cat2'],
                                         allUserInputFormData['daysDialysis_cat3']],
                    'narrivals': [allUserInputFormData['narrivals_cat1'], allUserInputFormData['narrivals_cat2'],
                                  allUserInputFormData['narrivals_cat3']],
                    'ninitials': [allUserInputFormData['ninitials_cat1'], allUserInputFormData['ninitials_cat2'],
                                  allUserInputFormData['ninitials_cat3']],
                    'ecmo': {
                        "resourcesRequired": {
                            Resources.CT.name: allUserInputFormData['requiredRes_cat1_ct'],
                            Resources.MRI.name: allUserInputFormData['requiredRes_cat1_mri'],
                            Resources.PPE.name: allUserInputFormData['requiredRes_cat1_ppe']
                        },
                        "medicationRequired": {
                            Medication.PROPOFOL.name: allUserInputFormData['requiredRes_cat1_propofol'],
                            Medication.DEXMEDETOMIDINE.name: allUserInputFormData[
                                'requiredRes_cat1_dexmedetomidine'],
                            Medication.FENTANYL.name: allUserInputFormData['requiredRes_cat1_fentanyl'],
                            Medication.MORPHINE.name: allUserInputFormData['requiredRes_cat1_morphine'],
                            Medication.MORPHINE_ORAL.name: allUserInputFormData[
                                'requiredRes_cat1_morphineOral'],
                            Medication.OXYCODONE.name: allUserInputFormData['requiredRes_cat1_oxycodone'],
                            Medication.CISATRICURIUM.name: allUserInputFormData[
                                'requiredRes_cat1_cisatricurium'],
                            Medication.VECURONIUM.name: allUserInputFormData[
                                'requiredRes_cat1_vecuronium']
                        },
                        "consultationsRequired": allUserInputFormData['nconsultations_cat1']},

                    'ventilated': {
                        "resourcesRequired": {
                            Resources.CT.name: allUserInputFormData['requiredRes_cat2_ct'],
                            Resources.MRI.name: allUserInputFormData['requiredRes_cat2_mri'],
                            Resources.PPE.name: allUserInputFormData['requiredRes_cat2_ppe']
                        },
                        "medicationRequired": {
                            Medication.PROPOFOL.name: allUserInputFormData['requiredRes_cat2_propofol'],
                            Medication.DEXMEDETOMIDINE.name: allUserInputFormData[
                                'requiredRes_cat2_dexmedetomidine'],
                            Medication.FENTANYL.name: allUserInputFormData['requiredRes_cat2_fentanyl'],
                            Medication.MORPHINE.name: allUserInputFormData['requiredRes_cat2_morphine'],
                            Medication.MORPHINE_ORAL.name: allUserInputFormData[
                                'requiredRes_cat2_morphineOral'],
                            Medication.OXYCODONE.name: allUserInputFormData['requiredRes_cat2_oxycodone'],
                            Medication.CISATRICURIUM.name: allUserInputFormData[
                                'requiredRes_cat2_cisatricurium'],
                            Medication.VECURONIUM.name: allUserInputFormData[
                                'requiredRes_cat2_vecuronium']
                        },
                        "consultationsRequired": allUserInputFormData['nconsultations_cat2']},

                    'bed': {
                        "resourcesRequired": {
                            Resources.CT.name: allUserInputFormData['requiredRes_cat3_ct'],
                            Resources.MRI.name: allUserInputFormData['requiredRes_cat3_mri'],
                            Resources.PPE.name: allUserInputFormData['requiredRes_cat3_ppe']
                        },
                        "medicationRequired": {
                            Medication.PROPOFOL.name: allUserInputFormData['requiredRes_cat3_propofol'],
                            Medication.DEXMEDETOMIDINE.name: allUserInputFormData[
                                'requiredRes_cat3_dexmedetomidine'],
                            Medication.FENTANYL.name: allUserInputFormData['requiredRes_cat3_fentanyl'],
                            Medication.MORPHINE.name: allUserInputFormData['requiredRes_cat3_morphine'],
                            Medication.MORPHINE_ORAL.name: allUserInputFormData[
                                'requiredRes_cat3_morphineOral'],
                            Medication.OXYCODONE.name: allUserInputFormData['requiredRes_cat3_oxycodone'],
                            Medication.CISATRICURIUM.name: allUserInputFormData[
                                'requiredRes_cat3_cisatricurium'],
                            Medication.VECURONIUM.name: allUserInputFormData[
                                'requiredRes_cat3_vecuronium']
                        },
                        "consultationsRequired": allUserInputFormData['nconsultations_cat3']},
                }
                sim = RunSimulation(inputParams)
                result = sim.run_sim()
                response = Response(result, status=status.HTTP_200_OK)
            except:
                response = Response('Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response = Response('Error: incompatible input parameters.', status=status.HTTP_400_BAD_REQUEST)

        return response

class ErlangPdfAPIView(APIView):
    def get(self, request, *args, **kwargs):

        inputForm = AllUserInputForm(request.GET)
        if inputForm.is_valid():

            try:
                mean = inputForm.cleaned_data
                # print(mean)
                mean = {value: value for key, value in mean.items() if 'days' in key}
                # print(mean)
                x = np.linspace(0, 50, 101)
                pdf = {}
                for k, v in mean.items():
                    erlang = Erlang(v, x)
                    pdf[k] = erlang.get_pdf()
                data = {
                    "Days": x,
                    "pdf": pdf
                }
                return Response(data, status=status.HTTP_200_OK)
            except:
                response = Response('Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # print('eror l170')
            return Response('Error: incompatible input parameters.', status=status.HTTP_400_BAD_REQUEST)

class CreateCsvAPIView(APIView):
    def get(self, request, *args, **kwargs):
        output = OutputForm(request.GET)
        if output.is_valid():
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="' + date.today().strftime("%Y_%m_%d") + '_resources.csv"'
            outputData = output.cleaned_data['output']
            writer = csv.writer(response)
            header = []
            subheader = []
            body = {}
            for k in outputData:
                try:
                    subheader.extend(outputData[k].keys())
                    header.append(k)
                    header.extend([''] * (len(outputData[k]) - 1))
                    body = {**body, **outputData[k]}
                except AttributeError:
                    header.append('')
                    subheader.append(k)
                    body = {**body, **{k: outputData[k]}}

            writer.writerow(tuple(header))
            writer.writerow(tuple(subheader))
            writer.writerows(zip(*body.values()))
            return response
        else:
            response = Response('Error: incompatible input parameters.', status=status.HTTP_400_BAD_REQUEST)

        return response

class SaveSimAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        sim = Sim(request.POST)
        if sim.is_valid():
            print('isvalid')
        else:
            print('notvalid')

    def get(self, request, *args, **kwargs):
        print(request.POST)
        if request.method == 'POST':
            sim = Sim(request.POST)
            if sim.is_valid():
                print('isvalid')
                # response = HttpResponse(content_type='text/csv')
                # response['Content-Disposition'] = 'attachment; filename="' + date.today().strftime("%Y_%m_%d") + '_resources.csv"'
                # outputData = sim.cleaned_data['output']
                # # outputData = dict(ChainMap(*outputData))
                # writer = csv.writer(response)
                # writer.writerow(outputData.keys())
                # writer.writerows(zip(*outputData.values()))
                # return response
            else:
                response = Response('Error: incompatible input parameters.', status=status.HTTP_400_BAD_REQUEST)

            return response
