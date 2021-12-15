from rest_framework import serializers
from sim.models import Sim
from sim.modelFields import JSONSchemaField
import patientFlowSim.settings as settings
import json
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError


# class JSONSchemaField(serializers.JSONField):
# # Custom field that validates incoming data against JSONSchema,
# # Then, if successful, will store it as a string.
#
#     def __init__(self, schema, *args, **kwargs):
#         self.schema = kwargs.pop('schema', None)
#         super(JSONSchemaField, self).__init__(*args, **kwargs)
#
#
#     @property
#     def _schema_data(self):
#         # schema file related to model.py path
#         p = os.path.join(settings.BASE_DIR, self.schema)
#         with open(p, 'r') as file:
#             return json.loads(file.read())
#
#     def to_representation(self, obj):
#         return json.loads(obj)
#
#     def to_internal_value(self, data):
#         try:
#             validate(data, self._schema_data)
#         except JSONSchemaValidationError as e:
#             raise serializers.ValidationError(e.message)
#
#         return super(JSONSchemaField, self).to_internal_value(json.dumps(data))


class SimulationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sim
        fields = [
            'pk',
            'name',
            'author',
            'date_created',
            'description',
            'output',
            # inputs
            'requiredRes_cat1_ct', 'requiredRes_cat1_mri', 'requiredRes_cat1_ppe', 'requiredRes_cat1_propofol',
            'requiredRes_cat1_dexmedetomidine', 'requiredRes_cat1_fentanyl', 'requiredRes_cat1_morphine',
            'requiredRes_cat1_morphineOral', 'requiredRes_cat1_oxycodone', 'requiredRes_cat1_cisatricurium',
            'requiredRes_cat1_vecuronium',
            'requiredRes_cat2_ct', 'requiredRes_cat2_mri', 'requiredRes_cat2_ppe',
            'requiredRes_cat2_propofol', 'requiredRes_cat2_dexmedetomidine', 'requiredRes_cat2_fentanyl',
            'requiredRes_cat2_morphine', 'requiredRes_cat2_morphineOral', 'requiredRes_cat2_oxycodone',
            'requiredRes_cat2_cisatricurium', 'requiredRes_cat2_vecuronium',
            'requiredRes_cat3_ct', 'requiredRes_cat3_mri', 'requiredRes_cat3_ppe',
            'requiredRes_cat3_propofol', 'requiredRes_cat3_dexmedetomidine', 'requiredRes_cat3_fentanyl',
            'requiredRes_cat3_morphine', 'requiredRes_cat3_morphineOral', 'requiredRes_cat3_oxycodone',
            'requiredRes_cat3_cisatricurium', 'requiredRes_cat3_vecuronium',
            'simDays', 'narrivals_cat1', 'narrivals_cat2', 'narrivals_cat3', 'ninitials_cat1', 'ninitials_cat2',
            'ninitials_cat3', 'daysIcu_cat1', 'daysIcu_cat2', 'daysIcu_cat3', 'daysEcmo_cat1', 'daysEcmo_cat2',
            'daysEcmo_cat3', 'daysVent_cat1', 'daysVent_cat2', 'daysVent_cat3', 'daysDialysis_cat1',
            'daysDialysis_cat2', 'daysDialysis_cat3', 'nconsultations_cat1', 'nconsultations_cat2',
            'nconsultations_cat3'
        ]
        read_only_fields = ['author']

