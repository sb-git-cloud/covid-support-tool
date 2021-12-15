from django import forms
from django.forms import ModelForm
from .models import Sim
import re


class SaveForm(ModelForm):
    class Meta:
        model = Sim
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea,
        }


class OutputForm(ModelForm):
    class Meta:
        model = Sim
        fields = ['output']
        widgets = {'output': forms.HiddenInput()}


class AllUserInputForm(ModelForm):
    class Meta:
        model = Sim
        fields = ['requiredRes_cat1_ct', 'requiredRes_cat1_mri', 'requiredRes_cat1_ppe', 'requiredRes_cat1_propofol',
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
                  'requiredRes_cat3_cisatricurium', 'requiredRes_cat3_vecuronium']
        widgets_res = {field: forms.NumberInput(attrs={"class": "form-control form-control-sm table my-0"})
                       for field in fields}
        fields.extend(['simDays', 'narrivals_cat1', 'narrivals_cat2', 'narrivals_cat3', 'ninitials_cat1', 'ninitials_cat2',
                  'ninitials_cat3', 'daysIcu_cat1', 'daysIcu_cat2', 'daysIcu_cat3', 'daysEcmo_cat1', 'daysEcmo_cat2',
                  'daysEcmo_cat3', 'daysVent_cat1', 'daysVent_cat2', 'daysVent_cat3', 'daysDialysis_cat1',
                  'daysDialysis_cat2', 'daysDialysis_cat3', 'nconsultations_cat1', 'nconsultations_cat2',
                  'nconsultations_cat3'])

        widgets_misc = {
            'nconsultations_cat1': forms.NumberInput(attrs={"class": "form-control form-control-sm table my-0"}),
            'nconsultations_cat2': forms.NumberInput(attrs={"class": "form-control form-control-sm table my-0"}),
            'nconsultations_cat3': forms.NumberInput(attrs={"class": "form-control form-control-sm table my-0"}),
            'daysEcmo_cat2': forms.HiddenInput(),
            'daysEcmo_cat3': forms.HiddenInput(),
            'daysVent_cat1': forms.HiddenInput(),
            'daysVent_cat3': forms.HiddenInput(),
            'simDays': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range",
                    "oninput": "simDaysSliderVal.value = id_simDays.value",
                    "max": 21,
                }
            ),
            'narrivals_cat1': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range",
                    "oninput": "id_output_narrivals_cat1.value = id_narrivals_cat1.value"
                }
            ),
            'narrivals_cat2': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range",
                    "oninput": "id_output_narrivals_cat2.value = id_narrivals_cat2.value"
                }
            ),
            'narrivals_cat3': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range",
                    "oninput": "id_output_narrivals_cat3.value = id_narrivals_cat3.value"
                }
            ),
            'ninitials_cat1': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range",
                    "oninput": "id_output_ninitials_cat1.value = id_ninitials_cat1.value"
                }
            ),
            'ninitials_cat2': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range",
                    "oninput": "id_output_ninitials_cat2.value = id_ninitials_cat2.value"
                }
            ),
            'ninitials_cat3': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range",
                    "oninput": "id_output_ninitials_cat3.value = id_ninitials_cat3.value"
                }
            ),
            'daysIcu_cat1': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range icu",
                    "oninput": "id_output_daysIcu_cat1.value = id_daysIcu_cat1.value"
                }
            ),
            'daysIcu_cat2': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range icu",
                    "oninput": "id_output_daysIcu_cat2.value = id_daysIcu_cat2.value"
                }
            ),
            'daysIcu_cat3': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range icu",
                    "oninput": "id_output_daysIcu_cat3.value = id_daysIcu_cat3.value"
                }
            ),
            'daysEcmo_cat1': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range ecmo",
                    "oninput": "id_output_daysEcmo_cat1.value = id_daysEcmo_cat1.value"
                }
            ),
            # 'daysEcmo_cat2': forms.NumberInput(
            #     attrs={
            #         "type": "range",
            #         "class": "custom-range",
            #         "oninput": "id_output_daysEcmo_cat2.value = id_daysEcmo_cat2.value"
            #     }
            # ),
            # 'daysEcmo_cat3': forms.NumberInput(
            #     attrs={
            #         "type": "range",
            #         "class": "custom-range",
            #         "oninput": "id_output_daysEcmo_cat3.value = id_daysEcmo_cat3.value"
            #     }
            # ),
            # 'daysVent_cat1': forms.NumberInput(
            #     attrs={
            #         "type": "range",
            #         "class": "custom-range",
            #         "oninput": "id_output_daysVent_cat1.value = id_daysVent_cat1.value"
            #     }
            # ),
            'daysVent_cat2': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range vent",
                    "oninput": "id_output_daysVent_cat2.value = id_daysVent_cat2.value"
                }
            ),
            # 'daysVent_cat3': forms.NumberInput(
            #     attrs={
            #         "type": "range",
            #         "class": "custom-range",
            #         "oninput": "id_output_daysVent_cat3.value = id_daysVent_cat3.value"
            #     }
            # ),
            'daysDialysis_cat1': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range dialysis",
                    "oninput": "id_output_daysDialysis_cat1.value = id_daysDialysis_cat1.value"
                }
            ),
            'daysDialysis_cat2': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range dialysis",
                    "oninput": "id_output_daysDialysis_cat2.value = id_daysDialysis_cat2.value"
                }
            ),
            'daysDialysis_cat3': forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "custom-range dialysis",
                    "oninput": "id_output_daysDialysis_cat3.value = id_daysDialysis_cat3.value"
                }
            )
        }
        widgets = {**widgets_res, **widgets_misc}