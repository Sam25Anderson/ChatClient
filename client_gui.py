import tkinter as tk
from tkinter import scrolledtext

def add_button(button_name):
    global button_count
    button_count += 1
    tk.Button(button_frame, text=f"{button_name}").pack(fill="x", pady=2)
    canvas.configure(scrollregion=canvas.bbox("all"))

# Create the main window
window = tk.Tk()
window.title("Responsive Chat Client")

# Configure grid layout for responsiveness
window.columnconfigure(0, weight=1)  # Button list column
window.columnconfigure(1, weight=4)  # Chat display column
window.columnconfigure(2, weight=1)  # Send button column
window.rowconfigure(0, weight=5)  # Main content (buttons and chat display)
window.rowconfigure(1, weight=1)  # Message entry row

# Create a canvas and scrollbar for the button box
canvas = tk.Canvas(window)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Place canvas and scrollbar
canvas.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
scrollbar.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=10)

# Create a frame inside the canvas for buttons
button_frame = tk.Frame(canvas)
button_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=button_frame, anchor="nw")

# Initialize the button count
button_count = 0

# Programmatically add buttons
add_button("Test")
add_button("Big testerson")

# Add the chat display box
chat_display = scrolledtext.ScrolledText(window, state=tk.DISABLED)
chat_display.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=0, pady=10)

# Add the message entry box
message_entry = tk.Entry(window)
message_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=(0, 10))

# Add the send button
send_button = tk.Button(window, text="Send")
send_button.grid(row=1, column=2, sticky="ew", padx=10, pady=(0, 10))

# Run the main loop
window.mainloop() 
