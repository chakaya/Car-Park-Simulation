from main import Car, CarPark
import sys

class Menu():
    """
        Menu class for the command-line interface of the Car Park Simulator.
        It handles user interactions for car park operations like entering, exiting,
        viewing available spaces, querying records, and exiting the program.
    """
    def __init__(self):
        self.car_park = None

    #Function to initialize Carpark class and load reacords.csv
    def start(self):
        self.car_park = CarPark(parking_spaces = 5, rate = 2)
        self.car_park.load_records('records.csv')

        #creating the display menu and handling the user's choice
        while True:
            self.display_menu()
            choice = input('Welcome! What would you like to do?')

            if choice == '1':
                self.enter()
            elif choice == '2':
                self.exit()
            elif choice == '3':
                self.parkingspaces()
            elif choice == '4':
                self.query_record()
            elif choice == '5':
                self.quit()
                break

    def display_menu(self):
        print('Car Park Menu')
        print('1. Enter the car park')
        print('2. Exit the car park')
        print('3. View available parking spaces')
        print('4. Query parking record by the ticket number')
        print('5. Quit')

    #Entering, exit, query and quit using logic from main.py
    def enter(self):
        reg_No = input ('Enter your registration number(Valid reg no example AB12 XYZ): ').upper()#changes all letters to uppercase
        car_instance = self.car_park.enter_carPark(reg_No)
        if car_instance:
            if isinstance(car_instance, str):
                print(car_instance)
            else:
                print(f'Vehicle with registration number {reg_No} has entered the car park')
                print(f'Entry time: {car_instance.entry_time}')
                print(f'Assigned parking space: {car_instance.parking_space} ')
                print(f'Ticket number: {car_instance.ticket}')
                if car_instance.exit_time is None: #checks if a car has exited or not
                    print(f'Exit time: Parking...')
                else:
                    print(f'Exit time: {car_instance.exit_time}')
                print(f'Available parking spaces: {len(self.car_park.parking_spaces)}')

    def exit(self):
        reg_No = input('Enter your registration number(Valid reg no example AB12 XYZ): ').upper()
        car_instance = self.car_park.exit_carPark(reg_No)
        if car_instance:
            if isinstance(car_instance, str):
                print(car_instance)
            else:
                print(f'Vehicle with registration number {reg_No} has exited the car park')
                print(f'Entry time: {car_instance.entry_time}')
                print(f'Parking fee: £{car_instance.parking_fee}')
                print(f'Exit time: {car_instance.exit_time}')
                print(f'Assigned parking space: {car_instance.parking_space}')
                print(f'Available parking spaces: {len(self.car_park.parking_spaces)}')

    def parkingspaces(self):
        print(f'Available parking spaces: {len(self.car_park.parking_spaces)}')

    def query_record(self):
        ticket_number = input('Enter your ticket number: ').upper()
        car_instance = self.car_park.query_by_ticket(ticket_number)
        if car_instance:
            if isinstance(car_instance, str):
                print(car_instance)
            else:
                print(f'Vehicle with ticket number: {ticket_number}')
                print(f'Registration number: {car_instance.regNo}')
                print(f'Entry time: {car_instance.entry_time}')
                print(f'Assigned parking space: {car_instance.parking_space} ')
                if car_instance.exit_time is None: #checks if the car has exited or not
                    print(f'Exit time: Parking...')
                else:
                    print(f'Exit time: {car_instance.exit_time}')
                if car_instance.parking_fee is None: #checks if the car has exited and received a parking fee or not
                    print(f'Parking fee: Still parking...')
                else:
                    print(f'Parking fee: £{car_instance.parking_fee}')
    #Saves all the records to the csv
    def quit(self):
        self.car_park.csv_save('records.csv')
        print('Exiting the program. Come again. Thank you!!')
        sys.exit()

if __name__ == '__main__':
    menu = Menu()
    menu.start()

