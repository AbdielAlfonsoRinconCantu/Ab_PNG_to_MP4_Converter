#Ab's PNG to MP4 converter
#Global
import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
from PIL import Image, ImageTk
FPS = 0
stop_joining_frames = False 
def custom_error_message(title, message):
    error_window = tk.Toplevel(root)
    error_window.overrideredirect(True)
    error_window.configure(background='#201c1c', highlightbackground='#c0c0c0', highlightthickness=1)
    label = tk.Label(error_window, text=title, bg='#201c1c', fg='white')
    label.pack(padx=20, pady=(10, 5))
    message_label = tk.Label(error_window, text=message, bg='#201c1c', fg='white')
    message_label.pack(padx=20, pady=(0, 10))
    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy, bg='#201c1c', fg='white', width=10)
    ok_button.pack(padx=20, pady=(0, 10))
    error_window.geometry("300x120")
    center_window(error_window)
    root.wait_window(error_window)
def update_progress_bar(progress, total):
    progress_bar['value'] = (progress / total) * 100
    root.update_idletasks()
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
def select_frames_path():
    global frames_path
    frames_path = filedialog.askdirectory(title="Select a folder")
    if frames_path:
        frames_path_label.config(text=f"Frames folder path: {frames_path}")
def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory(title="Select output folder")
    if output_folder:
        output_folder_label.config(text=f"Output folder: {output_folder}")
def set_FPS():
    global FPS, x, y  # Declare x, y, and FPS as global
    def on_drag(event):
        FPS_window.geometry(f"+{FPS_window.winfo_pointerx()-x}+{FPS_window.winfo_pointery()-y}")
    def on_drag_start(event):
        global x, y  # Declare x and y as global within this function scope
        x, y = event.x, event.y
    def submit_FPS():
        global FPS  # Declare FPS as global within this function scope
        try:
            FPS = float(entry.get())
            FPS_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")
    def cancel_FPS():
        FPS_window.destroy()
    FPS_window = tk.Toplevel(root)
    FPS_window.overrideredirect(True)
    FPS_window.configure(background='#201c1c', highlightbackground='#c0c0c0', highlightthickness=1)  # Set the outline color and thickness
    FPS_window.geometry("240x120")
    FPS_window.bind("<B1-Motion>", on_drag)
    FPS_window.bind("<Button-1>", on_drag_start)
    center_window(FPS_window)  # Center FPS window
    label = tk.Label(FPS_window, text="Enter FPS:", bg='#201c1c', fg='white')
    label.pack(pady=(10, 5))
    entry_frame = tk.Frame(FPS_window, bg='#201c1c')
    entry_frame.pack()
    entry = tk.Entry(entry_frame, bg='#201c1c', fg='white', justify='center')  
    entry.pack(padx=10, pady=5)
    button_frame = tk.Frame(FPS_window, bg='#201c1c')
    button_frame.pack(pady=5)
    submit_button = tk.Button(button_frame, text="Submit", command=submit_FPS, bg='#201c1c', fg='white')
    submit_button.pack(side=tk.LEFT, padx=5)
    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_FPS, bg='#201c1c', fg='white')
    cancel_button.pack(side=tk.LEFT, padx=5)
    root.mainloop()
def join_frames(frames_path, output_folder, FPS, root):
    global stop_joining_frames
    if not frames_path:
        custom_error_message("Error", "Frames folder not selected.")
        return
    elif not output_folder:
        custom_error_message("Error", "Output folder not selected.")
        return
    elif not FPS:
        custom_error_message("Error", "FPS count not set.")
        return
    if frames_path and output_folder and FPS:
        images = [img for img in os.listdir(frames_path) if img.startswith("frame_") and img.endswith(".png")]
        images.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
        frame = cv2.imread(os.path.join(frames_path, images[0]))
        height, width, layers = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_video_path = os.path.join(output_folder, 'output_video.mp4')
        video = cv2.VideoWriter(output_video_path, fourcc, FPS, (width, height))
        stop_joining_frames = False
        frame_count = 0
        total_frames = len(images)
        for image in images:
            if stop_joining_frames:
                break
            img_path = os.path.join(frames_path, image)
            frame = cv2.imread(img_path)
            video.write(frame)
            frame_count += 1
            update_progress_bar(frame_count, total_frames)  # Updated to call the progress bar update function

        cv2.destroyAllWindows()
        video.release()
        messagebox.showinfo("Frames Joined", f"Joined {frame_count} frames out of {total_frames}")
def open_frames_path_folder():
    if frames_path:
        subprocess.Popen(['explorer', os.path.normpath(frames_path)])
def open_output_folder():
    if output_folder:
        subprocess.Popen(['explorer', os.path.normpath(output_folder)])
def close_program():
    root.destroy()
def on_drag(event):
    root.geometry(f"+{root.winfo_pointerx()-x}+{root.winfo_pointery()-y}")
def on_drag_start(event):
    global x, y
    x, y = event.x, event.y
def stop_joining_frames_process():
    global stop_joining_frames
    stop_joining_frames = True 
#Main
root = tk.Tk()
root.title("Frame video maker")
root.overrideredirect(True)
root.configure(background='#201c1c')
root.geometry("540x360")
center_window(root)
frame = tk.Frame(root, bg='#201c1c')
frame.pack(padx=20, pady=20)
frames_path = ""
output_folder = ""
icon_path = os.path.join(os.path.dirname(__file__), "Open-File-Folder-Flat-icon.png")
open_video_icon_img = Image.open(icon_path)
open_video_icon_img = open_video_icon_img.resize((20, 20))
open_video_icon = ImageTk.PhotoImage(open_video_icon_img)
open_output_icon_img = Image.open(icon_path)
open_output_icon_img = open_video_icon_img.resize((20, 20))
open_output_icon = ImageTk.PhotoImage(open_video_icon_img)
frames_button = tk.Button(frame, text="Select frames folder", command=select_frames_path, bg='#201c1c', fg='white')
frames_button.grid(row=0, column=0, sticky='w', pady=10, padx=10)
frames_path_label = tk.Label(frame, text="Frames folder path: ", bg='#201c1c', fg='white', wraplength=400)
frames_path_label.grid(row=1, column=0, sticky='w')
output_button = tk.Button(frame, text="Select output folder", command=select_output_folder, bg='#201c1c', fg='white')
output_button.grid(row=2, column=0, sticky='w', pady=10, padx=10)
output_folder_label = tk.Label(frame, text="Output folder: ", bg='#201c1c', fg='white',wraplength=400)
output_folder_label.grid(row=3, column=0, sticky='w')
open_frames_path_button = tk.Button(frame, image=open_video_icon, command=open_frames_path_folder, bg='#201c1c', borderwidth=0)
open_frames_path_button.grid(row=1, column=1, sticky='e', pady=10, padx=10)
open_output_folder_button = tk.Button(frame, image=open_output_icon, command=open_output_folder, bg='#201c1c', borderwidth=0)
open_output_folder_button.grid(row=3, column=1, sticky='e', pady=10, padx=10)
progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
progress_bar.pack(pady=10)
start_button = tk.Button(frame, text="Start", command=lambda: join_frames(frames_path, output_folder, FPS, root), bg='#201c1c', fg='white')
start_button.grid(row=5, column=0, pady=5, columnspan=2)
close_button = tk.Button(root, text="Exit", command=close_program, bg='#201c1c', fg='white')
close_button.pack(padx=20, pady=0)
root.bind("<B1-Motion>", on_drag)
root.bind("<Button-1>", on_drag_start)
stop_button = tk.Button(frame, text="Stop", command=stop_joining_frames_process, bg='#201c1c', fg='white')
stop_button.grid(row=5, column=0, pady=5, columnspan=2, sticky='e')
program_name_label = tk.Label(root, text="Ab's PNG to MP4 converter 1.0", bg='#201c1c', fg='white')
program_name_label.pack(side=tk.BOTTOM, padx=10, pady=10, anchor=tk.SW)
set_FPS_button = tk.Button(frame, text="Set FPS", command=set_FPS, bg='#201c1c', fg='white')
set_FPS_button.grid(row=5, column=0, pady=5, sticky='w')
root.mainloop()