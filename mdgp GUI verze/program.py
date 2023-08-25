import tkinter as tk
import random
import csv

def load_champions_from_csv(filename):
    champions = {}
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            champion = row[0]
            champions[champion] = ""
    return champions

def champ_select(chosen_champs):
    champion_names = list(chosen_champs.keys())
    return random.sample(champion_names, champ_count)

def choices(choice: str):
    if choice.lower() == "no":
        result_label.config(text="OK!")
        return True
    return False

def select_champions():
    chosen_champs = champ_select(champions)
    champions_text = "\n".join(f"{champion} - Tier: {champions[champion]}" for champion in chosen_champs)
    champions_label.config(text=champions_text)

def reroll():
    choice = choice_entry.get()
    if choices(choice):
        root.destroy()
    else:
        select_champions()

def update_tier_entry():
    champion_name = update_champion_entry.get()
    new_tier = new_tier_entry.get()
    update_champion_entry.delete(0, tk.END)
    new_tier_entry.delete(0, tk.END)
    if champion_name in champions:
        update_tier(champion_name, new_tier)
        save_to_csv("champions.csv")
        result_label.config(text=f"Tier for {champion_name} updated to {new_tier}")
        select_champions()  # Aktualizovat text v GUI
    else:
        result_label.config(text=f"{champion_name} not found in champions")

def update_tier(champion_name, new_tier):
    champions[champion_name] = new_tier
    save_to_csv("champions.csv")  # Aktualizovat CSV soubor po změně třídy

def save_to_csv(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Champion", "Tier"])  # Přidat záhlaví pro třídy
        for champion, tier in champions.items():
            writer.writerow([champion, tier])

champ_count = 20
champions = load_champions_from_csv("champions.csv")

root = tk.Tk()
root.title("League of Legends Champ Select")

champions_label = tk.Label(root, text="", justify="left")
champions_label.pack()

choice_label = tk.Label(root, text="Do you wish to reroll? (yes/no)")
choice_label.pack()

choice_entry = tk.Entry(root)
choice_entry.pack()

reroll_button = tk.Button(root, text="Reroll", command=reroll)
reroll_button.pack()

update_champion_label = tk.Label(root, text="Champion to update:")
update_champion_label.pack()

update_champion_entry = tk.Entry(root)
update_champion_entry.pack()

new_tier_label = tk.Label(root, text="New Tier:")
new_tier_label.pack()

new_tier_entry = tk.Entry(root)
new_tier_entry.pack()

update_tier_button = tk.Button(root, text="Update Tier", command=update_tier_entry)
update_tier_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

select_champions()

root.mainloop()
