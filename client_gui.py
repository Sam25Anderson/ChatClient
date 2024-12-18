import tkinter as tk
from tkinter import scrolledtext

def add_button(button_name):
    global button_count
    button_count += 1
    tk.Button(button_frame, text=f"{button_name}").pack(fill="x", pady=2)
    canvas.configure(scrollregion=canvas.bbox("all"))

window = tk.Tk()
window.title("Chat Client")

# Set the minimum size of the window
window.minsize(400, 400)

# Configure rows and columns
window.columnconfigure(0, weight=0)  # Fix button list column width
window.columnconfigure(1, weight=2)  # Chat display
window.columnconfigure(2, weight=1)  # Send button
window.rowconfigure(0, weight=3)  # Main content
window.rowconfigure(1, weight=1)  # Message entry

# Create the button frame with a fixed width
button_frame = tk.Frame(window, width=100)
button_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(10, 0), pady=10)

button_frame.grid_propagate(False)
canvas = tk.Canvas(button_frame)
scrollbar = tk.Scrollbar(button_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")

inner_frame = tk.Frame(canvas)
inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

button_count = 0
add_button("Test")  # Example buttons
add_button("Big testerson")

# Create the chat display
chat_display = scrolledtext.ScrolledText(window, state=tk.DISABLED)
chat_display.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=0, pady=10)

# Create the message entry
message_entry = tk.Entry(window)
message_entry.grid(row=1, column=1, sticky="ew", padx=0, pady=(0, 10))

# Create the send button
send_button = tk.Button(window, text="Send")
send_button.grid(row=1, column=2, sticky="ew", padx=10, pady=(0, 10))

window.mainloop()
