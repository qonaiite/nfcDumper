import struct
import os
import tkinter as tk
from tkinter import filedialog

def convert_file(file_path):
    with open(file_path, "rb") as f:
        n = struct.unpack('<I', f.read(4))[0]
        offsets = list(struct.unpack('<'+str(n) +'I', f.read(4*n)))
        full_size = os.path.getsize(file_path)
        offsets.append(full_size)    
        sizes = [offsets[i+1] - offsets[i] for i in range(n)]
        print(sizes)
        for i, offs in enumerate(offsets):
            f.seek(offs)
            fourCC = f.read(4)
            if fourCC == b'_M1G':
                f.seek(offs)
                with open(f"model-{i}.g1m", 'wb') as out:
                    out.write(f.read(sizes[i]))
            elif fourCC == b'GT1G':
                f.seek(offs)
                with open(f"texture-{i}.g1t", 'wb') as out:
                    out.write(f.read(sizes[i]))

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        convert_file(file_path)

# Create a basic GUI window
root = tk.Tk()
root.title("nfcDumper")

# Create a button to open the file dialog
button = tk.Button(root, text="Select a .NFC File", command=open_file_dialog)
button.pack(pady=20)

# Run the GUI main loop
root.mainloop()
