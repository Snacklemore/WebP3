import json
import codecs
import os
import copy

class Database:

    # Constructor
    # Parameters database_file_path = json path
    # rest are the entry names in the json file
    def __init__(self, database_file_path, employee, training, qualification, certificate):

        # Variables
        self.json_file_path = database_file_path
        # Complete json file
        self.empty_database = \
        {
            "Mitarbeiter" :
                {
                "Max-ID": "0",
                "Count": "0",
                "List":
                    {

                    }
                },
            "Weiterbildungen" :
                {
                "Max-ID": "0",
                "Count": "0",
                "Participation_count": "0",
                "List":
                    {

                    }
                },
            "Qualifikation":
                {
                "Max-ID": "0",
                "Count": "0",
                "List":
                    {

                    }
                },
            "Zertifikat":
                {
                    "Max-ID": "0",
                    "Count": "0",
                    "List":
                        {

                        }
                }
        }
        self.main_data = None
        # Entry names for json file entries
        self.employee = employee
        self.training = training
        self.qualification = qualification
        self.certificate = certificate

        # Init Functions
        self.read_json_file()

    '''# JSON file methods #'''

    # Method which resets the database marked as private because of 'safety' reasons
    def __reset_json_file(self):
        if self.main_data is not None:
            try:
                file = codecs.open(os.path.join('data', self.json_file_path), 'w', 'utf-8')
                try:
                    json.dump(self.empty_database, file, indent=3)
                finally:
                    file.close()
            except (FileNotFoundError, PermissionError):
                # Raise an error if database file could not be opened
                raise Exception("[!] JSON DATABASE FILE NOT FOUND")

    def read_json_file(self):
        try:
            file = codecs.open(os.path.join('data', self.json_file_path), 'r', 'utf-8')
            try:
                self.main_data = json.load(file)
            finally:
                file.close()
        except (FileNotFoundError, PermissionError):
            # Raise an error if database file could not be opened
            raise Exception("[!] JSON DATABASE FILE NOT FOUND")

    def write_json_file(self):
        if self.main_data is not None:
            try:
                file = codecs.open(os.path.join('data', self.json_file_path), 'w', 'utf-8')
                try:
                    json.dump(self.main_data, file, indent=3)
                finally:
                    file.close()
            except (FileNotFoundError, PermissionError):
                # Raise an error if database file could not be opened
                raise Exception("[!] JSON DATABASE FILE NOT FOUND")

    '''# Database methods #'''

    # Private -> only used by class internal methods
    def __get_list(self, dict_name, entry_id=None):
        # Get list_name dictionary entry
        data = self.main_data.get(dict_name)
        if data:
            data = data.get("List")
            if data:
                if entry_id:
                   data = data.get(entry_id)

        # Raise an exception if function fails -> easier to filter out errors in calling functions
        if data is None:
            raise KeyError("__get_list -> data was None(Database.py line 119)")
        # Notice that data is a REFERENCE to the dictionary
        return data

    # Public method to be accessed from outside the class | Notice it returns a value copy not reference
    # Reason -> database should only be changed from methods inside the class
    # relations: If True relations are returned as well | False: no relations are returned
    # relations_true_value: If True returns the value behind an id | if false returns the id -> is ignored if relations is set False
    def get_list(self, dict_name, entry_id=None, relations=False, relations_true_value=True):
        # Get list_name dictionary entry
        data = self.main_data.get(dict_name)
        if data:
            data = data.get("List")
            if data:
                if entry_id:
                   data = data.get(entry_id)

        # Raise an exception if function fails -> easier to filter out errors in calling functions
        if data is None:
            #return None
            raise KeyError("get_list -> data was None in first check(Line 139 Database.py)")

        # copy by value
        data = copy.deepcopy(data)

        # if no relations should be returned
        if relations is False:

            if dict_name is self.employee:
                # If one entry
                if entry_id is not None:
                    data = data[0:4]
                # If all entries
                else:
                    for employee in data:
                        data[employee] = data[employee][0:4]

            elif dict_name is self.training:
                if entry_id is not None:
                    data = data[0:6]
                else:
                    for training in data:
                        data[training] = data[training][0:6]

            elif dict_name is self.qualification:
                if entry_id is not None:
                    data = data[0:2]
                else:
                    for qualification in data:
                        data[qualification] = data[qualification][0:2]

            elif dict_name is self.certificate:
                if entry_id is not None:
                    data = data[0:3]
                else:
                    for certificate in data:
                        data[certificate] = data[certificate][0:3]

            else:
                raise KeyError("dict_name was not a class object(Line 178 Database.py)")

        # If relations should be returned
        else:
            if relations_true_value is True:

                if dict_name is self.employee:

                    if entry_id is not None:

                        for counter, training in enumerate(data[4]):
                            data[4][counter] = self.get_list(self.training, entry_id=training[0])
                            # Add the participation Status at the end
                            data[4][counter].append(training[1])

                        for counter, qualification_id in enumerate(data[5]):
                            data[5][counter] = self.get_list(self.qualification, entry_id=qualification_id)

                        for counter, certificate_id in enumerate(data[6]):
                            data[6][counter] = self.get_list(self.certificate, entry_id=certificate_id)

                    else:
                        for employee in data:
                            for counter, training in enumerate(data[employee][4]):
                                data[employee][4][counter] = self.get_list(self.training, entry_id=training[0])
                                # Add the participation Status at the end
                                data[employee][4][counter].append(training[1])

                            for counter, qualification_id in enumerate(data[employee][5]):
                                data[employee][5][counter] = self.get_list(self.qualification, entry_id=qualification_id)

                            for counter, certificate_id in enumerate(data[employee][6]):
                                data[employee][6][counter] = self.get_list(self.certificate, entry_id=certificate_id)

                elif dict_name is self.training:
                    if entry_id is not None:

                        if data[6] is not None:
                            data[6] = self.get_list(self.certificate, entry_id=data[6])

                        else:
                            data[6] = []

                        for counter, qualification_id in enumerate(data[7]):
                            data[7][counter] = self.get_list(self.qualification, entry_id=qualification_id)

                        for counter, employee in enumerate(data[8]):
                            data[8][counter] = self.get_list(self.employee, entry_id=employee[0])
                            data[8][counter].append(employee[1])

                    else:
                        for training in data:

                            if data[training][6] is not None:
                                data[training][6] = self.get_list(self.certificate, entry_id=data[training][6])

                            else:
                                data[training][6] = []

                            for counter, qualification_id in enumerate(data[training][7]):
                                data[training][7][counter] = self.get_list(self.qualification, entry_id=qualification_id)

                            for counter, employee in enumerate(data[training][8]):
                                data[training][8][counter] = self.get_list(self.employee, entry_id=employee[0])
                                data[training][8][counter].append(employee[1])

                elif dict_name is self.qualification:
                    if entry_id is not None:

                        for counter, employee_id in enumerate(data[2]):
                            data[2][counter] = self.get_list(self.employee, entry_id=employee_id)
                            data[2][counter].append(employee_id)

                    else:
                        for qualification in data:
                            for counter, employee_id in enumerate(data[qualification][2]):
                                data[qualification][2][counter] = self.get_list(self.employee, entry_id=employee_id)
                                data[qualification][2][counter].append(employee_id)

                elif dict_name is self.certificate:
                    if entry_id is not None:

                        for counter, employee_id in enumerate(data[3]):
                            data[3][counter] =  self.get_list(self.employee, entry_id=employee_id)
                            data[3][counter].append(employee_id)

                    else:
                        for certificate in data:
                            for counter, employee_id in enumerate(data[certificate][3]):
                                data[certificate][3][counter] = self.get_list(self.employee, entry_id=employee_id)
                                data[certificate][3][counter].append(employee_id)
                else:
                    raise KeyError("dict_name was not a class object(Line 263 Database.py)")
                    #return None

        # Notice that a copy by value is returned
        return data

    # Increases max_id by one and returns new value
    def raise_max_id(self, dict_name):
        # Get employees dictionary entry
        employees = self.main_data.get(dict_name)
        if employees:
            max_id = employees.get("Max-ID")
            if max_id:
                max_id = int(max_id) + 1
                employees["Max-ID"] = str(max_id)
                return str(max_id)
        raise KeyError

    # Method changes count and returns it
    # If amount = 0 only returns the count
    def change_count(self, list_name, amount=0):
        employees = self.main_data.get(list_name)
        if employees:
            count = employees.get("Count")
            if count:
                count = int(count) + amount
                employees["Count"] = str(count)
                return str(count)
        raise KeyError

    '''# General employee methods #'''

    # Method to add new employee | it is assumed that the employee has no trainings, qualifications and certificates
    def add_employee(self, new_employee):
        try:
            employee_id = self.raise_max_id(self.employee)
            employee_list = self.__get_list(self.employee)
            self.change_count(self.employee, amount=1)

            # Append 3 empty list for trainings, qualifications and certificates
            for _ in range(0, 3):
                new_employee.append([])

            employee_list[employee_id] = new_employee
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return employee_id

    def delete_employee(self, employee_id):
        try:
            employee_list = self.__get_list(self.employee)

            # Get a Value copy of the list because delete_employee_from_training() will change the list
            # which would manipulate the for loop
            employee = copy.deepcopy(self.__get_list(self.employee, entry_id=employee_id))

            # Delete employee from training
            for training in employee[4]:
                self.delete_employee_from_training(employee_id, training[0])

            # Delete employee from qualifications
            for qualification_id in employee[5]:
                self.remove_employee_from_qualification(qualification_id, employee_id)

            # Delete employee from certificates
            for certificate_id in employee[6]:
                self.remove_employee_from_certificate(certificate_id, employee_id)

            employee_list.pop(employee_id)
            self.change_count(self.employee, amount=-1)
            self.write_json_file()

        except KeyError:
            return False
        else:
            return True

    # This function only edits the employee properties not the references to other objects
    def edit_employee(self, employee_id, changed_employee):
        try:
            employee_list = self.__get_list(self.employee)

            for i in range(0, 4):
                employee_list[employee_id][i] = changed_employee[i]

            self.write_json_file()

        except KeyError:
            return False
        else:
            return True

    def get_empty_employee_array(self):
        array = []
        for i in range(0, 4):
            array.append('')
        return array

    '''# Employee Training methods #'''

    # Adds a training to one employee and checks if it was successful finished
    def add_training_to_employee(self, employee_id, training_id, employee_participation_status):
        try:
            employee = self.__get_list(self.employee, entry_id=employee_id)
            employee[4].append([training_id, employee_participation_status])

            training = self.__get_list(self.training, entry_id=training_id)
            training[-1].append([employee_id, employee_participation_status])

            # Check if participation status is successful
            # If so add qualification and certificate to employee
            if employee_participation_status.lower() in "erfolgreich beendet":
                for qualification_id in training[-2]:
                    self.add_qualification_to_employee(qualification_id, employee_id)
                if training[-3] is not None:
                    self.add_certificate_to_employee(training[-3], employee_id)

            # Add 1 to participation count if employee has not already finished the training
            if employee_participation_status in self.get_participation_status_array(not_finished=True):
                self.change_participation_count(1)

            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    # Deletes an employee from training by setting participation status to storniert
    # but keeps the entry in employee and training for later reference
    # It also reduces participation count by 1
    def delete_employee_from_training(self, employee_id, training_id):
        try:
            has_not_finished_training = False
            finished_training_states = self.get_participation_status_array(finished=True)
            employee_list = self.__get_list(self.employee, entry_id=employee_id)
            for training in employee_list[4]:
                if training_id in training:
                    if training[1].lower() not in finished_training_states:
                        has_not_finished_training = True
                        training[1] = "storniert"

            # TODO Temporary solution for employee delete -> deletes employee completely from the database instead of setting it to "storniert"
            training_list = self.__get_list(self.training, entry_id=training_id)
            for employee in training_list[-1]:
                if employee_id in employee:
                    #employee[-1] = "storniert"
                    training_list[-1].remove(employee)

            # Subtract 1 from participation count if employee has not finished the training
            if has_not_finished_training is True:
                self.change_participation_count(-1)

            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    # Deletes a training for all employees
    def delete_training_from_employees(self, training_id):
        try:
            employee_list = self.__get_list(self.employee)
            for entry in employee_list:
                for training in employee_list[entry][4]:
                    if training_id in training:
                        self.change_participation_count(-1)
                        employee_list[entry][4].remove(training)

        except (KeyError, ValueError):
            return False
        else:
            return True

    # Changes the participation count in training or returns the current value if amount is 0
    def change_participation_count(self, amount=0):
        try:
            training = self.main_data.get(self.training)
            count = training.get("Participation_count")
            count = int(count) + amount
            training["Participation_count"] = str(count)
            return str(count)
        except (KeyError, ValueError):
            return None

    def get_employee_participation_status(self, employee_id, training_id):
        try:
            training = self.__get_list(self.training, entry_id=training_id)
            for employee in training[-1]:
                if employee[0] == employee_id:
                    return employee[1]

        except (KeyError, ValueError):
            return None

    '''# General training methods #'''

    # Adds new training
    def add_training(self, new_training):
        try:
            training_id = self.raise_max_id(self.training)
            training_list = self.__get_list(self.training)
            self.change_count(self.training, amount=1)

            # Append certificate, qualification and employee
            new_training.append(None) # None because entry is no list -> there can only be one certificate from a training
            new_training.append([])
            new_training.append([])

            training_list[training_id] = new_training
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        return training_id

    # Deletes training and all its connections to employees
    def delete_training(self, training_id):
        try:
            employee_list = self.__get_list(self.training)
            employee_list.pop(training_id)
            self.delete_training_from_employees(training_id)
            self.change_count(self.training, amount=-1)
            self.write_json_file()
        except KeyError:
            return False
        else:
            return True

    # This function should only be used to change title, description, dates and max-min employees of training
    # To change employees, qualifications and certificates regarded to this training use functions in
    # Employee Training methods, Qualification Training methods, Certificates Training methods
    def edit_training(self, training_id, changed_training):
        try:
            training_list = self.__get_list(self.training)
            for i in range(0, 6):
                training_list[training_id][i] = changed_training[i]
            self.write_json_file()

        except (KeyError, ValueError):
            return False
        else:
            return True

    def get_empty_training_array(self):
        array = []
        for i in range(0, 6):
            array.append('')
        return array

    def get_participation_status_array(self, finished=False, not_finished=False):
        if finished is True:
            return ["storniert", "abgebrochen", "nicht erfolgreich beendet", "erfolgreich beendet"]
        elif not_finished is True:
            return ["angemeldet", "nimmt teil"]
        else:
            return ["angemeldet", "nimmt teil", "storniert", "abgebrochen", "nicht erfolgreich beendet", "erfolgreich beendet"]

    ''' # Qualification Training methods # '''

    def add_qualification_to_training(self, qualification_id, training_id):
        try:
            training = self.__get_list(self.training, entry_id=training_id)

            # Add to qualification array(second last entry)
            training[-2].append(qualification_id)
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    def remove_qualification_from_training(self, qualification_id, training_id):
        try:
            training = self.__get_list(self.training, entry_id=training_id)

            # Add if to qualification array(second last entry)
            training[-2].remove(qualification_id)
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    # This method is called by delete_qualification | Also not sure if we need this method
    def remove_qualification_from_all_trainings(self, qualification_id):
        try:
            training_list = self.__get_list(self.training)
            for training in training_list:
                if qualification_id in training_list[training][-2]:
                    training_list[training][-2].remove(qualification_id)

        except (KeyError, ValueError):
            return False
        else:
            return True

    ''' # Qualification employee methods # '''

    def add_qualification_to_employee(self, qualification_id, employee_id):
        try:
            employee = self.__get_list(self.employee, entry_id=employee_id)

            # Add qualification to employee qualification array(second last entry)
            employee[-2].append(qualification_id)

            # Add employee to qualification
            qualification = self.__get_list(self.qualification, entry_id=qualification_id)
            qualification[2].append(employee_id)

            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    def remove_employee_from_qualification(self, qualification_id, employee_id):
        try:
            employee = self.__get_list(self.employee, entry_id=employee_id)

            # Remove qualification from employee qualification array(second last entry)
            employee[-2].remove(qualification_id)

            # Remove employee from qualification
            qualification = self.__get_list(self.qualification, entry_id=qualification_id)
            qualification[2].remove(employee_id)

            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    '''# General qualifications methods #'''

    # This method assumes that new_qualification only has title and description in list form
    def add_qualification(self, new_qualification):
        try:
            qualification_id = self.raise_max_id(self.qualification)
            qualification_list = self.__get_list(self.qualification)
            self.change_count(self.qualification, amount=1)

            # Add array for employee id
            new_qualification.append([])
            qualification_list[qualification_id] = new_qualification
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return qualification_id

    # This method assumes that an employee keeps his qualification even tho it was deleted
    # Not sure if this method is necessary
    def delete_qualification(self, qualification_id):
        try:
            qualification_list = self.__get_list(self.qualification)
            qualification_list.pop(qualification_id)
            self.change_count(self.qualification, -1)
            self.remove_qualification_from_all_trainings(qualification_id)
            self.write_json_file()

        except (KeyError, ValueError):
            return False
        else:
            return True

    # This function should only be used to change description and title of qualification
    # To change employees regarded to this qualification use functions in 'Qualification employee methods'
    def edit_qualification(self, qualification_id, changed_qualification):
        try:
            qualification_list = self.__get_list(self.qualification)
            # Only change first two entries of array this way relations stay untouched
            for i in range(0, 2):
                qualification_list[qualification_id][i] = changed_qualification[i]
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    '''# Certificates Training methods #'''

    def add_certificate_to_training(self, certificate_id, training_id):
        try:
            training = self.__get_list(self.training, entry_id=training_id)

            # Override third last entry with certificate id
            training[-3] = certificate_id
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    def remove_certificate_from_training(self, certificate_id, training_id):
        try:
            training = self.__get_list(self.training, entry_id=training_id)

            # Prevent accidental overrides by checking first
            if certificate_id == training[-3]:
                training[-3] = None
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    # This method is called by delete_certificate | Also not sure if we need this method
    def remove_certificate_from_all_trainings(self, certificate_id):
        try:
            training_list = self.__get_list(self.training)
            for training in training_list:
                if certificate_id is training_list[training][-3]:
                    training_list[training][-3] = None

        except (KeyError, ValueError):
            return False
        else:
            return True

    '''# Certificate Employee methods #'''

    def add_certificate_to_employee(self, certificate_id, employee_id):
        try:
            employee = self.__get_list(self.employee, entry_id=employee_id)

            # Add certificate to employee certificate array(last entry)
            employee[-1].append(certificate_id)

            # Add employee to certificate
            certificate = self.__get_list(self.certificate, entry_id=certificate_id)
            certificate[-1].append(employee_id)

            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    def remove_employee_from_certificate(self, certificate_id, employee_id):
        try:
            employee = self.__get_list(self.employee, entry_id=employee_id)

            # Add certificate to employee certificate array(last entry)
            employee[-1].remove(certificate_id)

            # Add employee to qualification
            certificate = self.__get_list(self.certificate, entry_id=certificate_id)
            certificate[-1].remove(employee_id)

            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    ''' # General certificate methods #'''

    # This method assumes that new_certificate only has title and description in list form
    def add_certificate(self, new_certificate):
        try:
            certificate_id = self.raise_max_id(self.certificate)
            certificate_list = self.__get_list(self.certificate)
            self.change_count(self.certificate, 1)

            # Add array for employee id
            new_certificate.append([])
            certificate_list[certificate_id] = new_certificate
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return certificate_id

    # Deletes certificate itself and removes it from all trainings
    def delete_certificate(self, certificate_id):
        try:
            certificate_list = self.__get_list(self.certificate)
            certificate_list.pop(certificate_id)
            self.change_count(self.certificate, -1)
            # TODO BUG wegen löschen
            self.remove_certificate_from_all_trainings(certificate_id)
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True

    # This function should only be used to change description and title of certificate
    # To change employees regarded to this qualification use functions in 'certificate employee methods'
    def edit_certificate(self, certificate_id, changed_certificate):
        try:
            certificate_list = self.__get_list(self.certificate)
            # Only change first two entries of array this way relations stay untouched
            for i in range(0, 3):
                certificate_list[certificate_id][i] = changed_certificate[i]
            self.write_json_file()
        except (KeyError, ValueError):
            return False
        else:
            return True