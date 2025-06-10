import random
import tkinter as tk
import pyglet
from helldiversapi import *
pyglet.options["win32_gdi_font"] = True

window = tk.Tk()
pyglet.font.add_file("assets\\FS Sinclair Regular.otf")
pyglet.font.add_file("assets\\FS Sinclair Bold.otf")
button_frame = tk.Frame(window, bg="gray6", width=450, height=300)
label = tk.Label(window, text=f"Relay // {str(random.randint(100, 1000))} // CONNECTED", fg="yellow", bg="gray6", font=("FS Sinclair", 27, "bold"), pady=25)
text_output = tk.Text(window, bg="gray10", fg="yellow", font=("FS Sinclair", 15), height=17, relief="solid", state="disabled")
dispatch_btn = tk.Button(button_frame, text="Get Dispatch", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=36, relief="solid", overrelief="groove")
major_order_btn = tk.Button(button_frame, text="Get Major Order", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=28, relief="solid", overrelief="groove")
active_planet_btn = tk.Button(button_frame, text="Get War Status", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=24, relief="solid", overrelief="groove")
select_planet_btn = tk.Button(button_frame, text="Search Planet", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=34, relief="solid", overrelief="groove")
planet_entry = tk.Entry(button_frame, bg="gray10", fg="yellow", font=("FS Sinclair", 15), relief="solid")

def main() -> None:
    window.config(bg="gray6")
    window.resizable(False, False)
    window.geometry("1280x720")
    window.iconbitmap("assets\\icon.ico")
    window.title("Hellbuddy v1.0")

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

def on_button_click(identifier: str, planet_name: str=None) -> None:
    timer_var = 0

    match identifier:
        case "dispatch":
            text_output.config(state="normal")
            text_output.delete("0.0", "end")
            window.after(25, smooth_insert, "end", f"Connecting to Station {str(random.randint(10, 100))}...\n", 0)
            for message in HelldiversAPI.get_dispatch():
                timer_var += 3900
                window.after(timer_var, smooth_insert, "end", message + "\n", 0)
        case "major order":
            text_output.config(state="normal")
            text_output.delete("0.0", "end")
            window.after(25, smooth_insert, "end", f"Connecting to Station {str(random.randint(10, 100))}...\n", 0)
            for message in HelldiversAPI.get_major_order():
                timer_var += 1750
                window.after(timer_var, smooth_insert, "end", message + "\n", 0)
        case "active planets":
            text_output.config(state="normal")
            text_output.delete("0.0", "end")
            window.after(25, smooth_insert, "end", f"Connecting to Station {str(random.randint(10, 100))}...\n", 0)
            for planet in HelldiversAPI.get_campaign_info():
                timer_var += 4825
                window.after(timer_var, smooth_insert, "end", f"DISTRESS: {planet["name"]} is overrun with {planet["faction"]}. "
                                          f"There are {planet["players"]} Helldivers fighting here. This planet is {round(planet["percentage"], 4)}% liberated.\n"
                                          f" INFO: {planet["biome"]["description"]}\n\n", 0)
        case "select planet":
            text_output.config(state="normal")
            text_output.delete("0.0", "end")
            window.after(25, smooth_insert, "end", f"Connecting to Station {str(random.randint(10, 100))}...\n", 0)
            timer_var += 1500
            info = HelldiversAPI.get_planet_info(planet_name)
            try:
                window.after(timer_var, smooth_insert, "end", f"Planet found: {info[0]} // {info[1]} sector.\nINFO: ", 0)
                timer_var += 1500
                window.after(timer_var, smooth_insert, "end", f"{info[2]["description"]} You can expect the following: \n", 0)
                for environment in info[3]:
                    timer_var += 3300
                    window.after(timer_var, smooth_insert, "end", f"{environment["name"]} // {environment["description"]}\n", 0)
            except IndexError:
                window.after(timer_var, smooth_insert, "end", "Unavailable...", 0)

def smooth_insert(index: str | int, string: str, string_index: int=0) -> None:
    text_output.config(state="normal")
    dispatch_btn.config(state="disabled")
    major_order_btn.config(state="disabled")
    active_planet_btn.config(state="disabled")
    select_planet_btn.config(state="disabled")
    text_output.insert(index, string[string_index])
    if string_index + 1 > len(string) - 1:
        text_output.config(state="disabled")
        dispatch_btn.config(state="normal")
        major_order_btn.config(state="normal")
        active_planet_btn.config(state="normal")
        select_planet_btn.config(state="normal")
    else:
        string_index += 1
        window.after(10, smooth_insert, index, string, string_index)


if __name__ == "__main__":
    main()