'''
start a virtual enviroment
pip install pillow (*NOT* PIL, I know it's weird)
pip install requests
On windows, tkinter is installed by default
'''

import requests
import io # needed to process the bytes that we will download the sprite in
from pathlib import Path # if you want to create a cache of sprites
import tkinter as tk
from PIL import Image, ImageTk # allows us to manipulate images
import random


# ---------- constants ----------
POKE_COUNT = 1025           # adjust if new pokemon come out (is this a thing?)
API_URL    = "https://pokeapi.co/api/v2/pokemon/{}" # we will use {} later for substitution with .format()


# ---------- create our own dictionary of pokemon info ----------
def fetch_pokemon(pokemon_id:int)->dict:
    request = requests.get(API_URL.format(pokemon_id),timeout=10)
    request.raise_for_status()
    data = request.json()
    formatted_data = {
        "id":           pokemon_id,
        "name":         data["name"].title(),
        "types":        [t["type"]["name"] for t in data["types"]], 
        "weight_kg":    data["weight"]/10,
        "sprite":       data["sprites"]["front_default"]
        
    }
    return formatted_data

def fetch_image(url:str)->ImageTk.PhotoImage:
    img_bytes = requests.get(url,timeout=10).content
    pillow_image = Image.open(io.BytesIO(img_bytes)).resize((200,200))
    tk_image = ImageTk.PhotoImage(pillow_image)
    return tk_image

# ---------- GUI Stuff ----------
root = tk.Tk()
root.title("Random Pokémon Generator")
root.geometry("400x400")
root.resizable(False, False)

def show_pokemon(pokemon_id):
    try:
        formatted_data = fetch_pokemon(pokemon_id)
        tk_image = fetch_image(formatted_data["sprite"])
        root.img_label.photo = tk_image
        root.img_label.config(image=tk_image)

        types = " / ".join(formatted_data["types"]).title() # convert dict to string
        root.info_label.config(
            text=f"{formatted_data['name']}  (#{pokemon_id})\n"
                    f"Type: {types}\n"
                    f"Weight: {formatted_data['weight_kg']} kg"
        )
    except Exception as e:
        root.info_label.config(text=f"Error: {e}")
        
# widgets
root.img_label = tk.Label()
root.img_label.pack(pady=(10, 5))
root.info_label = tk.Label(font=("Helvetica", 12), justify="center")
root.info_label.pack(pady=(0, 10))

root.btn = tk.Button(
    text="Show Pokémon",
    font=("Helvetica", 14, "bold"),
    command = lambda:show_pokemon(random.randint(0,POKE_COUNT)) 
)
root.btn.pack(fill="x", padx=20, pady=5)



root.mainloop()
