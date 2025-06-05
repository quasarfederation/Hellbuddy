import tkinter as tk
import pyglet
from helldiversapi import *
pyglet.options["win32_gdi_font"] = True

window = tk.Tk()
pyglet.font.add_file("assets\\FS Sinclair Regular.otf")
pyglet.font.add_file("assets\\FS Sinclair Bold.otf")
label = tk.Label(window, text="Coretta Kelly Newsfeed", fg="yellow", bg="gray6", font=("FS Sinclair", 27, "bold"), pady=25)
text_output = tk.Text(window, bg="gray10", fg="yellow", font=("FS Sinclair", 15), height=17, relief="flat")
dispatch_btn = tk.Button(window, text="Get dispatch", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=25, relief="flat")
major_order_btn = tk.Button(window, text="Get MO", font=("FS Sinclair", 16), bg="gray10", fg="yellow", pady=25, padx=25, relief="flat")

def main():
    window.config(bg="gray6")
    window.resizable(False, False)
    window.geometry("1280x720")
    window.iconbitmap("assets\\icon.ico")
    window.title("Hellbuddy")

    text_output.config(state="disabled")

    dispatch_btn.config(command=lambda: on_button_click("dispatch"))
    major_order_btn.config(command=lambda: on_button_click("major order"))

    label.pack(fill="x")
    text_output.pack(side="right", expand=True)
    dispatch_btn.pack(side="left", expand=True)
    major_order_btn.pack(side="left", expand=True)

    window.mainloop()

def on_button_click(identifier):
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

if __name__ == "__main__":
    main()