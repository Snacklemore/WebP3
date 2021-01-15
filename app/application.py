from .database import Database
from .view import View_cl
import cherrypy
import json


class Parent:
    # Static Variables
    database = Database("database.json", "Mitarbeiter", "Weiterbildungen", "Qualifikation", "Zertifikat")
    view_o = View_cl()

    # Method to merge dictionaries
    # Entries with same key will be overwritten
    @staticmethod
    def merge_dictionaries(*args):
        return_dictionary = dict()

        for dictionary in args:
            return_dictionary.update(dictionary)

        return return_dictionary

    # Creates a dict from values
    # Expects unlimited tuples as parameters
    # First tuple value is the key, second is the value of the key
    # example function call:
    # create_dict_from_values_and_name_list(('first_key', 'first_value'), ('second_key', 'second_value'))
    @staticmethod
    def create_dict_from_values_and_name_list(*args):
        return_dictionary = dict()

        for value in args:
            if isinstance(value, tuple) and len(value) == 2:
                return_dictionary[value[0]] = value[1]

        return return_dictionary

    # Creates a dict from values
    # Key is the index of the entry in args
    @staticmethod
    def create_dict_from_values(*args):
        return_dictionary = dict()

        for counter, value in enumerate(args):
            return_dictionary[counter] = value

        return return_dictionary


@cherrypy.expose
class Startseite(Parent):

    def GET(self):
        # change_count methods return int
        employee_count = self.database.change_count(self.database.employee)
        training_count = self.database.change_count(self.database.training)
        participation_count = self.database.change_participation_count()

        return_dict = self.create_dict_from_values_and_name_list(('Employee_count', employee_count),
                                                                 ('training_count', training_count),
                                                                 ('participation_count', participation_count))

        return return_dict


@cherrypy.expose
class Pflege_Mitarbeiter(Parent):

    def __init__(self):
        pass

    # Returns string dict
    def GET(self, employee_id=None, mitarbeiter=None):
        if employee_id:
            employee = self.database.get_list(self.database.employee, entry_id=employee_id, relations=True)
            return json.dumps(employee)

        else:
            employee_list = self.database.get_list(self.database.employee)
            return json.dumps(employee_list)

    # Returns employee id as a string
    def POST(self, second_name, first_name, academic_degree, occupation):
        return self.database.add_employee([second_name, first_name, academic_degree, occupation])

    # Returns True of False as string
    def PUT(self, employee_id, second_name, first_name, academic_degree, occupation):
        return str(self.database.edit_employee(employee_id, [second_name, first_name, academic_degree, occupation]))

    # Returns True of False as string
    def DELETE(self, employee_id):
        return str(self.database.delete_employee(employee_id))


@cherrypy.expose
class Pflege_Weiterbildung(Parent):

    # Returns string dict
    def GET(self, training_id=None):
        if training_id:
            training = self.database.get_list(self.database.training, entry_id=training_id, relations=True)
            return json.dumps(training)

        else:
            training_list = self.database.get_list(self.database.training)
            return json.dumps(training_list)

    # Returns new training id as string
    def POST(self, title, date_begin, date_end, description, max_attendees, min_attendees):
        return self.database.add_training([title, date_begin, date_end, description, max_attendees, min_attendees])

    # Returns true of false as string
    def PUT(self, training_id, title, date_begin, date_end, description, max_attendees, min_attendees):
        return str(self.database.edit_training(training_id, [title, date_begin, date_end, description, max_attendees,
                                                             min_attendees]))

    def DELETE(self, training_id):
        return str(self.database.training(training_id))


@cherrypy.expose
class Teilnahme_Mitarbeiter(Parent):

    # Returns string dict
    def GET(self, employee_id=None):
        if employee_id:
            employee = self.database.get_list(self.database.employee, entry_id=employee_id, relations=True)
            return json.dumps(employee)

        else:
            employee_list = self.database.get_list(self.database.employee)
            return json.dumps(employee_list)

    # TODO
    def POST(self):
        pass

    # TODO
    def PUT(self):
        pass

    # TODO
    def DELETE(self):
        pass


@cherrypy.expose
class Teilnahme_Weiterbildung(Parent):

    # Returns string dict
    def GET(self, training_id=None):
        if training_id:
            training = self.database.get_list(self.database.training, entry_id=training_id, relations=True)
            return json.dumps(training)

        else:
            training_list = self.database.get_list(self.database.training)
            return json.dumps(training_list)

    # TODO
    def POST(self):
        pass

    # TODO
    def PUT(self):
        pass


@cherrypy.expose
class Auswertung_Mitarbeiter(Parent):

    def GET(self):
        employee_list = self.database.get_list(self.database.employee, relations=True, relations_true_value=True)
        employee_list = sorted(employee_list.items(), key=lambda x: x[1][0])

        for employee in employee_list:
            employee[1][4] = sorted(employee[1][4], key=lambda x: x[1])

        return json.dumps(employee_list)


@cherrypy.expose
class Auswertung_Weiterbildung(Parent):

    def GET(self):
        training_list = self.database.get_list(self.database.training, relations=True, relations_true_value=True)
        training_list = sorted(training_list.items(), key=lambda x: x[1][0])
        for training in training_list:
            training[1][-1] = list(filter(lambda x: x[4] == "erfolgreich beendet", training[1][-1]))

        return json.dumps(training_list)


@cherrypy.expose
class Auswertung_Zertifikat(Parent):

    def GET(self):
        certificate_list = self.database.get_list(self.database.certificate, relations=True, relations_true_value=True)

        certificate_list = sorted(certificate_list.items(), key=lambda x: x[1][0])

        return json.dumps(certificate_list)