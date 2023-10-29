from tkinter import *
import random
import pygame
import pandas

random_genre = ""
points = 0

genre_to_include = []
correct_key = 0
# Create and configure widgets.
root = Tk()
root.title("Guess the Genre Game")
data = pandas.read_csv("features_3_sec.csv").to_dict()
data_frame = pandas.DataFrame(data)
result_dictionary = data_frame.set_index("filename")["label"].to_dict()
items = list(result_dictionary.items())
flag2 = 0
flag = -1


def one_pressed():  # to check if button one is pressed
    global flag2
    flag2 = 1
    play_song()


def two_pressed():  # to check if button 2 is pressed
    global flag2
    flag2 = 2
    play_song()


def three_pressed():  # to check if button three is pressed
    global flag2
    flag2 = 3
    play_song()


def four_pressed():  # to check if button four is pressed
    global flag2
    flag2 = 3
    play_song()


# Place widgets in the window.
def button_text(correct_genre):  ## to change the button texts every single time the song changes
    global flag

    genre_list = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
    genre_list.remove(correct_genre)
    final_list = [correct_genre]
    for i in range(0, 3):
        final_genre = random.choice(genre_list)
        genre_list.remove(final_genre)
        final_list.append(final_genre)
    random.shuffle(final_list)
    button1.config(text=final_list[0])
    button1_text = final_list[0]
    button2.config(text=final_list[1])
    button2_text = final_list[1]
    button3.config(text=final_list[2])
    button3_text = final_list[2]
    button4.config(text=final_list[3])
    button4_text = final_list[3]
    flag = 0
    for i in range(4):
        if final_list[i] == correct_genre:
            flag = i + 1

        else:
            pass
    print(flag)


# Sample tracks and genres for your game.

def play_song(): # to check if the users selected button corresponds to the right song genre and change songs
    global points
    global random_genre
    global genre_to_include
    if flag == flag2:

        points += 1

        points_label.config(text=f"Points: {points}")
        result_label.config(text="CORRECT, YESSIR")
    elif flag == -1 and flag2 == 0:
        pass
    else:

        result_label.config(text=f"WRONG, ISSOK, the correct genre is {random_genre}")

    genre_list = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
    options = [button1, button2, button3, button4]
    random_item = random.choice(items)
    r_name = random_item[0].split(".")
    random_name = f"{r_name[0]}.{r_name[1]}.wav"
    random_genre = random_item[1]
    genre_list.remove(random_genre)
    location = f"D:/songs_database/Data/genres_original/{random_name}"
    button_text(random_genre)

    pygame.init()
    pygame.mixer.music.load(location)
    pygame.mixer.music.play()


genre_label = Label(root, text="Guess the genre of the track:")

points_label = Label(root, text="Points: 0")
result_label = Label(root, text="") # to display the result message on the screen

# Place widgets in the window.

button1 = Button(text="Button 1", command=one_pressed)
button2 = Button(text="Button 2", command=two_pressed)
button3 = Button(text="Button 3", command=three_pressed)
button4 = Button(text="Button 4", command=four_pressed)

# Load and play the audio clip.

play_song()
button1.pack()
button2.pack()
button3.pack()
button4.pack()
genre_label.pack()
points_label.pack()
result_label.pack()
root.mainloop()