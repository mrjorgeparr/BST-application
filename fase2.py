# -*- coding: utf-8 -*-

from binarysearchtree import BinarySearchTree
import csv  # read files csv, tsv
import os.path  # to work with files and directory https://docs.python.org/3/library/os.path.html
import queue  # package implementes a queueu, https://docs.python.org/3/library/queue.html
import re  # working with regular expressions
from Queue import Queue  # to be used in level order traversals troughout the script


def checkFormatHour(time):
    """checks if the time follows the format hh:dd"""
    pattern = re.compile(r'\d{1,2}:\d{2}')  # busca la palabra foo

    if pattern.match(time):
        data = time.split(':')
        hour = int(data[0])
        minute = int(data[1])
        if hour in range(8, 20) and minute in range(0, 60, 5):
            return True

    return False


# number of all possible appointments for one day
NUM_APPOINTMENTS = 144


class Patient:
    """Class to represent a Patient"""

    def __init__(self, name, year, covid, vaccine, appointment=None):
        self.name = name
        self.year = year
        self.covid = covid
        self.vaccine = vaccine
        self.appointment = appointment  # string with format hour:minute

    def setAppointment(self, time):
        """gets a string with format hour:minute"""
        self.appointment = time

    def __str__(self):
        return self.name + '\t' + str(self.year) + '\t' + str(self.covid) + '\t' + str(
            self.vaccine) + '\t appointment:' + str(self.appointment)

    def __eq__(self, other):
        return other != None and self.name == other.name


class HealthCenter2(BinarySearchTree):
    """Class to represent a Health Center. This class is a subclass of a binary search tree to 
    achive a better temporal complexity of its algorithms for 
    searching, inserting o removing a patient (or an appointment)"""

    def __init__(self, filetsv=None, orderByName=True):
        """
        This constructor allows to create an object instance of HealthCenter2. 
        It takes two parameters:
        - filetsv: a file csv with the information about the patients whe belong to this health center
        - orderByName: if it is True, it means that the patients should be sorted by their name in the binary search tree,
        however, if is is False, it means that the patients should be sorted according their appointments
        """

        # Call to the constructor of the super class, BinarySearchTree.
        # This constructor only define the root to None
        super(HealthCenter2, self).__init__()

        # Now we
        if filetsv is None or not os.path.isfile(filetsv):
            # If the file does not exist, we create an empty tree (health center without patients)
            self.name = ''
            # print('File does not exist ',filetsv)
        else:
            # order='by appointment'
            # if orderByName:
            #    order='by name'
            # print('\n\nloading patients from {}. The order is {}\n\n'.format(filetsv,order))

            self.name = filetsv[filetsv.rindex('/') + 1:].replace('.tsv', '')
            # print('The name of the health center is {}\n\n'.format(self.name))

            fichero = open(filetsv)
            lines = csv.reader(fichero, delimiter="\t")

            for row in lines:
                # print(row)
                name = row[0]  # nombre
                year = int(row[1])  # año nacimiento
                covid = False
                if int(row[2]) == 1:  # covid:0 o 1
                    covid = True
                vaccine = int(row[3])  # número de dosis
                try:
                    appointment = row[4]
                    if checkFormatHour(appointment) == False:
                        # print(appointment, ' is not a right time (h:minute)')
                        appointment = None

                except:
                    appointment = None

                objPatient = Patient(name, year, covid, vaccine, appointment)
                # name is the key, and objPatient the eleme
                if orderByName:
                    self.insert(name, objPatient)
                elif orderByName == False and appointment:
                    # we only save if the appointement has a right format
                    self.insert(appointment, objPatient)

            fichero.close()

    def searchPatients(self, year=2021, covid=None, vaccine=None):
        """return a new object of type HealthCenter 2 with the patients who
        satisfy the criteria of the search (parameters). 
        The function has to visit all patients, so the search must follow a level traverse of the tree.
        If you use a inorder traverse, the resulting tree should be a list!!!"""
        """Regarding complexity:
        The first part is the error handling routines. They are just if blocks with constant time operations 
        inside them, and thus the complexity of that part is also constant.
        Then we find an if block, that handles the base case, i.e, when year = 2021, covid is None and vaccine is None.
        Inside this block, there's only one statement to return the invoking healthcenter, as every patient matches those 
        filters.
        Afterwards we find the general case, in which we iterate through the tree, using a level order traversal, inside 
        this main loop, the only non-constant-time statement is the call to the insert function, which on the slides of the
        course is described to have log2(n), complexity, and therefore, this part has complexity n*log2(n), which since it's
        the most complex case of the three, it's the overall complexity of the function.
        - Best case: when year = 2021, covid is None and vaccine is None. In this case, the complexity
        is constant as there's an if block designed to handle this case, in which we directly return
        the invoking health center.
        - Worst case: the worst case is when the BST, has degenerated into a list. In this case insertion is linear
        and since we call the insert function inside a while loop it has complexity O(n^2)
        """
        result = HealthCenter2()

        if self._root is None:
            print("Healthcenter is emtpy!")
            return result
        if type(year) is not int:
            try:
                # we try typecasting in case it was passed as a string
                year = int(year)
            except ValueError:
                # in case we cannot type cast we return the emtpy heatlhcenter
                print("Error: invalid type of input variable 'year'")
                return result
        # in the case, the user passed two arguments and the second one was meant to be vaccine and not Covid
        if type(covid) is int and vaccine is None:
            vaccine = covid
            covid = None

        if type(covid) is str and vaccine is None:
            try:
                """we try typecasting, in case the user wanted to introduce values for year and vaccine 
                and the second one was introduced as a string"""
                aux = int(covid)
                vaccine = aux
                covid = None
            except ValueError:
                print("Error: invalid type of input variable 'covid'")
                return result
        # ------------------------------------------
        if covid is not None and type(covid) is not bool:
            print("Error: invalid type of input variable 'covid'")
            return result

        if type(vaccine) is not int and vaccine is not None:
            try:
                # we try typecasting in case it was passed as a string
                vaccine = int(vaccine)
            except ValueError:
                # in case we cannot type cast we return the empty healthcenter
                print("Error: invalid type of input variable 'vaccine'")
                return result

        # Number of vaccine doses cannot exceed 2
        if vaccine is not None:
            if vaccine > 2 or vaccine < 0:
                print("Error: invalid number of doses")
                return result
        # the oldest living human in Spain in 2020, was María Branyas, born in 1907
        if year > 2021 or year < 1907:
            print("There is no one alive in Spain of that age!")
            return result

        if year == 2021 and covid is None and vaccine is None:
            return self  # base case, return directly self as all patients satisfy

        if self._root is None:
            print('tree is empty')
        else:
            q = Queue()
            q.put(self._root)  # enqueue: we save the root
            while q.empty() is False:
                current = q.get()  # dequeue
                element = current.elem  # this is the part where we perform the checking
                if element.year <= year and (covid is None or element.covid == covid) and (
                        vaccine is None or element.vaccine == vaccine):
                    result.insert(current.key, element)
                if current.left is not None:
                    q.put(current.left)
                if current.right is not None:
                    q.put(current.right)
            return result

    def vaccine(self, name, vaccinated):
        """This functions simulates the vaccination of a patient whose
        name is name. It returns True is the patient is vaccinated and False eoc"""
        """Regarding complexity: in the case of  O(n)?
        this is a very simple function, on the code of the function we have
        linear complexity, but we must analyze the complexity of the functions we called inside, 
        _removeNode,find and insert.
        In removeNode, the worst case in terms of complexity is where the node has two children, inside the else
        block regarding this case, we find a while loop, with no nested calls, so the complexity of this function
        is linear.
        Regarding the find function, we know that the worst case scenario is when the binary tree has degenerated 
        into a list, in said case, the complexity is linear
        About the insert function, we know that since for every comparison on a balanced tree, the search space
        gets divided over two every iteration, but if the tree has degenerated into a list, where the complexity
        would be linear as well.
        Since all of the functions that are called inside the if blocks are linear, we can conclude that the complexity
        of the function vaccine is also linear.
        The best case is when the node does not exist, in this case the complexity is linear but  there's only one extra
        operation to be performed, which is of constant time.
        The worst case is the last one, as it calls print, _removeNode, insert and returns a value, and in this
        last two the complexity is linear."""
        # error handling
        if type(name) is not str:
            print("Error: invalid type of input variable 'name'")
            return False
        if type(vaccinated) is not HealthCenter2:
            print("Error: invalid type of input variable 'vaccinated'")
            return False
        if name.isnumeric() is True:
            print("Error: expected non-numeric string in variable 'name'")
            return False
        #The first letter of the input name and/or surname may not be in upper case
        tname = ' '.join(n.capitalize() for n in name.split(" "))
        node = self.find(tname)
        if node is None:
            print("\nPatient was not in Healthcenter")
            return False
        else:
            element = node.elem  # now we check the number of vaccine doses
            if element.vaccine == 0:
                element.vaccine += 1  # we update the number of doses
                return True
            elif element.vaccine == 1:
                element.vaccine += 1  # we update the number of doses
                self._removeNode(node)
                vaccinated.insert(node.key, node.elem)
                return True
            else:
                print("\nPatient had been vaccinated previously")
                self._removeNode(node)  # we remove it from the invoking health center and add it to vaccinated
                vaccinated.insert(node.key, node.elem)
                return False

    @staticmethod
    def tconversion(time):
        t = time.split(":")
        return int(t[0]) * 60 + int(t[1])

    @staticmethod
    def tbackwards_conversion(time):
        hours = time // 60
        minutes = time - hours * 60
        if minutes < 10:
            return str(hours) + ":" + "0" + str(minutes)
        if hours < 10:
            if minutes >= 10:
                return  str(hours) + ":" + str(minutes)
        else:
            return str(hours) + ":" + str(minutes)

    @staticmethod
    def update(n, i):
        n += 1
        if n % 2 == 1 and n != 1:
            i += 1
        return n, i

    def makeAppointment(self, name, time, schedule):
        """This functions makes an appointment 
        for the patient whose name is name. It functions returns True is the appointment 
        is created and False eoc """
        """Regarding complexity: O(n^2)
        The first thing we do in the function is check for invalid input, which may be because the input variables are
        of invalid type or because name is a numeric string, if some error occurs we print it on screen and return false
        the big O, of this part is constant as we just perform simple if and possibly print and return operations.
        
        Afterwards we check if the invoking tree, where the patient is supposed to be located at is empty or not, we 
        also check if the maximum number of appointments has been met, in any of these cases print a message on screen
        and return False, this part also has constant complexity, which is the best case.
        
        Assuming no errors, and that none of the two exceptions explained above has occurred, we use the method .find
        to check whether the patient is in fact in the invoking center or not, this has a complexity of O(log n), if 
        we don't find it we print it on screen, if it's found there are two different cases we must consider.
        
        If the input patient has already received two doses of tha vaccine, we print a message on screen and return 
        False, this is of constant time.
        
        In any other case, we must check first if the format of the input time is valid, and search for it on the 
        schedule object, if it's available, we assign it to the patient ant return True, if it's not available we enter
        a loop to find the best option available, i.e, we search for time - 5, time + 5, time - 10, time + 10, time -15, 
        time + 15 and so on. When found, we must also perform an insert operation, to the schedule center. This is the 
        worst case in terms of complexity as we call the search function inside a loop and thus the complexity of this 
        part and of the function is O(n*log n).
        
        The worst case is when the BST has degenerated into a list, case in which the search, insert and find operations
        case in which the complexity of these methods goes up to O(n).
        """
        # error handling
        if type(name) is not str:
            print("Error: expected string in input variable 'name', got ", type(name))
            return False
        if type(schedule) is not HealthCenter2:
            print("Error: expected HealthCenter2 as 'schedule', got ", type(schedule))
            return False
        if type(time) is not str:
            print("Error: expected string in input variable 'time', got", type(time))
            return False
        if name.isnumeric() is True:
            print("Error: expected non-numeric string in input variable 'name'")
            return False
        if self._root is None:
            print("Tree is empty!")
            return False
        size = schedule.size()
        if size >= NUM_APPOINTMENTS:
            print("Full number of appointments")
            return False
        # the first letters of name and surname, may not be in Upper case
        tname = ' '.join(n.capitalize() for n in name.split(" "))
        node = self.find(tname)
        if node is None: # the first letters of name and surname, may not be in Upper case
            print("\nPatient was not in Healthcenter")
            return False
        else:
            element = node.elem
            if element.vaccine == 2:  # the patient has been found and has already received both doses
                print("\nPatient has already been vaccinated")
                return False
            else:
                if checkFormatHour(time) is False:  # check if time format is valid
                    # error, invalid format
                    print("\nInvalid format")
                    return False
                aux = HealthCenter2.tconversion(time)
                time = HealthCenter2.tbackwards_conversion(aux)
                is_taken = schedule.search(time)  # search has complexity O(log n)
                if not is_taken:  # if the time was not found in any patient then it's free
                    node.elem.appointment = time
                    schedule.insert(time, node)
                    return True
                else:  # if the time is not in schedule
                    n = 1
                    i = 1
                    found = False
                    while not found:  # we rule out each of the best options in hierarchical order, until one is free
                        """(-1)**n)*5*i, is a general formula to get the difference between the time and the best 
                        alternative that should be tried on an iteration"""
                        print(((-1)**n)*5*i)
                        time_to_search = HealthCenter2.tbackwards_conversion(
                            HealthCenter2.tconversion(time) + ((-1) ** n)* 5 * i)
                        print("tiempo a buscar: ",time_to_search)
                        split = time_to_search.split(":")
                        if int(split[0]) < 8 or int(split[0]) > 20:  # those hour ranges are not valid
                            n, i = HealthCenter2.update(n, i)
                            continue    #if time_to_search is not inside the valid bounds, get the next best option
                        to_search = schedule.search(time_to_search)
                        time_to_search2 = time_to_search
                        if to_search is False:  #i.e, time_to_search is available
                            hour_min = time_to_search.split(":")
                            if int(hour_min[0]) < 10:
                                time_to_search2 = "0" + time_to_search
                            print(time_to_search)
                            node.elem.appointment = time_to_search2
                            schedule.insert(time_to_search, node)
                            return True
                        else:
                            n, i = HealthCenter2.update(n, i)


if __name__ == '__main__':
    ###Testing the constructor. Creating a health center where patients are sorted by name
    o = HealthCenter2('data/LosFrailes2.tsv')
    o.draw()
    print()
    # Tests that work
    # u = o.searchPatients()
    u2 = o.searchPatients(1990)
    u2.draw()
    print()
    # schedule = HealthCenter2('data/LosFrailesCitas.tsv', False)
    oInput = HealthCenter2('data/LosFrailes2.tsv')
    expected = HealthCenter2('data/LosFrailes2.tsv')

    schedule = HealthCenter2('data/LosFrailesCitas.tsv', False)
    schedule_exp = HealthCenter2('data/LosFracilesCitasLosada8-15.tsv', False)
    schedule.draw(False)
    name = 'Losada'
    time = '08:00'
    result = oInput.makeAppointment(name, time, schedule)

    """
    print('Patients who were born in or before than 1990, had covid and did not get any vaccine')
    result=o.searchPatients(1990, True,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990, did not have covid and did not get any vaccine')
    result=o.searchPatients(1990, False,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and got one dosage')
    result=o.searchPatients(1990, None,1)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and had covid')
    result=o.searchPatients(1990, True)
    result.draw()
    print()


    ###Testing the constructor. Creating a health center where patients are sorted by name
    schedule=HealthCenter2('data/LosFrailesCitas.tsv',False)
    schedule.draw(False)
    print()
    
    

    o.makeAppointment("Perez","8:00",schedule)
    o.makeAppointment("Losada","19:55",schedule)
    o.makeAppointment("Jaen","16:00",schedule)
    o.makeAppointment("Perez","16:00",schedule)
    o.makeAppointment("Jaen","16:00",schedule)

    o.makeAppointment("Losada","15:45",schedule)
    o.makeAppointment("Jaen","8:00",schedule)

    o.makeAppointment("Abad","8:00",schedule)
    o.makeAppointment("Omar","15:45",schedule)
    
    
    schedule.draw(False)

    vaccinated=HealthCenter2('data/vaccinated.tsv')
    vaccinated.draw(False)

    name='Ainoza'  #doest no exist
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)

    name='Abad'   #0 dosages
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    
   

    name='Font' #with one dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    
    name='Omar' #with two dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    """

def rearrange(num):
    return int("".join(sorted([x for x in str(num)], reverse = True)))

print(rearrange(67348723489723))

from itertools import permutations

from itertools import permutations as pt
def middle_permutation(string):
    if len(string) < 2 or len(string) > 26: return " "
    p = pt(string)
    p = list(p)
    mid = len(p)//2 - 1
    print(p)
    return "".join(p[mid])
# print(middle_permutation("abc"))
import math
def manhattan_distance(c1, c2):
    return int(sum([abs(c1[i] - c2[i]) for i in range(len(c1))]))


