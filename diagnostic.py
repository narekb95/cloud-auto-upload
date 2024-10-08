import tkinter as tk

from os import path
from config import Config
from helpers import timestamp_to_date, open_file

def get_data():
    config = Config()
    files = sorted(config.files, key=lambda f: f['last-update'], reverse=True)
    return list(map(lambda f: {
        'name': f['name'],
        'timestamp': timestamp_to_date(f['last-update']),
        'path': path.join(config.target_dir, f['name'])
        }, files))

def create_table(frame):
    data = get_data()
    for i, row in enumerate(data):
        bg_col = "white" if i % 2 == 0 else "lightgrey"
        label_name = tk.Label(frame, text=row['name'], padx=25, pady=5, borderwidth=0, relief="solid",
                              bg=bg_col, anchor="w", font=("Arial", 16))
        label_name.grid(row=i, column=0, sticky="nsew")

        label_name.bind("<Enter>", lambda e, lbl=label_name: lbl.config(fg="blue"))  # Change text color on hover
        label_name.bind("<Leave>", lambda e, lbl=label_name: lbl.config(fg="black"))  # Reset text color
        # Bind click event to open the file
        label_name.bind("<Button-1>", lambda e, path=row['path']: open_file(path))

        label_timestamp = tk.Label(frame, text=row['timestamp'], padx=25, pady=5, borderwidth=0, relief="solid",
                                    bg=bg_col, anchor="w", font=("Arial", 16))
        label_timestamp.grid(row=i, column=1, sticky="nsew")

    frame.grid_columnconfigure(0, weight=2)
    frame.grid_columnconfigure(1, weight=1)

def resize_table(event):
    canvas_width = event.width
    canvas.itemconfig(table_window, width=canvas_width)

def update_scrollregion(_):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


root = tk.Tk()
root.title("Active files")
root.geometry("600x400")
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
table_frame = tk.Frame(canvas)
table_window = canvas.create_window((0, 0), window=table_frame, anchor="nw")

canvas.bind("<Configure>", resize_table)
table_frame.bind("<Configure>", update_scrollregion)
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

create_table(table_frame)

root.mainloop()
