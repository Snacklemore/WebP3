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
        if employee_id != 'null':
            employee = self.database.get_list(self.database.employee, entry_id=employee_id, relations=True)
            return json.dumps(employee)

        elif employee_id is None:
            employee_list = self.database.get_list(self.database.employee)
            return json.dumps(employee_list)
        elif employee_id == 'null':
            di = {'0': ["", ""]}
            return json.dumps(di)

    # Returns employee id as a string
    def POST(self, employee_id, second_name, first_name, academic_degree, occupation):
        return self.database.add_employee([second_name, first_name, academic_degree, occupation])

    # Returns True of False as string
    def PUT(self, employee_id, second_name, first_name, academic_degree, occupation):
        return json.dumps(str(self.database.edit_employee(employee_id, [second_name, first_name, academic_degree, occupation])))

    # Returns True of False as string
    def DELETE(self, employee_id):
        return str(self.database.delete_employee(employee_id))


@cherrypy.expose
class mitarbeiter_detail_cl(Parent):
    # -------------------------------------------------------
    def __init__(self):
        # -------------------------------------------------------
      pass

    # -------------------------------------------------------
    def GET(self, id=None, mitarbeiterAnzeigen=None):
        # -------------------------------------------------------
        retVal_s = ''
        retVal_s = self.get_mitarbeiter_anzeigen(id)

        return retVal_s

    # -------------------------------------------------------
    def get_mitarbeiter_anzeigen(self, id_spl):
        # -------------------------------------------------------
        # Daten auslesen und in die jeweilige "data_" packen
        training = self.database.get_list(self.database.training)
        certs = self.database.get_list(self.database.certificate)
        quali = self.database.get_list(self.database.qualification)
        employee = self.database.get_list(self.database.employee, entry_id=id_spl, relations=True)


        data_m = employee
        data_w = training
        data_q = quali
        data_z = certs
        data_o = [data_m]
        return json.dumps(data_o)


@cherrypy.expose
class weiterbildung_detail_cl(Parent):
    # -------------------------------------------------------
    def __init__(self):
        # -------------------------------------------------------
      pass

    # -------------------------------------------------------
    def GET(self, id=None, isW=None,weiterbildungAnzeigen=None):
        # -------------------------------------------------------
        retVal_s = ''
        retVal_s = self.get_weiterbildung_anzeigen(id)

        return retVal_s

    # -------------------------------------------------------
    def get_weiterbildung_anzeigen(self, id_spl):
        # Daten auslesen und in die jeweilige "data_" packen
        training = self.database.get_list(self.database.training,entry_id=id_spl,relations=True)
        certs = self.database.get_list(self.database.certificate)
        quali = self.database.get_list(self.database.qualification)
        #employee = self.database.get_list(self.database.employee, entry_id=id_spl, relations=True)

       # data_m = employee
        data_w = training
        data_q = quali
        data_z = certs
        data_o = [data_w]
        return json.dumps(data_o)

@cherrypy.expose
class Pflege_Weiterbildung(Parent):

    def __init__(self):
        pass

    # Returns string dict
    def GET(self, training_id=None, weiterbildung=None):
        if training_id != 'null':
            training = self.database.get_list(self.database.training, entry_id=training_id, relations=True)
            return json.dumps(training)
        elif training_id is None:
            training_list = self.database.get_list(self.database.training)
            return json.dumps(training_list)
        elif training_id == 'null':
            di = {'0': ["", ""]}
            return json.dumps(di)



    # Returns new training id as string
    def POST(self, training_id, title, date_begin, date_end, description, max_attendees, min_attendees):
        return self.database.add_training([title, date_begin, date_end, description, max_attendees, min_attendees])

    # Returns true of false as string
    def PUT(self, training_id, title, date_begin, date_end, description, max_attendees, min_attendees):
        return json.dumps(str(self.database.edit_training(training_id, [title, date_begin, date_end, description, max_attendees,
                                                             min_attendees])))

    def DELETE(self, training_id):
        return str(self.database.delete_training(training_id))


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


# ----------------------------------------------------------
class Teilnahme_cl(Parent):
    # ----------------------------------------------------------

    exposed = True
    # -------------------------------------------------------
    def __init__(self):
     # -------------------------------------------------------
        pass

    # -------------------------------------------------------
    def GET(self, id=None,wAnzeige=None, teilnahme=None):
    # -------------------------------------------------------
        if id and wAnzeige is None:
            employee = self.database.get_list(self.database.employee, entry_id=id, relations=True,
                                              relations_true_value=False)

            participated_training = []
            participated_training_ids = []
            not_participated_training = []

            for counter, training in enumerate(employee[4]):
                participated_training.append(self.database.get_list(self.database.training, entry_id=training[0]))

                # Add the participation status and the training id
                participated_training[counter].append(training[0])
                participated_training[counter].append(training[1])


                # Add participated training id array for comparison later
                participated_training_ids.append(training[0])

            # Filter out non participated trainings
            trainings_list = self.database.get_list(self.database.training)
            notParticipatedTrainingList = []
            for training_id in trainings_list:
                if training_id not in participated_training_ids:
                    entry = trainings_list[training_id][0:6]
                    entry.append(training_id)
                    notParticipatedTrainingList.append(entry)

            not_participated_training.append(notParticipatedTrainingList)
            participatedTrainingList = []
            participatedTrainingList.append(participated_training)
            idlist = [id]
            return json.dumps(employee+not_participated_training+participatedTrainingList+idlist)
        elif id and wAnzeige == 'isW':
            #get trainingdata with id and participants(with ids)
            training = self.database.get_list(self.database.training, entry_id=id, relations=True)
            idlist = [id]

            return json.dumps(training + idlist)

        else:
            employee_list = self.database.get_list(self.database.employee)
            train_list = self.database.get_list(self.database.training)
            return json.dumps(employee_list + train_list)
     # -------------------------------------------------------

    def POST(self, id_w, id_m):
    # -------------------------------------------------------

        var = self.database.add_training_to_employee(employee_id=id_m, training_id=id_w, employee_participation_status="angemeldet")

        return str(id)

        # -------------------------------------------------------

    def PUT(self, id_m, id_w, status):
        # -------------------------------------------------------
        #noway to change status in one call. get employee ->change its training status
        #-> put back in
        # get training->change training status of employee->putback in
        var = self.database.change_employee_participation_status(employee_id=id_m, training_id=id_w,new_status=status)

        return

        # -------------------------------------------------------

    def DELETE(self, id_w, id_m):
        # -------------------------------------------------------
        var = self.database.delete_employee_from_training(employee_id=id_m, training_id=id_w)

        return
        # -------------------------------------------------------

    def getList_w(self):
        # -------------------------------------------------------


        return

        # -------------------------------------------------------

    def getDetail_mt(self, id_spl):
        # -------------------------------------------------------


        return

        # -------------------------------------------------------

    def getDetail_wt(self, id_spl):
        # -------------------------------------------------------


        return


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

    def GET(self, id=None, auswertungMitarbeiter=None):
        if id == None:
            employee_list = self.database.get_list(self.database.employee, relations=True, relations_true_value=True)
            employee_list = sorted(employee_list.items(), key=lambda x: x[1][0])

            for employee in employee_list:
                employee[1][4] = sorted(employee[1][4], key=lambda x: x[1])

            return json.dumps(employee_list)
        else:
            employee = self.database.get_list(self.database.employee,entry_id=id, relations=True)
            return json.dumps(employee)
            pass


@cherrypy.expose
class Auswertung_Weiterbildung(Parent):

    def GET(self, id=None, auswertungWeiterbildung=None):
        if id == None:
            training_list = self.database.get_list(self.database.training, relations=True, relations_true_value=True)
            training_list = sorted(training_list.items(), key=lambda x: x[1][0])
            for training in training_list:
                training[1][-1] = list(filter(lambda x: x[4] == "erfolgreich beendet", training[1][-1]))

            return json.dumps(training_list)
        else:
            training = self.database.get_list(self.database.training,entry_id=id, relations=True)
            return json.dumps(training)


@cherrypy.expose
class Auswertung_Zertifikat(Parent):

    def GET(self, id=None, auswertungZertifikat=None):
        if id == None:
            certificate_list = self.database.get_list(self.database.certificate, relations=True, relations_true_value=True)

            certificate_list = sorted(certificate_list.items(), key=lambda x: x[1][0])

            return json.dumps(certificate_list)
        else:
            certificate = self.database.get_list(self.database.certificate,entry_id=id, relations=True)
            return json.dumps(certificate)
