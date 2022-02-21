import tkinter as tk
from PIL import ImageTk,Image


root = tk.Tk()


MOVIE_NAMES = ["Uncharted", "Scream", "Batman"]

photo = ImageTk.PhotoImage(Image.open("Movie Images\\ScreamImage.jpg"))

Button = tk.Button(root , image = photo)
Button.pack()

MOVIES = {
    "Uncharted":"Movie Images\\UnchartedImage.jpg",
    "Scream":"Movie Images\\ScreamImage.jpg",
    "Batman":"Movie Images\\BatmanImage.jpg"
}

pick_movie_label = tk.Label(root, text = 'Pick a movie:')
pick_movie_label.pack()
#show_movies(MOVIE_NAMES)


root.mainloop()