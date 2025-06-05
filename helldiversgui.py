import tkinter as tk
import pyglet
from helldiversapi import *
pyglet.options["win32_gdi_font"] = True

window = tk.Tk()
pyglet.font.add_file("assets\\FS Sinclair Regular.otf")
pyglet.font.add_file("assets\\FS Sinclair Bold.otf")
button_frame = tk.Frame(window, bg="gray6", width=450, height=300)
label = tk.Label(window, text="Coretta Kelly Newsfeed", fg="yellow", bg="gray6", font=("FS Sinclair", 27, "bold"), pady=25)
text_output = tk.Text(window, bg="gray10", fg="yellow", font=("FS Sinclair", 15), height=17, relief="flat", )
dispatch_btn = tk.Button(button_frame, text="Get Dispatch", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=36, relief="flat")
major_order_btn = tk.Button(button_frame, text="Get Major Order", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=28, relief="flat")
active_planet_btn = tk.Button(button_frame, text="Get War Status", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=24, relief="flat")
select_planet_btn = tk.Button(button_frame, text="Search Planet", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=34, relief="flat")
planet_entry = tk.Entry(button_frame, bg="gray10", fg="yellow", font=("FS Sinclair", 15), relief="sunken")

def main():
    window.config(bg="gray6")
    window.resizable(False, False)
    window.geometry("1280x720")
    window.iconbitmap("assets\\icon.ico")
    window.title("Hellbuddy v0.9")

    text_output.config(state="disabled")

    dispatch_btn.config(command=lambda: on_button_click("dispatch"))
    major_order_btn.config(command=lambda: on_button_click("major order"))
    active_planet_btn.config(command=lambda: on_button_click("active planets"))
    select_planet_btn.config(command=lambda: on_button_click("select planet", planet_name=planet_entry.get()))

    label.pack(fill="x")
    button_frame.pack(side="left")
    text_output.pack(side="right", expand=True)
    dispatch_btn.grid(row=0, column=0)
    major_order_btn.grid(row=0, column=1)
    active_planet_btn.grid(row=1, column=0)
    select_planet_btn.grid(row=1, column=1)
    planet_entry.grid(row=3, column=1, pady=15, padx=10)


    window.mainloop()

def on_button_click(identifier, planet_name=None):
    match identifier:
        case "dispatch":
            text_output.config(state="normal")
            text_output.delete("0.0", "end")
            text_output.insert("end", "Connecting to Station 5...\n")
            for message in HelldiversAPI.get_dispatch():
                text_output.insert("end", "BROADCAST:\n" + message + "\n")
            text_output.config(state="disabled")
        case "major order":
            text_output.config(state="normal")
            text_output.delete("0.0", "end")
            text_output.insert("0.0", "Connecting to Station 16...\nBROADCAST:\n")
            for message in HelldiversAPI.get_major_order():
                text_output.insert("end", message + "\n")
            text_output.config(state="disabled")
        case "active planets":
            text_output.config(state="normal")
            text_output.delete("0.0", "end")
            text_output.insert("0.0", "Connecting to Station 12...\nBROADCAST:\n")
            for planet in HelldiversAPI.get_campaign_info():
                text_output.insert("end", f"DISTRESS: {planet["name"]} is overrun with {planet["faction"]}. "
                                          f"There are {planet["players"]} Helldivers fighting here. This planet is {round(planet["percentage"], 4)}% liberated.\n"
                                          f" INFO: {planet["biome"]["description"]}\n\n")
            text_output.config(state="disabled")
        case "select planet":
            text_output.config(state="normal")
            text_output.delete("0.0", "end")
            text_output.insert("0.0", "Connecting to Station 23...\nBROADCAST:\n")
            info = HelldiversAPI.get_planet_info(planet_name)
            text_output.insert("end", f"Planet found: {info[0]} // {info[1]} sector.\nINFO: ")
            try:
                text_output.insert("end", f"{info[2]["description"]} You can expect the following: \n")
                for environment in info[3]:
                    text_output.insert("end", f"{environment["name"]} // which means {environment["description"]}")

            except:
                text_output.insert("end", "Unavailable...")
            text_output.config(state="disabled")

if __name__ == "__main__":
    main()