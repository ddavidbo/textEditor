import tkinter as tk
from tkinter import filedialog, Menu, messagebox, font, simpledialog, scrolledtext
import subprocess
import os

filename = None

def newFile():
    global filename
    filename = "Untitled"
    text.delete('1.0', tk.END)

def saveFile():
    global filename
    if filename:
        content = text.get('1.0', tk.END)
        with open(filename, 'w') as file:
            file.write(content)
    else:
        saveAs()

def saveAs():
    global filename
    f = filedialog.asksaveasfile(mode="w", defaultextension='.txt')
    if f is None:
        return  # User cancelled the operation

    text_content = text.get('1.0', tk.END)
    try:
        f.write(text_content.rstrip())
        filename = f.name  # Update the filename
    except Exception as e:
        # Handle any exceptions that occur during writing
        messagebox.showerror("Error", "Unable to save file: " + str(e))
    finally:
        f.close()

def openFile():
    global filename
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                text.delete('1.0', tk.END)
                text.insert('1.0', content)
                filename = file_path
        except Exception as e:
            messagebox.showerror("Error", "Unable to open file: " + str(e))

def change_font_size():
    global text
    size = simpledialog.askinteger("Font Size", "Enter font size:")
    if size is not None:
        text.config(font=(text_font_family, size))

def change_font_family(family):
    global text, text_font_family
    text_font_family = family
    text.config(font=(text_font_family, text_font_size))

def execute_python_code():
    code = text.get('1.0', tk.END)
    try:
        result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            output_text.config(state='normal')
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, output)
            output_text.config(state='disabled')
            output_window.deiconify()
        else:
            error = result.stderr
            messagebox.showerror("Python Error", error)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def close_output_window():
    output_window.withdraw()

def confirm_quit():
    if messagebox.askyesno("Quit", "Do you want to save before quitting?"):
        saveFile()
    root.destroy()

# Create the main application window
root = tk.Tk()
root.title("textEditor")

# Define default font settings
text_font_family = "Arial"
text_font_size = 12

# Create a text widget
text = tk.Text(root, bg="#222222", fg="white", insertbackground="white", font=(text_font_family, text_font_size))
text.pack(expand=True, fill='both')

# Create a menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create a File menu
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)

# Add commands to the File menu
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As", command=saveAs)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_separator()  # Add a separator between commands
filemenu.add_command(label="Quit", command=confirm_quit)

# Create a Font menu
fontmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Font", menu=fontmenu)

# Add command to the Font menu for changing font size
fontmenu.add_command(label="Change Font Size", command=change_font_size)

# Add commands to the Font menu for changing font family
font_families = font.families()
font_family_menu = Menu(fontmenu, tearoff=0)
fontmenu.add_cascade(label="Font Family", menu=font_family_menu)
for family in font_families:
    font_family_menu.add_command(label=family, command=lambda f=family: change_font_family(f))

# Create a Compiler menu
compiler_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Compile", menu=compiler_menu)

# Add commands to the Compiler menu for executing Python and Java code
compiler_menu.add_command(label="Run Python Code", command=execute_python_code)

# Create output window
output_window = tk.Toplevel(root)
output_window.title("Output")
output_window.withdraw()  # Hide initially

# Create output text widget
output_text = scrolledtext.ScrolledText(output_window, wrap=tk.WORD)
output_text.pack(expand=True, fill='both')

# Close button for output window
close_button = tk.Button(output_window, text="Close", command=close_output_window)
close_button.pack()

# Start the tkinter event loop
root.mainloop()
