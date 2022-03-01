import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk,Image
from movies_info import *
import smtplib
import ssl
from email.message import EmailMessage
import qrcode
import imghdr

root = tk.Tk()
root.title("Theatre Seat Reservation")
root.geometry("600x600")

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

def calculate_index(row, col, cols):
    return cols*row + col

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
    clear_frame(frame2)

    global Seats
    Seats = [[Seat(row,col,False) for col in range(columns)] for row in range(rows)]
    global Buttons
    Buttons =  [[0 for col in range(columns)] for row in range(rows)]
    Labels = [0 for row in range(rows)]

    for row in range(rows):
        letter = Row_Letter[row]
        Labels[row] = tk.Label(frame2, text = f'{letter}: ')
        Labels[row].grid(row=row, column=1, padx = 1, pady = 1)
        for col in range(columns):
            Buttons[row][col] = tk.Button(frame2, width = 2, text = col+1, bg = 'green', command= lambda x1=letter, y1=col+1, x2=row: show_info(x1,y1,x2))
            Buttons[row][col].grid(row=row, column=col+2, padx = 1, pady = 1)
    
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

def calculate_price():
    number = 0
    for i in range(len(seats_to_reserve)):
        number += 5
    tk.Label(frame3, text = number).grid(row = 3, column = 3)

def show_theatre_maker():
    # PUT THEATRE INFORMATION WIDGETS TO GRID
    clear_frame(show_frame)
    print('fjiaofdsjifoij')
    pick_movie_label.config(text = '')
    label_rows_entry.grid(row=0,column=0)
    rows_entry.grid(row=0,column=1)
    label_columns_entry.grid(row=1,column=0)
    columns_entry.grid(row=1,column=1)
    make_theatre_button.grid(row=2,column=0, pady = 10)
    reserve_seat_button.grid(row=3,column=1, pady = 10)
    calculate_button.grid(row=3,column=2, padx = 10, pady = 10)

def make_theatre():
    clear_frame(frame2)

    rows = int(rows_entry.get())
    columns = int(columns_entry.get())

    global Seats
    Seats = [[Seat(row,col,False) for col in range(columns)] for row in range(rows)]
    global Buttons
    Buttons =  [[0 for col in range(columns)] for row in range(rows)]
    Labels = [0 for row in range(rows)]

    for row in range(rows):
        letter = Row_Letter[row]
        Labels[row] = tk.Label(frame2, text = f'{letter}: ')
        Labels[row].grid(row=row, column=0, padx = 1, pady = 1)
        for col in range(columns):
            Buttons[row][col] = tk.Button(frame2, width = 2, text = col+1, bg = 'green', command= lambda x1=letter, y1=col+1, x2=row: show_info(x1,y1,x2))
            Buttons[row][col].grid(row=row, column=col+1, padx = 1, pady = 1)

def save_theatre():
    theatre_file = filedialog.asksaveasfilename(
        initialdir="C:\\Users\\admin\\Desktop\\Coding\\Python\\Button Array Creation\\Theatres", 
        defaultextension = ".*",
        title = 'Save Theatre',
        filetypes = (("Text Files", "*.txt"), ("All Files", "*.*")))
    if theatre_file:
        name = f'{theatre_file} - Theatre Seat Reservation'
        name = name.replace("C:/Users/admin/Desktop/Coding/Python/Button Array Creation/Theatres/", "")
        root.title(name)

        theatre_file = open(theatre_file, 'w')
        rows_to_be_saved = rows_entry.get()
        columns_to_be_saved = columns_entry.get()
        output = f'{rows_to_be_saved} {columns_to_be_saved} '
        for seat in seats_to_reserve:
            output = f'{output} {get_letter(seat.row)}{seat.number+1}'
        theatre_file.write(output)
        theatre_file.close()
        print("Theatre Saved!")

def import_theatre():
    clear_frame(frame2)
    reservation_label.config(text = '')
    theatre_file = filedialog.askopenfilename(
        initialdir="C:\\Users\\admin\\Desktop\\Coding\\Python\\Button Array Creation\\Theatres", 
        title = "Import Theatre",
        filetypes = (("Text Files", "*.txt"), ("All Files", "*.*")))        
    if theatre_file:
        name = f'{theatre_file} - Theatre Seat Reservation'
        name = name.replace("C:/Users/admin/Desktop/Coding/Python/Button Array Creation/Theatres/", "")
        root.title(name)

        theatre_file = open(theatre_file, 'r')
        info = theatre_file.read()
        theatre_file.close()
        #print(info)
        info_array = info.split()
        row, col = int(info_array[0]), int(info_array[1])
        make_theatre_for_file(row, col)
        for i in range(2, len(info_array), 1):
            seat_row, seat_col = get_row_col(info_array[i])
            switch(Buttons[seat_row][seat_col-1])
            make_reservation_for_file(seat_row, seat_col-1)
        print('Theatre Imported!')

def show_movie_theatre(movie_name):
    theatre_file = open(f"Movie Theatres\\{movie_name}Theatre.txt", "r")
    info = theatre_file.read()
    theatre_file.close()
    print(info)
    info_array = info.split()
    row, col = int(info_array[0]), int(info_array[1])
    make_theatre_for_file(row, col)
    for i in range(2, len(info_array), 1):
        seat_row, seat_col = get_row_col(info_array[i])
        switch(Buttons[seat_row][seat_col-1])
        make_reservation_for_file(seat_row, seat_col-1)
    tk.Label(frame3, text = 'Email to send the tickets to: ').grid(row = 0, column = 0, padx = 5)
    mail_entry.grid(row = 0, column = 1, pady = 5)
    tk.Button(frame3, text = 'Make Reservation', command = lambda x1=movie_name: make_reservation_mail(x1)).grid(row = 1, column = 0, pady = 10)
    print('Theatre Imported!')

def make_qr_code(seats_string):
    qr_code_content = f'Seats:{seats_string}'
    print(qr_code_content)
    img=qrcode.make(qr_code_content)
    filename = "seat_qr_code.png"
    img.save(filename)

    return filename

def make_reservation_mail(movie_name):
    seat_string = ''
    global seats_to_reserve
    seats_to_reserve = list(dict.fromkeys(seats_to_reserve))
    for seat in seats_to_reserve:
        seat.isTaken = True
        Buttons[seat.row][seat.number].configure(bg = 'red')
        switch(Buttons[seat.row][seat.number])
        seat_string = f'{seat_string} {get_letter(seat.row)}{seat.number+1}'

    subject = f"Tickets for {movie_name} at Cinemas"
    body = f"Your tickets for seats {seat_string} for the movie -{movie_name}- have been reserved. Thank you for choosing us!"
    sender_email = "jniddas@gmail.com"
    password = "pythonpassword"
    receiver_email = mail_entry.get()
    qr_code = make_qr_code(seat_string)

    message = EmailMessage()
    message['From'] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.set_content(body)
    with open(qr_code, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name

    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    context = ssl.create_default_context()

    print("Sending Email...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email Successfully Sent!")

    theatre_file = open(f"Movie Theatres\\{movie_name}Theatre.txt", "a")
    output = ''
    for seat in seats_to_reserve:
        output = f'{output} {get_letter(seat.row)}{seat.number+1}'
    theatre_file.write(output)
    theatre_file.close()
    print("Theatre Saved!")
    tk.Label(frame3, text = 'Your tickets have been sent to your email.').grid(row = 1, column = 1)

    
def show_movies():
    for i in range(len(MOVIES)):
        tk.Button(movie_frame, image = MOVIES[MOVIE_NAMES[i]], command= lambda x1=MOVIE_NAMES[i]: show_movie_info(x1)).grid(row = 1, column = i, padx = 3, pady = 1)
        tk.Label(movie_frame, text = MOVIE_NAMES[i]).grid(row = 2, column = i, padx = 3)
    
def show_movie_info(movie_name):
    clear_frame(movie_frame)

    if movie_name == "Uncharted":
        img = unchartedImage
        info = info_uncharted
    elif movie_name == "Scream":
        img = screamImage
        info = info_scream
    elif movie_name == "Batman":
        img = batmanImage
        info = info_batman

    tk.Label(show_frame, image = img).grid(row = 0, column = 0)
    tk.Button(show_frame, text = 'Show Available Seats', command = lambda x1=movie_name: show_movie_theatre(x1)).grid(row = 2, column = 0, pady = 5)
    tk.Label(show_frame, text = movie_name).grid(row = 1, column = 0)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# MAKE MOVIE PICKER FRAME 
movie_frame = tk.Frame(root)
movie_frame.grid(row = 0, column = 1)

show_frame = tk.Frame(root)
show_frame.grid(row = 0, column = 0)

# MAKE THEATRE FRAME
frame1 = tk.Frame(root)
frame1.grid(row=1,column=0)

# SHOW THEATRE FRAME
frame2 = tk.Frame(root)
frame2.grid(row=2,column=0)

# CHECK SEAT FRAME
frame3 = tk.Frame(root)
frame3.grid(row=3,column=0)

# PICK A MOVIE 
unchartedImage = ImageTk.PhotoImage(Image.open("Movie Images\\UnchartedImage.jpg"))
screamImage = ImageTk.PhotoImage(Image.open("Movie Images\\ScreamImage.jpg"))
batmanImage = ImageTk.PhotoImage(Image.open("Movie Images\\BatmanImage.jpg"))

MOVIE_NAMES = ["Uncharted", "Scream", "Batman"]

MOVIES = {
    "Uncharted":unchartedImage,
    "Scream":screamImage,
    "Batman":batmanImage
}

pick_movie_label = tk.Label(movie_frame, text = '           Playing Now ')
pick_movie_label.grid(row = 0, column = 0)
upcoming_movie_label = tk.Label(movie_frame, text = ' Upcoming ')
upcoming_movie_label.grid(row = 0, column = 2)
show_movies()

# MAKE THEATRE INFORMATION WIDGETS
label_rows_entry = tk.Label(frame1, text = '    How many rows is the theatre going to be: ')
rows_entry = tk.Entry(frame1)
label_columns_entry = tk.Label(frame1, text = '    How many seats per row is the theatre going to have: ')
columns_entry = tk.Entry(frame1)
make_theatre_button = tk.Button(frame1, text = 'Make Theatre', command = make_theatre)

# FILE MENUS 
my_menu = tk.Menu(root)
root.config(menu=my_menu)
file_menu = tk.Menu(my_menu, tearoff = False)
my_menu.add_cascade(label='File', menu = file_menu)
file_menu.add_command(label='New Theatre', command=show_theatre_maker)
file_menu.add_command(label='Save Theatre', command=save_theatre)
file_menu.add_command(label='Import Theatre', command=import_theatre)

# BUTTONS
calculate_button = tk.Button(frame3, text = "Calculate Total Price", command = calculate_price)
reserve_seat_button = tk.Button(frame3, text = 'Make Reservation', command = make_reservation)
reservation_label = tk.Label(frame3, text = '')
mail_entry = tk.Entry(frame3)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()