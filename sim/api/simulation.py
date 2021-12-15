import numpy as np
from enum import Enum
from collections import defaultdict

class Resources(Enum):
    CT = 1
    MRI = 2
    VENTILATOR = 3
    PPE = 4
    ECMO = 5

class Medication(Enum):

    # Sedatives
    PROPOFOL = 6
    DEXMEDETOMIDINE = 7
    # Analgesics
    FENTANYL = 8
    MORPHINE = 9
    # Oral Narcotics
    MORPHINE_ORAL = 10
    OXYCODONE = 11
    # NRMS
    CISATRICURIUM = 12
    VECURONIUM = 13

class States(Enum):
    BED = 1
    VENTILATED = 2
    ECMO = 3
    DISCHARGED = 4

class Simulation(object):

    def __init__(self, inputs):
        self.simDays = inputs["simDays"]  # 100
        self.meanDaysIcu = inputs["meanDaysIcu"]  # [3, 10, 17]
        self.meanDaysVent = inputs["meanDaysVent"]  # [3, 10, 17]
        self.meanDaysEcmo = inputs["meanDaysEcmo"]  # [3, 10, 17]
        self.meanDaysDialysis = inputs["meanDaysDialysis"]  # [3, 10, 17]
        self.narrivals = inputs["narrivals"]  # [0, 0, 15]  # arrivals per !SHIFT!
        self.ninitialPatients = inputs["ninitials"]  # [0, 0, 15]  # arrivals per !SHIFT! per category
        self.availableResources = inputs["availableResources"]
        self.availableMedication = inputs["availableMedication"]
        self.ecmo = inputs["ecmo"]  # [resourcesRequired], [consultationsRequired]
        self.bed = inputs["bed"]  # [resourcesRequired], [consultationsRequired])
        self.ventilated = inputs["ventilated"]  # [resourcesRequired], [consultationsRequired])

    def run_sim(self):
        # Initialize time vector of consultations
        consultations = []

        # Set up available resources
        resources = defaultdict(list)
        medication = defaultdict(list)
        for r in Resources:
            resources[r.name] = [self.availableResources[r.name]]
        for m in Medication:
            medication[m.name] = [self.availableMedication[m.name]]

        # Initialize patients
        patients_t = self.initial_patients()
        patients_textend = patients_t.extend

        # Run time-update
        for dt in range(self.simDays * 2 + 1):
            newpt = self.arrivals()  # new arrivals
            patients_textend(newpt)  # add to existing patients
            patients_t, resources_t, medication_t, consultations_t = self.time_update(patients_t)  # time update
            # print(resources)
            # print(medication)
            # print(medication_t)
            # record resources for each shift
            for r in Resources:
                try:
                    if r in (Resources.ECMO, Resources.VENTILATOR):
                        # non-depletable (non-accumulative) resources
                        resources[r.name].append(self.availableResources[r.name]+resources_t[r])
                    else:
                        # subtract from available resources (count down as resources_t is negative)
                        resources[r.name].append(resources[r.name][-1]+resources_t[r])
                except KeyError:
                    # no such resource defined in 'resources_t' and hence not consumed
                    if r in (Resources.ECMO, Resources.VENTILATOR):
                        # non-depletable (non-accumulative) resources
                        resources[r.name].append(self.availableResources[r.name])
                    else:
                        resources[r.name].append(resources[r.name][-1]+0)

            # record medication for each shift
            for m in Medication:
                try:
                    # subtract from available resources (count down as resources_t is negative)
                    medication[m.name].append(medication[m.name][-1]+medication_t[m])

                except KeyError:
                    # no such resource defined in 'resources_t' and hence not consumed
                    medication[m.name].append(medication[m.name][-1]+0)


            # record consultations
            consultations.append(consultations_t)

        return {'resources': resources,
                'medication': medication,
                'consultations': consultations,
                'days': np.arange(0, self.simDays + 0.5, 0.5).tolist()}

    # ----------------------------------- functions for running simulation ---------------------------------------------

    def initial_patients(self):
        peeps = []
        append = peeps.append

        cuminitials = np.cumsum(np.round(self.ninitialPatients))
        for i in range(cuminitials[2]):
            # assign properties according to category of initial patients
            if i < cuminitials[0]:      # ECMO patients
                category = 1
            elif i < cuminitials[1]:    # Ventilated patients
                category = 2
            else:                       # Patients in ICU bed
                category = 3

            # assign days in ICU/ECMO/ventilator/dialysis
            daysdialysis = self.assign_days(self.meanDaysDialysis[category - 1])
            daysvent = self.assign_days(self.meanDaysVent[category - 1])
            daysecmo = self.assign_days(self.meanDaysEcmo[category - 1])
            daysicu = self.assign_days(self.meanDaysIcu[category - 1])


            # assign days patient has already been in ICU and used resources with uniform distribution
            if category == 1:  # ECMO

                # ensure that days in ICU >= days on dialysis/ventilator+ecmo
                daysicu = np.maximum(np.maximum(daysicu, daysdialysis), daysvent + daysecmo)

                state = States.ECMO
                startecmo = self.get_start_day_center(daysicu, daysecmo+daysvent)  # set ECMO+vent to middle of ICU stay
                startvent = startecmo + daysecmo  # ventilator after ECMO
                startdialysis = self.get_start_day_center(daysicu, daysdialysis)  # set dialysis to middle of ICU stay


                if daysecmo == 0:
                    # Pt is not on ECMO according randomly assigned 'daysecmo' given Erlang distribution
                    # -> ensure that it stays there for one shift

                    # negative value ensures that patient stays on ECMO for one shift (see 'time_update' function)
                    accdaysecmo = -0.5

                    # Set remaining days in ICU
                    if daysicu == 0:
                        # Pt is not in ICU according randomly assigned 'daysicu' given Erlang distribution
                        # -> discharge after one shift

                        # negative value ensures that patient stays in ICU for one shift (see 'time_update' function)
                        accdaysicu = -0.5
                    else:
                        # Set accumulated days in ICU uniformly in [0, 'daysicu' - 0.5]
                        # ('-0.5' to ensure that pt stays for one shift
                        accdaysicu = np.round((daysicu - 0.5) * np.random.rand(1) * 2) / 2

                else:
                    # Pt on ECMO is consistent with randomly assigned (i.e. 'daysecmo' > 0)
                    # -> assign accumulated days uniformly

                    # Set accumulated days on ECMO uniformly between [0,'daysecmo'-0.5]
                    # ('-0.5' to ensure that pt stays for one shift
                    accdaysecmo = np.round((daysecmo-0.5) * np.random.rand(1) * 2) / 2
                    accdaysicu = startecmo + accdaysecmo

                #  Set accumulated days on ventilator/dialysis according to days in ICU ('accdaysicu')
                if accdaysicu <= startvent:
                    accdaysvent = 0
                elif accdaysicu <= startvent + daysvent:
                    accdaysvent = accdaysicu - startvent
                else:
                    accdaysvent = daysvent

                if accdaysicu <= startdialysis:
                    accdaysdialysis = 0
                elif accdaysicu <= startdialysis + daysdialysis:
                    accdaysdialysis = accdaysicu - startdialysis
                else:
                    accdaysdialysis = daysdialysis

                # Add patient to list
                append(self.create_patient(daysicu, daysvent, daysdialysis, daysecmo, category, state,
                                           accdaysicu=accdaysicu, accdaysecmo=accdaysecmo,
                                           accdaysvent=accdaysvent, accdaysdialysis=accdaysdialysis,
                                           startecmo=startecmo, startvent=startvent,
                                           startdialysis=startdialysis))


            elif category == 2:  # Ventilated

                # ensure that days in ICU >= days on dialysis/ventilator
                daysicu = np.maximum(np.maximum(daysicu, daysdialysis), daysvent)

                state = States.VENTILATED
                daysecmo = 0  # never do ECMO when in category 2 (ventilated) ['accdaysecmo' not necessary]
                startvent = self.get_start_day_center(daysicu, daysvent)  # set ventilator to middle of ICU stay
                startdialysis = self.get_start_day_center(daysicu, daysdialysis)  # set dialysis to middle of ICU stay

                # logic as above for ECMO
                if daysvent == 0:
                    accdaysvent = -0.5
                    if daysicu == 0:
                        accdaysicu = -0.5
                    else:
                        accdaysicu = np.round((daysicu - 0.5) * np.random.rand(1) * 2) / 2
                else:
                    accdaysvent = np.round((daysvent - 0.5) * np.random.rand(1) * 2) / 2
                    accdaysicu = startvent + accdaysvent

                if accdaysicu <= startdialysis:
                    accdaysdialysis = 0
                elif accdaysicu <= startdialysis + daysdialysis:
                    accdaysdialysis = accdaysicu - startdialysis
                else:
                    accdaysdialysis = daysdialysis

                append(self.create_patient(daysicu, daysvent, daysdialysis, daysecmo, category, state,
                                           accdaysicu=accdaysicu, accdaysvent=accdaysvent,
                                           accdaysdialysis=accdaysdialysis, startvent=startvent,
                                           startdialysis=startdialysis))


            elif category == 3:  # BED

                # ensure that days in ICU >= days on dialysis
                daysicu = self.assign_days(self.meanDaysIcu[category - 1])
                daysicu = np.maximum(daysicu, daysdialysis)

                state = States.BED
                daysecmo = 0  # never use ECMO
                daysvent = 0  # never use ventilator
                startdialysis = self.get_start_day_center(daysicu, daysdialysis)  # set dialysis to middle of ICU stay

                # Set remaining days in ICU (logic as above)
                if daysicu == 0:
                    accdaysicu = -0.5
                else:
                    accdaysicu = np.round((daysicu - 0.5) * np.random.rand(1) * 2) / 2

                if accdaysicu <= startdialysis:
                    accdaysdialysis = 0
                elif accdaysicu <= startdialysis + daysdialysis:
                    accdaysdialysis = accdaysicu - startdialysis
                else:
                    accdaysdialysis = daysdialysis

                append(self.create_patient(daysicu, daysvent, daysdialysis, daysecmo, category, state,
                                           accdaysicu=accdaysicu, accdaysdialysis=accdaysdialysis,
                                           startdialysis=startdialysis))
        return peeps

    def arrivals(self):
        cumarrivals = np.cumsum(np.round(self.narrivals))
        peeps = []
        append = peeps.append
        for i in range(cumarrivals[2]):

            # assign category according to arrivals
            if i < cumarrivals[0]:  # ECMO
                category = 1
                state = States.ECMO
            elif i < cumarrivals[1]:  # Ventilated
                category = 2
                state = States.VENTILATED
            else:  # BED
                category = 3
                state = States.BED

            # assign days in ICU/ECMO/ventilator/dialysis
            daysdialysis = self.assign_days(self.meanDaysDialysis[category - 1])
            daysvent = self.assign_days(self.meanDaysVent[category - 1])
            daysecmo = self.assign_days(self.meanDaysEcmo[category - 1])
            daysicu = self.assign_days(self.meanDaysIcu[category - 1])

            if category == 1:  # ECMO
                # ensure that days in ICU >= days on dialysis/ECMO + ventilated
                daysicu = np.maximum(np.maximum(daysicu, daysdialysis), daysecmo + daysvent)
                startecmo = self.get_start_day_center(daysicu, daysecmo)  # set ECMO to middle of ICU stay
                startvent = startecmo + daysecmo  # ventilator after ECMO
                append(self.create_patient(daysicu, daysvent, daysdialysis, daysecmo, category, state,
                                           startecmo=startecmo, startvent=startvent))
            elif category == 2:  # Ventilated
                daysecmo = 0  # never use ECMO when category 'Ventilated'
                daysicu = np.maximum(np.maximum(daysicu, daysdialysis), daysvent)
                append(self.create_patient(daysicu, daysvent, daysdialysis, daysecmo, category, state))
            elif category == 3:  # BED
                daysecmo = 0  # never use ECMO
                daysvent = 0  # never use ventilator
                daysicu = np.maximum(daysicu, daysdialysis)
                append(self.create_patient(daysicu, daysvent, daysdialysis, daysecmo, category, state))

        return peeps

    def get_start_day_center(self, los, days):
        if days > 0:
            startshift = (los - days) / 2
            startshift = np.floor(startshift * 2) / 2  # round down to nearest 0.5 increment
        else:
            startshift = los
        return startshift

    def create_patient(self, daysicu, daysvent, daysdialysis, daysecmo, category, state, **kwargs):

        return {
            "daysecmo": daysecmo,
            "daysicu": daysicu,
            "daysvent": daysvent,
            "daysdialysis": daysdialysis,
            "category": category,
            "accdaysecmo": kwargs["accdaysecmo"] if "accdaysecmo" in kwargs else 0,
            "accdaysicu": kwargs["accdaysicu"] if "accdaysicu" in kwargs else 0,
            "accdaysvent": kwargs["accdaysvent"] if "accdaysvent" in kwargs else 0,
            "accdaysdialysis": kwargs["accdaysdialysis"] if "accdaysdialysis" in kwargs else 0,
            "state": state,
            "startecmo": kwargs["startecmo"] if "startecmo" in kwargs else self.get_start_day_center(daysicu, daysecmo),
            "startvent": kwargs["startvent"] if "startvent" in kwargs else self.get_start_day_center(daysicu, daysvent),
            "startdialysis":
                kwargs["startdialysis"] if "startdialysis" in kwargs else self.get_start_day_center(daysicu,
                                                                                                    daysdialysis)
        }

    def assign_days(self, mean):
        s = round(mean)

        # if desired mean is zero set rate = 100 as mean of Erlang distribution is = s/r, otherwise r = 1
        if s == 0:
            s = 1
            rate = 100
        else:
            rate = 1

        days = -1 / rate * np.log(np.prod(np.random.rand(s)))  # assignment according to Erlang distribution
        days = np.round(days * 2) / 2  # round to nearest .5
        return days

    def time_update(self, peeps):
        # TODO: add vent, dialysis, ecmo to resources
        resources = defaultdict(int)  # resources are subtracted
        medication = defaultdict(int)  # resources are subtracted
        consultations = 0  # (#) of consultations
        for pt in peeps:
            # Discharge as days in ICU elapsed
            if pt['accdaysicu'] == pt['daysicu']:
                pt['state'] = States.DISCHARGED

            if pt['state'] is States.BED:

                # Move to ECMO state
                if pt['accdaysicu'] == pt['startecmo']:
                    pt['state'] = States.ECMO
                    pt['accdaysicu'] += 0.5  # increment shifts in ICU
                    pt['accdaysecmo'] += 0.5  # increment shifts on ECMO

                    # update resources
                    for r in Resources:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            if r == Resources.ECMO:
                                resources[r] -= 1
                            else:
                                resources[r] -= self.ecmo["resourcesRequired"][r.name] / 2
                        except KeyError:
                            continue

                    # update medication
                    for m in Medication:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            medication[m] -= self.ecmo["medicationRequired"][m.name] / 2
                        except KeyError:
                            continue

                    # update consultations per patient per shift
                    consultations += self.ecmo["consultationsRequired"] / 2

                # Move to ventilator state
                elif pt['accdaysicu'] == pt['startvent']:
                    pt['state'] = States.VENTILATED
                    pt['accdaysvent'] += 0.5  # increment shifts ventilator
                    pt['accdaysicu'] += 0.5  # increment shifts in ICU

                    # update resources
                    for r in Resources:
                        try:
                            # (#) of resource r during current shift in state VENTILATED
                            if r == Resources.VENTILATOR:
                                resources[r] -= 1
                            else:
                                resources[r] -= self.ventilated["resourcesRequired"][r.name] / 2
                        except KeyError:
                            continue

                    # update medication
                    for m in Medication:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            medication[m] -= self.ventilated["medicationRequired"][m.name] / 2
                        except KeyError:
                            continue

                    # update consultations per patient per shift
                    consultations += self.ventilated["consultationsRequired"] / 2

                # Stay in BED state
                else:
                    pt['accdaysicu'] += 0.5  # increment shifts in ICU
                    # update resources
                    for r in Resources:
                        try:
                            # (#) of resource r during current shift in state BED
                            resources[r] -= self.bed["resourcesRequired"][r.name] / 2
                        except KeyError:
                            continue

                    # update medication
                    for m in Medication:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            medication[m] -= self.bed["medicationRequired"][m.name] / 2
                        except KeyError:
                            continue

                    # update consultations per patient per shift
                    consultations += self.bed["consultationsRequired"] / 2

            elif pt['state'] is States.ECMO:
                # Stay in ECMO state
                if pt['accdaysecmo'] < pt['daysecmo']:
                    pt['accdaysicu'] += 0.5  # increment shifts in ICU
                    pt['accdaysecmo'] += 0.5  # increment shifts on ECMO

                    # update resources
                    for r in Resources:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            if r == Resources.ECMO:
                                resources[r] -= 1
                            else:
                                resources[r] -= self.ecmo["resourcesRequired"][r.name] / 2
                        except KeyError:
                            continue

                    # update medication
                    for m in Medication:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            medication[m] -= self.ecmo["medicationRequired"][m.name] / 2
                        except KeyError:
                            continue

                    # update consultations per patient per shift
                    consultations += self.ecmo["consultationsRequired"] / 2

                # Move to ventilator state (ventilator always after ECMO)
                elif pt['accdaysicu'] == pt['startvent']:
                    pt['state'] = States.VENTILATED
                    pt['accdaysvent'] += 0.5  # increment shifts ventilator
                    pt['accdaysicu'] += 0.5  # increment shifts in ICU

                    # update resources
                    for r in Resources:
                        try:
                            # (#) of resource r during current shift in state VENTILATED
                            if r == Resources.VENTILATOR:
                                resources[r] -= 1
                            else:
                                resources[r] -= self.ventilated["resourcesRequired"][r.name] / 2
                        except KeyError:
                            continue

                    # update medication
                    for m in Medication:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            medication[m] -= self.ventilated["medicationRequired"][m.name] / 2
                        except KeyError:
                            continue

                    # update consultations per patient per shift
                    consultations += self.ventilated["consultationsRequired"] / 2

                # Move to BED
                else:
                    pt['state'] = States.BED
                    pt['accdaysicu'] += 0.5  # increment shifts in ICU

                    # update resources
                    for r in Resources:
                        try:
                            # (#) of resource r during current shift in state BED
                            resources[r] -= self.bed["resourcesRequired"][r.name] / 2
                        except KeyError:
                            continue

                    # update medication
                    for m in Medication:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            medication[m] -= self.bed["medicationRequired"][m.name] / 2
                        except KeyError:
                            continue

                    # update consultations per patient per shift
                    consultations += self.bed["consultationsRequired"] / 2

            elif pt['state'] is States.VENTILATED:
                # Move to ECMO state
                if pt['accdaysicu'] == pt['startecmo']:
                    pt['state'] = States.ECMO
                    pt['accdaysicu'] += 0.5  # increment shifts in ICU
                    pt['accdaysecmo'] += 0.5  # increment shifts on ECMO

                    # update resources
                    for r in Resources:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            if r == Resources.ECMO:
                                resources[r] -= 1
                            else:
                                resources[r] -= self.ecmo["resourcesRequired"][r.name] / 2
                        except KeyError:
                            continue

                    # update medication
                    for m in Medication:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            medication[m] -= self.ecmo["medicationRequired"][m.name] / 2
                        except KeyError:
                            continue

                    # update consultations per patient per shift
                    consultations += self.ecmo["consultationsRequired"] / 2

                # Stay ventilated
                elif pt['accdaysvent'] < pt['daysvent']:
                    pt['accdaysvent'] += 0.5  # increment shifts ventilator
                    pt['accdaysicu'] += 0.5  # increment shifts in ICU

                    # update resources
                    for r in Resources:
                        try:
                            # (#) of resource r during current shift in state VENTILATED
                            if r == Resources.VENTILATOR:
                                resources[r] -= 1
                            else:
                                resources[r] -= self.ventilated["resourcesRequired"][r.name] / 2
                        except KeyError:
                            continue

                    # update medication
                    for m in Medication:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            medication[m] -= self.ventilated["medicationRequired"][m.name] / 2
                        except KeyError:
                            continue

                    # update consultations per patient per shift
                    consultations += self.ventilated["consultationsRequired"] / 2

                # Move to BED
                else:
                    pt['state'] = States.BED
                    pt['accdaysicu'] += 0.5  # increment shifts in ICU

                    # update resources
                    for r in Resources:
                        try:
                            # (#) of resource r during current shift in state BED
                            resources[r] -= self.bed["resourcesRequired"][r.name] / 2
                        except KeyError:
                            continue

                    # update medication
                    for m in Medication:
                        try:
                            # (#) of resource r during current shift in state ECMO
                            medication[m] -= self.bed["medicationRequired"][m.name] / 2
                        except KeyError:
                            continue

                    # update consultations per patient per shift
                    consultations += self.bed["consultationsRequired"] / 2


        return peeps, resources, medication, consultations

        # WORK ON THE INIT SECTION