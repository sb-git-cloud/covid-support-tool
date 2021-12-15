from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from .modelFields import JSONSchemaField
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Sim(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200)
    output = JSONSchemaField(schema='static/schemas/outputSchema.json', default=dict, blank=True)
    simDays = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(21)])

    # (#) of consultations per patient per day
    nconsultations_cat1 = models.PositiveSmallIntegerField()
    nconsultations_cat2 = models.PositiveSmallIntegerField()
    nconsultations_cat3 = models.PositiveSmallIntegerField()

    # (#) of arriving patients
    narrivals_cat1 = models.PositiveSmallIntegerField()
    narrivals_cat2 = models.PositiveSmallIntegerField()
    narrivals_cat3 = models.PositiveSmallIntegerField()

    # (#) of initial patients
    ninitials_cat1 = models.PositiveSmallIntegerField()
    ninitials_cat2 = models.PositiveSmallIntegerField()
    ninitials_cat3 = models.PositiveSmallIntegerField()

    # Required Resources by category
    requiredRes_cat1_ct = models.PositiveSmallIntegerField()
    requiredRes_cat1_mri = models.PositiveSmallIntegerField()
    requiredRes_cat1_ppe = models.PositiveSmallIntegerField()
    requiredRes_cat1_propofol = models.PositiveSmallIntegerField()
    requiredRes_cat1_dexmedetomidine = models.PositiveSmallIntegerField()
    requiredRes_cat1_fentanyl = models.PositiveSmallIntegerField()
    requiredRes_cat1_morphine = models.PositiveSmallIntegerField()
    requiredRes_cat1_morphineOral = models.PositiveSmallIntegerField()
    requiredRes_cat1_oxycodone = models.PositiveSmallIntegerField()
    requiredRes_cat1_cisatricurium = models.PositiveSmallIntegerField()
    requiredRes_cat1_vecuronium = models.PositiveSmallIntegerField()

    requiredRes_cat2_ct = models.PositiveSmallIntegerField()
    requiredRes_cat2_mri = models.PositiveSmallIntegerField()
    requiredRes_cat2_ppe = models.PositiveSmallIntegerField()
    requiredRes_cat2_propofol = models.PositiveSmallIntegerField()
    requiredRes_cat2_dexmedetomidine = models.PositiveSmallIntegerField()
    requiredRes_cat2_fentanyl = models.PositiveSmallIntegerField()
    requiredRes_cat2_morphine = models.PositiveSmallIntegerField()
    requiredRes_cat2_morphineOral = models.PositiveSmallIntegerField()
    requiredRes_cat2_oxycodone = models.PositiveSmallIntegerField()
    requiredRes_cat2_cisatricurium = models.PositiveSmallIntegerField()
    requiredRes_cat2_vecuronium = models.PositiveSmallIntegerField()

    requiredRes_cat3_ct = models.PositiveSmallIntegerField()
    requiredRes_cat3_mri = models.PositiveSmallIntegerField()
    requiredRes_cat3_ppe = models.PositiveSmallIntegerField()
    requiredRes_cat3_propofol = models.PositiveSmallIntegerField()
    requiredRes_cat3_dexmedetomidine = models.PositiveSmallIntegerField()
    requiredRes_cat3_fentanyl = models.PositiveSmallIntegerField()
    requiredRes_cat3_morphine = models.PositiveSmallIntegerField()
    requiredRes_cat3_morphineOral = models.PositiveSmallIntegerField()
    requiredRes_cat3_oxycodone = models.PositiveSmallIntegerField()
    requiredRes_cat3_cisatricurium = models.PositiveSmallIntegerField()
    requiredRes_cat3_vecuronium = models.PositiveSmallIntegerField()

    # Average (mean) days of ICU/ECMO/vent/dialysis
    daysIcu_cat1 = models.PositiveSmallIntegerField()
    daysIcu_cat2 = models.PositiveSmallIntegerField()
    daysIcu_cat3 = models.PositiveSmallIntegerField()

    daysEcmo_cat1 = models.PositiveSmallIntegerField()
    daysEcmo_cat2 = models.PositiveSmallIntegerField(blank=True)
    daysEcmo_cat3 = models.PositiveSmallIntegerField(blank=True)

    daysVent_cat1 = models.PositiveSmallIntegerField(blank=True)
    daysVent_cat2 = models.PositiveSmallIntegerField()
    daysVent_cat3 = models.PositiveSmallIntegerField(blank=True)

    daysDialysis_cat1 = models.PositiveSmallIntegerField()
    daysDialysis_cat2 = models.PositiveSmallIntegerField()
    daysDialysis_cat3 = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/sims/{self.pk}"
