import json

class TimedStateSample:
    def __init__(self, current_time, decay_values, token_counts, marking, place_list, resource_count=None, resource_indices=None, loadExisting=False):
        self.data = {'current_time' : current_time}

        if not loadExisting:
            decay_vector = []
            token_count_vector = []
            marking_vector = []

            for place in place_list:
                decay_vector.append(decay_values[str(place)])
                token_count_vector.append(token_counts[str(place)])
                
                ##### BUGFIX
                """
                if place in marking:
                    marking_vector.append(1)
                """
                if str(place) in [str(key) for key in marking.keys()]:
                    for key, val in marking.items():
                        if str(key) == str(place):
                            marking_vector.append(val)
                            break
                else:
                    marking_vector.append(0)
                ##### ------->

            if resource_count is None:
                self.data["TimedStateSample"] = [decay_vector, token_count_vector, marking_vector]
            else:
                resource_vector = [0 for i in range(len(resource_indices.keys()))]
                for key in resource_count.keys():
                    resource_vector[resource_indices[key]] = resource_count[key]
                self.data["TimedStateSample"] = [decay_vector, token_count_vector, marking_vector, resource_vector]
        else:
            """ Load from File """
            self.data = {'current_time' : current_time,
                         'TimedStateSample' : [decay_values, token_counts, marking]}

    def setResourceVector(self, resource_vector):
        if len(self.data["TimedStateSample"]) < 4:
            self.data["TimedStateSample"].append(resource_vector)
        else:
            self.data["TimedStateSample"][3] = resource_vector

    def setRecentEvent(self, event):
        self.data["recentEvent"] = event

    def setNextEvent(self, event):
        self.data["nextEvent"] = event

    def export(self):
        return self.data

    def setGender(self, gender):
        self.data["gender"] = gender

    def setAge(self, age):
        self.data["age"] = age

    def setCharlson(self, charlson):
        self.data["charlson"] = charlson

    def setElixhauser(self, elixhauser):
        self.data["elixhauser"] = elixhauser

    def setSeverity(self, severity):
        self.data["severity"] = severity

    def setEthnicity(self, ethnicity):
        # self.data["ethnicity"] = ethnicity
        if "white" in str(ethnicity).lower():
            self.data["ethnicity"] = 1
        elif "black" in str(ethnicity).lower():
            self.data["ethnicity"] = 2
        elif "asian" in str(ethnicity).lower() or "middle eastern" in str(ethnicity).lower():
            self.data["ethnicity"] = 3
        elif "latino" in str(ethnicity).lower() or "hispanic" in str(ethnicity).lower():
            self.data["ethnicity"] = 4
        else:
            self.data["ethnicity"] = 5

def loadTimedStateSamples(filename):
    """
    Load decay functions for a given petri net from file.

    :param filename: filename of Timed State Samples
    :return: list containing TimedStateSample objects
    """
    actual_events = list()
    final = list()
    with open(filename) as json_file:
        tss = json.load(json_file)
        for sample in tss:
            ts = TimedStateSample(sample["current_time"],
                             sample["TimedStateSample"][0],
                             sample["TimedStateSample"][1],
                             sample["TimedStateSample"][2],
                             None, loadExisting=True)
            """ Add resource count if exists """
            if len(sample["TimedStateSample"]) > 3:
                ts.setResourceVector(sample["TimedStateSample"][3])

            """ Add next event if present """
            if "nextEvent" in sample.keys():
                ts.setNextEvent(sample["nextEvent"])
                actual_events.append(sample["nextEvent"])

            final.append(ts)
    return final, actual_events
