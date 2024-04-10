import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
import serial
import serial.tools.list_ports
import time

import threading


def try_convert_to_float(s):
    try:
        return float(s)
    except ValueError:
        return 0.0
    
ports = serial.tools.list_ports.comports()
if len(ports) == 0:
    port = "COM10"
    ser = serial.serial_for_url('loop://' + port, baudrate=9600, timeout=1)
else:
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")
    baud_rate = 115200
    ser = serial.Serial(port, baud_rate, timeout = 1)
time_data = []
force_data = []


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, force):
        super().__init__()
        self.title("Results")
        self.geometry("400x200")
        self.label = customtkinter.CTkLabel(self, text=f"Measured stress is {force} Pa")

        self.label.pack(padx=20, pady=20)



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("U Mich App ")
        self.geometry(f"{1800}x{1160}")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

        self.area = 1


        # codes to add background
        image = Image.open("U_M.png")
        # Resize the image to fit the window size
        print(image.size)
        image = image.resize((300, 180), Image.Resampling.LANCZOS)  # Adjust the size as needed
        photo = ImageTk.PhotoImage(image)

        # self.background_label = customtkinter.CTkLabel(self, image=photo, text = "")
        # self.background_label.image = photo
        # self.background_label.place(relx=0, rely=0)

        ## create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=10, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)
        # add the name of the gui
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Data Collector", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # add background of umich
        self.project_logo = customtkinter.CTkLabel(self.sidebar_frame, image=photo, text = "")
        self.project_logo.grid(row=1, column=0, padx = 20, pady = (10, 10))

        # self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text = "help",  command=self.sidebar_button_event)
        # self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        # add option menu for apperance
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        # add scaling menu for scaling of gui
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        ## create canvas and button
        # create the frame for canvas
        self.canvas_frame = customtkinter.CTkFrame(self, width = 200, height = 200,  corner_radius=0, fg_color="#D3D3D3")
        self.canvas_frame.grid(row=1, column=1, sticky="nsew")
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_rowconfigure(1, weight=5)
        self.canvas_frame.grid_columnconfigure(0, weight=1)


        self.button_frame = customtkinter.CTkFrame(self, width = 200, height = 10, corner_radius=0, fg_color="#A3D3D3")
        self.button_frame.grid(row=0, column=1, sticky="nsew")
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # create canvas
        self.canvas_name = customtkinter.CTkLabel(self.canvas_frame, text="Force readings", font=("Helvetica", 24), anchor="w")
        self.canvas_name.grid(row=0, column=0, padx=(1, 1), pady=(20, 0))

        fig = Figure(figsize=(5, 4), dpi=100)

        self.frame = customtkinter.CTkFrame(self.canvas_frame, 
                                            height = 800,
                                            width = 1200,
                                            fg_color='white')
        self.frame.grid(row=1, column=0, padx=(1, 1), pady=(0, 0))        

        # create button
        self.area_input_button = customtkinter.CTkButton(self.button_frame, text="Input area", height = 40, width = 200,
                                                         font = ("Helvetica", 16),  command=self.open_input_dialog_event)
        self.area_input_button.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.record_data_button = customtkinter.CTkButton(self.button_frame, text="Record data", height = 40, width= 200,
                                                          font = ("Helvetica", 16),  command = self.start_animation)
        
        self.record_data_button.grid(row=0, column=1, padx=20, pady=(10, 10))

        self.analyze_data_button = customtkinter.CTkButton(self.button_frame, text="Analyze data", height = 40, width = 200,
                                                           font = ("Helvetica", 16), command= self.anaylze_data )
        self.analyze_data_button.grid(row=0, column=2, padx=20, pady=(10, 10))
        self.toplevel_window = None
        self.stop_event = threading.Event()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        # Cancel the scheduled update
        if hasattr(self, "update_id"):
            self.frame.after_cancel(self.update_id)

        if hasattr(self, "thread_plot") and hasattr(self, "thread_readData"):
            self.stop_threads()
        # Close the window
        self.destroy()
        
    
    def update_plot(self):
        if not self.running:
            return
        fig, ax = plt.subplots()
        fig.set_size_inches(self.frame.winfo_width()/100.0, self.frame.winfo_height()/100.0)
        plt.plot(time_data[::10], force_data[::10])
        ax.set_xlabel("Time, t [s]")
        ax.set_ylabel("Force, F [N]")
        canvas = FigureCanvasTkAgg(fig,master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.0, rely=0.0)
        plt.close(fig)
        self.update_id = self.frame.after(100, self.update_plot)
    
    def start_animation(self):
        self.running = True
        self.start_time = time.time()
        time_data.clear()
        force_data.clear()
        self.thread_plot = threading.Thread(target=self.update_plot)
        self.thread_readData = threading.Thread(target=self.read_data)

        self.thread_plot.start()
        self.thread_readData.start()

    def stop_threads(self):
        self.stop_event.set()
        self.running = False
        self.thread_plot.join()
        self.thread_readData.join()

    def read_data(self):
        while self.running:
            line = ser.readline().decode().strip()
            res = try_convert_to_float(line)
            time_data.append(time.time() - self.start_time)
            force_data.append(res)

    def anaylze_data(self):
        if len(force_data) == 0:
            max_F = 0
            max_time = 0
        else:
            max_F = max(force_data)
            max_index = force_data.index(max_F)
            max_time = time_data[max_index]
        
        self.stop_threads()

        fig, ax = plt.subplots()
        fig.set_size_inches(self.frame.winfo_width()/100.0, self.frame.winfo_height()/100.0)
        force_dash = np.linspace(0, 1.05 * max_F, 100)
        plt.plot(time_data[::10], force_data[::10], label="Sensor readings")
        plt.plot(np.ones_like(force_dash) * max_time, force_dash, '--')
        plt.plot(max_time, max_F, marker='o', markerfacecolor='none', markeredgecolor='red', markersize=10, label="Fracture point")
        ax.set_xlabel("Time, t [s]")
        ax.set_ylabel("Force, F [N]")
        plt.legend()
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.0, rely=0.0)
        plt.close(fig)

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(max_F/self.area)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it



    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in the crosssectional area [m^2]:", title="Ice sample dialog")
        temp = dialog.get_input()
        if temp is not None:
            self.area = float(temp)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = App()
    app.mainloop()