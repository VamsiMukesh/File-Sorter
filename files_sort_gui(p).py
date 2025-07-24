import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def sort_files(source_folder, organize_by_type, organize_by_date, progress_callback):
    file_types = {
        'Images': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
        'Documents': ['.pdf', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
        'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
        'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
        'Music': ['.mp3', '.wav', '.aac', '.flac']
    }

    def get_type(ext):
        for typ, exts in file_types.items():
            if ext in exts:
                return typ
        return 'Other'

    files = [f for f in os.listdir(source_folder) if os.path.isfile(
        os.path.join(source_folder, f))]
    total = len(files)

    for idx, filename in enumerate(files, 1):
        file_path = os.path.join(source_folder, filename)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # Determine primary folder (type or extension)
        if organize_by_type:
            folder = get_type(ext)
        else:
            folder = ext[1:].upper() if ext else 'OTHER'

        # Optionally, organize by date (Year/Month)
        if organize_by_date:
            mtime = os.path.getmtime(file_path)
            import time
            year = time.strftime('%Y', time.localtime(mtime))
            month = time.strftime('%B', time.localtime(mtime))
            target_folder = os.path.join(source_folder, folder, year, month)
        else:
            target_folder = os.path.join(source_folder, folder)

        os.makedirs(target_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(target_folder, filename))

        if progress_callback:
            progress_callback(idx, total)


def browse_folder(var):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        var.set(folder_selected)


def start_sorting(source_var, type_var, date_var, progress_bar, status_label):
    src = source_var.get()
    if not src or not os.path.isdir(src):
        messagebox.showerror("Error", "Please select a valid source folder.")
        return

    # Prepare for sorting
    def update_progress(count, total):
        progress = int((count / total) * 100)
        progress_bar['value'] = progress
        status_label.config(text=f"Sorting... {count} of {total} files")

    try:
        sort_files(
            src,
            organize_by_type=type_var.get(),
            organize_by_date=date_var.get(),
            progress_callback=update_progress
        )
        status_label.config(text="Completed successfully!")
        messagebox.showinfo("Finished", "Files sorted successfully!")
    except Exception as e:
        status_label.config(text="Error occurred!")
        messagebox.showerror("Error", str(e))


# Build GUI
root = tk.Tk()
root.title("File Sorter")

source_var = tk.StringVar()
type_var = tk.BooleanVar(value=True)
date_var = tk.BooleanVar()

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0)

# Folder selection
ttk.Label(frame, text="Source Folder:").grid(row=0, column=0, sticky="e")
ttk.Entry(frame, width=40, textvariable=source_var).grid(row=0, column=1)
ttk.Button(frame, text="Browse", command=lambda: browse_folder(
    source_var)).grid(row=0, column=2)

# Options
ttk.Label(frame, text="Options:").grid(row=1, column=0, sticky="ne")
opts = ttk.Frame(frame)
opts.grid(row=1, column=1, sticky='w')
ttk.Checkbutton(opts, text="Organize by file type (Images, Documents...)",
                variable=type_var).grid(row=0, column=0, sticky='w')
ttk.Checkbutton(opts, text="Organize by date (Year/Month)",
                variable=date_var).grid(row=1, column=0, sticky='w')

# Progress bar & status
progress_bar = ttk.Progressbar(
    frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=2, column=0, columnspan=3, pady=(12, 3))
status_label = ttk.Label(frame, text="")
status_label.grid(row=3, column=0, columnspan=3)

# Start button
ttk.Button(frame, text="Start Sorting", command=lambda: start_sorting(
    source_var, type_var, date_var, progress_bar, status_label)
).grid(row=4, column=0, columnspan=3, pady=(10, 0))

root.mainloop()
