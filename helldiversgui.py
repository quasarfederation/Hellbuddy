import tkinter as tk
import pyglet
from helldiversapi import *
pyglet.options["win32_gdi_font"] = True

window = tk.Tk()
pyglet.font.add_file("assets\\FS Sinclair Regular.otf")
pyglet.font.add_file("assets\\FS Sinclair Bold.otf")
button_frame = tk.Frame(window, bg="gray6", width=450, height=300)
label = tk.Label(window, text="Coretta Kelly Newsfeed", fg="yellow", bg="gray6", font=("FS Sinclair", 27, "bold"), pady=25)
text_output = tk.Text(window, bg="gray10", fg="yellow", font=("FS Sinclair", 15), height=17, relief="solid", )
dispatch_btn = tk.Button(button_frame, text="Get Dispatch", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=36, relief="solid")
major_order_btn = tk.Button(button_frame, text="Get Major Order", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=28, relief="solid")
active_planet_btn = tk.Button(button_frame, text="Get War Status", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=24, relief="solid")
select_planet_btn = tk.Button(button_frame, text="Search Planet", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=34, relief="solid")
planet_entry = tk.Entry(button_frame, bg="gray10", fg="yellow", font=("FS Sinclair", 15), relief="solid")

def main():
    window.config(bg="gray6")
    window.resizable(False, False)
    window.geometry("1280x720")
    window.iconbitmap("assets\\icon.ico")
    window.title("Hellbuddy v1.0")

    text_output.config(state="disabled")

    dispatch_btn.config(command=lambda: on_button_click("dispatch"))
    major_order_btn.config(command=lambda: on_button_click("major order"))
    active_planet_btn.config(command=lambda: on_button_click("active planets"))
    select_planet_btn.config(command=lambda: on_button_click("select planet", planet_name=planet_entry.get()))

    label.pack(fill="x")
    button_frame.pack(side="left")
    text_output.pack(side="right", expand=True, padx=10, pady=10, fill="y")
    dispatch_btn.grid(row=0, column=0, pady=5, padx=10)
    major_order_btn.grid(row=0, column=1, pady=5)
    active_planet_btn.grid(row=1, column=0, pady=5, padx=10)
    select_planet_btn.grid(row=1, column=1, pady=5)
    planet_entry.grid(row=3, column=1, pady=15, padx=10)

    window.mainloop()

def on_button_click(identifier, planet_name=None):
    timer_var = 0

    match identifier:
        case "dispatch":
            text_output.delete("0.0", "end")
            window.after(25, smooth_insert, "end", "Connecting to Station 5...\n", 0)
            for message in HelldiversAPI.get_dispatch():
                timer_var += 3900
                window.after(timer_var, smooth_insert, "end", message + "\n", 0)
        case "major order":
            text_output.delete("0.0", "end")
            window.after(25, smooth_insert, "end", "Connecting to Station 16...\n", 0)
            for message in HelldiversAPI.get_major_order():
                timer_var += 1750
                window.after(timer_var, smooth_insert, "end", message + "\n", 0)
        case "active planets":
            text_output.delete("0.0", "end")
            window.after(25, smooth_insert, "end", "Connecting to Station 12...\n", 0)
            for planet in HelldiversAPI.get_campaign_info():
                timer_var += 4825
                window.after(timer_var, smooth_insert, "end", f"DISTRESS: {planet["name"]} is overrun with {planet["faction"]}. "
                                          f"There are {planet["players"]} Helldivers fighting here. This planet is {round(planet["percentage"], 4)}% liberated.\n"
                                          f" INFO: {planet["biome"]["description"]}\n\n", 0)
        case "select planet":
            text_output.delete("0.0", "end")
            window.after(25, smooth_insert, "end", "Connecting to Station 23...\n", 0)
            timer_var += 1500
            info = HelldiversAPI.get_planet_info(planet_name)
            try:
                window.after(timer_var, smooth_insert, "end", f"Planet found: {info[0]} // {info[1]} sector.\nINFO: ", 0)
                timer_var += 2000
                window.after(timer_var, smooth_insert, "end", f"{info[2]["description"]} You can expect the following: \n", 0)
                for environment in info[3]:
                    timer_var += 2000
                    window.after(timer_var, smooth_insert, "end", f"{environment["name"]} // which means {environment["description"]}\n", 0)
            except IndexError:
                window.after(timer_var, smooth_insert, "end", "Unavailable...", 0)

def smooth_insert(index, string, string_index=0):
    text_output.config(state="normal")
    text_output.insert(index, string[string_index])
    if string_index + 1 > len(string) - 1:
        text_output.config(state="disabled")
    else:
        string_index += 1
        window.after(10, smooth_insert, index, string, string_index)


if __name__ == "__main__":
    main()