import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Theatre Seat Reservation")
root.geometry("600x420")

current_row, current_column = 0, 0
seats_to_reserve = []

Row_Letter = {
        0:'A',
        1:'B',
        2:'C',
        3:'D',
        4:'E',
        5:'F',
        6:'G',
        7:'H',
        8:'I',
        9:'J',
        10:'K',
        11:'L',
        12:'M',
        13:'N',
        14:'O',
        15:'P',
        16:'Q',
        17:'R',
        18:'S',
        19:'T',
        20:'U'
    }

class Seat():
    def __init__(self, row, number, isTaken):
        self.row = row
        self.number = number
        self.isTaken = isTaken

def show_info(row, column, cur_row):
    global current_row, current_column 
    current_row, current_column = cur_row, column-1
    global seats_to_reserve
    seats_to_reserve.append(Seats[current_row][current_column])
    Buttons[current_row][current_column].configure(bg = 'yellow')
    print(f'SEAT: {row} {column}')

def clear_frame(frame):
    for child in frame.winfo_children():
        child.destroy()

def switch(b1):
    if b1["state"] == "normal":
        b1["state"] = "disabled"
    else:
        b1["state"] = "normal"

def make_reservation():
    global seats_to_reserve
    string = ''
    #print(Seats[current_row][current_column].row, Seats[current_row][current_column].number, Seats[current_row][current_column].isTaken)
    seats_to_reserve = list(dict.fromkeys(seats_to_reserve))
    for seat in seats_to_reserve:
        seat.isTaken = True
        Buttons[seat.row][seat.number].configure(bg = 'red')
        switch(Buttons[seat.row][seat.number])
        string = f'{string} {get_letter(seat.row)}{seat.number+1}'
    reservation_label.config(text = f'Reservation made for seats: {string}')
    string = ''

def make_theatre_for_file(rows, columns):
    clear_frame(frame)

    global Seats
    Seats = [[Seat(row,col,False) for col in range(columns)] for row in range(rows)]
    global Buttons
    Buttons =  [[0 for col in range(columns)] for row in range(rows)]
    Labels = [0 for row in range(rows)]

    for row in range(rows):
        Labels[row] = tk.Label(frame, text = f'{get_letter(row)}: ')
        Labels[row].grid(row=row, column=0, padx = 1, pady = 1)
        for col in range(columns):
            Buttons[row][col] = tk.Button(frame, width = 2, text = col+1, bg = 'green', command= lambda x1=get_letter(row), y1=col+1, x2=row: show_info(x1,y1,x2))
            Buttons[row][col].grid(row=row, column=col+1, padx = 1, pady = 1)
   
def make_reservation_for_file(row, col):
    global Seats
    Seats[row][col].isTaken = True
    Buttons[row][col].configure(bg = 'red')

def get_row_col(seat):
    info = list(seat)
    row = int(get_key(info[0]))
    col = int(info[1])
    return row, col

def get_key(val):
    for key, value in Row_Letter.items():
         if val == value:
             return key
    return "key doesn't exist"

def get_letter(number_of_row):
    return Row_Letter[number_of_row]

def save_theatre():
    theatre_file = open("Theatres\\vol2.txt", "a")
    output = ''
    #seats_to_reserve = list(dict.fromkeys(seats_to_reserve))
    for seat in seats_to_reserve:
        output = f'{output} {get_letter(seat.row)}{seat.number+1}'
    theatre_file.write(output)
    theatre_file.close()
    print("Theatre Saved!")

def import_theatre():
    clear_frame(frame)
    theatre_file = open("Theatres\\vol2.txt", "r")

    info = theatre_file.read()
    theatre_file.close()
    print(info)
    info_array = info.split()
    global row, col
    row, col = int(info_array[0]), int(info_array[1])
    make_theatre_for_file(row, col)
    for i in range(2, len(info_array), 1):
        seat_row, seat_col = get_row_col(info_array[i])
        switch(Buttons[seat_row][seat_col-1])
        make_reservation_for_file(seat_row, seat_col-1)
    print('Theatre Imported!')

def reset():
    for row in range(len(Buttons)):
        for col in range(len(Buttons[0])):
            Buttons[row][col].configure(bg = 'green')
            Buttons[row][col]["state"] = "normal"

    theatre_file = open("Theatres\\vol2.txt", "w")
    string = f'{row+1} {col+1}'
    theatre_file.write(string)
    theatre_file.close()


def on_closing():
    save_theatre()
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# MAKE THEATRE FRAME
frame = tk.Frame(root)
frame.grid(row=0,column=0)

frame2 = tk.Frame(root)
frame2.grid(row=1,column=0)


reserve_seat_button = tk.Button(frame2, text = 'Make Reservation', command = make_reservation)
reserve_seat_button.grid(row=0,column=0, pady = 10)
reservation_label = tk.Label(frame2, text = '')
reservation_label.grid(row = 1, column = 0, pady = 10)
resetButton = tk.Button(frame2, text = 'Reset', command = reset)
resetButton.grid(row=2,column=0, pady = 10)
import_theatre()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()