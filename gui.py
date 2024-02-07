import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from main import Car, CarPark

class GUI():
    """
        GUI class for Car Park Simulator. It creates the user interface for interacting with the
        CarPark system, allowing users to enter or exit the car park, view available parking spaces,
        and query parking records.
    """
    def __init__(self, master):
        self.master = master
        master.title('Car Park Simulator')

        #set window size
        master.geometry('900x450')

        #initialize CarPark class and load records.csv
        self.car_park = CarPark(parking_spaces = 5, rate = 2 )
        self.car_park.load_records('records.csv')

        #Styling parameters
        bg_color = '#ddeeff'
        button_color = '#aaccee'
        button_active_color = '#7799cc'
        label_font = ('Helvetica', 14, 'bold')
        button_font = ('Arial', 12)
        button_border_color = '#445566'
        button_relief = tk.RAISED
        button_borderwidth = 2
        master.configure(bg = bg_color)

        button_style = {'bg': button_color, 'activebackground': button_active_color,
                        'font': button_font, 'borderwidth': button_borderwidth, 'relief': button_relief}

        #Creating the necessary widgets
        self.label = tk.Label(master, text = 'Welcome! What would you like to do?\n (Hourly rate is £2) \n (Valid reg No example:AB12 XYZ)  ', font=label_font, bg=bg_color)
        self.label.pack(side = tk.TOP, fill= tk.X, padx= 10, pady= 5)

        # Frame for buttons
        self.button_frame = tk.Frame(master, bg= bg_color)
        self.button_frame.pack(side=tk.TOP, fill=tk.BOTH, padx= 10, pady= 10)

        self.enter_carpark = tk.Button(self.button_frame, text = 'Enter the Car Park', command = self.enter, bg=button_color, font=button_font)
        self.enter_carpark.grid(row= 0, column= 0, padx= 5, pady= 5)

        self.exit_carpark = tk.Button(self.button_frame, text= 'Exit the Car Park', command = self.exit, bg=button_color, font=button_font)
        self.exit_carpark.grid(row= 0, column= 1, padx= 5, pady= 5)

        self.view_parking = tk.Button(self.button_frame, text = 'View available parking spaces', command= self.parkingspaces, bg=button_color, font=button_font)
        self.view_parking.grid(row= 0, column= 2, padx= 5, pady= 5)

        self.query = tk.Button(self.button_frame, text= 'Query parking record by ticket number', command = self.query_record, bg=button_color, font=button_font)
        self.query.grid(row= 0, column= 3, padx= 5, pady= 5)

        self.quit_program = tk.Button(self.button_frame, text= 'Quit', command= self.quit, bg=button_color, font=button_font)
        self.quit_program.grid(row= 0, column= 4, padx= 5, pady= 5)

        #Displays text on the labels.
        self.status = tk.StringVar()
        self.status_label = tk.Label(master, textvariable= self.status, bg= bg_color, font= label_font)
        self.status_label.pack(padx=10, pady=(0, 5))

        #Enter car park widgets
        self.reg_no_label = tk.Label(master, text='Please enter your vehicle registration number', bg=bg_color, font=label_font)
        self.reg_no_entry = tk.Entry(master)
        self.submit_button = tk.Button(master, text = 'Enter', command= self.submit_reg_no, bg=bg_color, font=label_font)

        #Exit car park widgets
        self.exit_submit_button = tk.Button(master, text='Exit', command=self.exit_submit_reg_no, bg=bg_color, font=label_font)

        #Query record widgets
        self.ticket_label = tk.Label(master, text= 'Please enter your ticket number', bg=bg_color, font=label_font)
        self.ticket_entry = tk.Entry(master)
        self.query_button = tk.Button(master, text = 'Query', command= self.submit_ticket, bg=bg_color, font=label_font)

        #Applying styling to buttons
        self.enter_carpark.configure(**button_style)
        self.exit_carpark.configure(**button_style)
        self.view_parking.configure(**button_style)
        self.query.configure(**button_style)
        self.quit_program.configure(**button_style)
        self.submit_button.configure(**button_style)
        self.exit_submit_button.configure(**button_style)
        self.query_button.configure(**button_style)

    #Clears any initial input of the buttons
    def clear_status(self):
        self.status.set('')

    # Entering the car park, exiting, query records and quit using logic from main.py
    def enter(self):
        self.clear_status()
        self.reg_no_label.pack()
        self.reg_no_entry.pack()
        self.submit_button.pack()

    def submit_reg_no(self):
        reg_no = self.reg_no_entry.get().upper()
        if reg_no:
            car_instance = self.car_park.enter_carPark(reg_no)
            if isinstance(car_instance, str):
                self.status.set(car_instance)
            else:
                if car_instance.exit_time is None: #Checks if a car has exited or not
                    exit_time_str = 'Exit time: Parking...'
                else:
                    exit_time_str = f'Exit time: {car_instance.exit_time}'
                details = (f'Vehicle with registration number {reg_no} has entered the car park\n'
                           f'Entry time: {car_instance.entry_time}\n'
                           f'Assigned parking space: {car_instance.parking_space}\n'
                           f'Ticket number: {car_instance.ticket}\n'
                           f'{exit_time_str}\n'
                           f'Available parking spaces: {len(self.car_park.parking_spaces)}')
                self.status.set(details)

            self.reg_no_entry.delete(0, tk.END)

        self.reg_no_label.pack_forget()
        self.reg_no_entry.pack_forget()
        self.submit_button.pack_forget()

    def exit(self):
        self.clear_status()
        self.reg_no_label.pack()
        self.reg_no_entry.pack()
        self.exit_submit_button.pack()

    def exit_submit_reg_no(self):
        reg_no = self.reg_no_entry.get().upper()
        if reg_no:
            car_instance = self.car_park.exit_carPark(reg_no)
            if isinstance(car_instance, str):
                self.status.set(car_instance)
            else:
                details = (f'Vehicle with registration number {reg_no} has exited the car park\n'
                           f'Entry time: {car_instance.entry_time}\n'
                           f'Assigned parking space: {car_instance.parking_space}\n'
                           f'Ticket number: {car_instance.ticket}\n'
                           f'Parking fee: £{car_instance.parking_fee}\n'
                           f'Exit time: {car_instance.exit_time}\n'
                           f'Available parking spaces: {len(self.car_park.parking_spaces)}')
                self.status.set(details)

            self.reg_no_entry.delete(0, tk.END)

        self.reg_no_label.pack_forget()
        self.reg_no_entry.pack_forget()
        self.exit_submit_button.pack_forget()

    def parkingspaces(self):
        self.clear_status()
        self.status.set(f'Available parking spaces: {len(self.car_park.parking_spaces)}')

    def query_record(self):
        self.clear_status()
        self.ticket_label.pack()
        self.ticket_entry.pack()
        self.query_button.pack()

    def submit_ticket(self):
        ticket_number = self.ticket_entry.get().upper()
        if ticket_number:
            car_instance = self.car_park.query_by_ticket(ticket_number)
            if isinstance(car_instance, str):
                self.status.set(car_instance)
            else:
                if car_instance.exit_time is None: #Checks if a car has exited or not
                    exit_time_str = 'Exit time: Parking...'
                else:
                    exit_time_str = f'Exit time: {car_instance.exit_time}'

                if car_instance.parking_fee is None: #Checks if the car has a parking fee or is still parking
                    fee_str = 'Parking fee: Still parking...'
                else:
                    fee_str = f'Parking fee: £{car_instance.parking_fee}'

                details = (f'Vehicle with ticket number: {ticket_number}\n'
                           f'Registration number: {car_instance.regNo}\n'
                           f'Entry time: {car_instance.entry_time}\n'
                           f'Assigned parking space: {car_instance.parking_space}\n'
                           f'{exit_time_str}\n'
                           f'{fee_str}')

                self.status.set(details)

            self.ticket_entry.delete(0, tk.END)

        self.ticket_label.pack_forget()
        self.ticket_entry.pack_forget()
        self.query_button.pack_forget()

    #saves the corresponding records to the csv file
    def quit(self):
        self.car_park.csv_save('records.csv')
        print('Exiting the program. Come again. Thank you!!')
        sys.exit()



#Function calling and running of the program
if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()