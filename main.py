# Important library imports
import re
import random
import string
import time
import csv


class Car():
    """
       Represents a car with attributes like registration number, ticket, entry and exit times,
       parking fee, and parking space. Provides methods for ticket generation, validation, and
       calculating parking fees.
    """
    valid_regNo = r'^[A-Z]{2}\d{2} [A-Z]{3}$'  # Uses regex to write the proper UK registration number format

    def __init__(self, regNo, entry_time, parking_space):
        self.regNo = regNo
        self.ticket = None  # Generated when a car enters the car park and not when a car instance is created
        self.entry_time = entry_time
        self.exit_time = None  # exit time not known until a car leaves the car park
        self.parking_fee = None
        self.parking_space = parking_space

    def validation(self):
        return re.match(self.valid_regNo, self.regNo) is not None

    def gen_ticket(self):
        # This function generates a ticket number by adding random letters & numbers to the regNo
        if self.ticket is None:  # Implies that the ticket is yet to be generated
            random_ticket = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
            self.ticket = f'{random_ticket}{self.regNo}'.replace(" ", "")

    def calc_parking_fee(self, rate):
        if self.entry_time and self.exit_time:
            # Converts time into a Unix Timestamp which is a single numeric value rep time in seconds
            entry_time = time.mktime(time.strptime(self.entry_time, "%Y-%m-%d %H:%M:%S"))
            exit_time = time.mktime(time.strptime(self.exit_time, "%Y-%m-%d %H:%M:%S"))
            parking_time = (exit_time - entry_time) / 3600  # determine number of hours a car was parked

            if parking_time <= 24:
                self.parking_fee = round(parking_time * rate, 2)  # Hourly rate is 2
            else:
                # 20 pound fee if car is parked longer than 24 hours
                self.parking_fee = 20.0 + round((parking_time - 24) * rate, 2)
            return self.parking_fee

        return 0.0  # If a car stays in the car park for an extremely short time ie seconds


class CarPark():
    """
       Manages a car park with functionalities to enter and exit cars, query by ticket,
       and manage parking spaces. Includes methods to save and load parking records to/from a CSV file.
    """
    def __init__(self, parking_spaces, rate):
        self.parking_spaces = [str(i) for i in range(1, parking_spaces + 1)]  # Counts the total number of parking spaces.
        self.cars = []
        self.rate = rate

    def enter_carPark(self, regNo):
        if len(self.parking_spaces) == 0:  # Checks if they're any parking spaces left
            return 'Sorry we are all out of parking spaces :('

        for car in self.cars:  # Checks if the car is already parked, cannot park same car twice if it has not exited
            if car.regNo == regNo and not car.exit_time:
                return 'This car is already parked'

        car_instance = Car(regNo, time.strftime("%Y-%m-%d %H:%M:%S"), None)
        if not car_instance.validation():
            return 'Invalid registration number'

        parking_space = random.choice(self.parking_spaces)  # assigns parking spaces randomly
        self.parking_spaces.remove(parking_space)
        car_instance.parking_space = parking_space
        car_instance.gen_ticket()
        self.cars.append(car_instance)
        return car_instance

    def exit_carPark(self, regNo):
        for car_instance in self.cars:
            if car_instance.regNo == regNo and not car_instance.exit_time:  # checks if the Reg No matches the record and if exit time is None meaning th car has not exited the car park
                car_instance.exit_time = time.strftime("%Y-%m-%d %H:%M:%S")
                parking_fee = car_instance.calc_parking_fee(self.rate)
                self.parking_spaces.append(car_instance.parking_space)
                self.cars.remove(car_instance)  # Remove the car from the car park list as it has exited
                return car_instance

        return "Vehicle not found or already exited"

    def query_by_ticket(self, ticket):
        for car in self.cars:
            if car.ticket == ticket:
                return car
        return 'Vehicle not found or already exited'

    def csv_save(self,filename):  # This code is used to save data into the csv file with the specific columns indicated
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['Registration Number', 'Ticket Number', 'Parking Space', 'Entry Time', 'Exit Time', 'Parking Fee'])
            for car in self.cars:
                writer.writerow(
                    [car.regNo, car.ticket, car.parking_space, car.entry_time, car.exit_time, car.parking_fee])

    def load_records(self, filename):  # This loads the records of the csv file and updates accordingly
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    car_instance = Car(row['Registration Number'], row['Entry Time'], row['Parking Space'])
                    car_instance.ticket = row['Ticket Number']
                    car_instance.exit_time = row['Exit Time']
                    car_instance.parking_fee = row['Parking Fee']
                    self.cars.append(car_instance)
                    if car_instance.parking_space in self.parking_spaces:
                        self.parking_spaces.remove(car_instance.parking_space)

        except FileNotFoundError:
            pass # Ignore if the file does not exist, as this means there are no records to load.

