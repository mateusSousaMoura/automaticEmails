import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import PhotoImage
import subprocess
import pathlib

# Set the base directory to the folder where the script is located
BASE_DIR = pathlib.Path(__file__).parent.resolve()
INPUT_FILE_PATH = BASE_DIR / "input.txt"
OUTPUT_FILE_PATH = BASE_DIR / "output.txt"
EMAIL_SCRIPT_PATH = BASE_DIR / "emailSend.py"
EMAIL_GENERATE_SCRIPT_PATH = BASE_DIR / "emailGenerate.py"
MODELS_DIR = BASE_DIR / "models"
IMAGE_PATH = BASE_DIR / "dracoLogo.png"  # Replace with the actual image filename

# Ensure the models directory exists
MODELS_DIR.mkdir(exist_ok=True)

# Function to load the content of input.txt into the text box
def load_file(path, box):
    try:
        with open(path, "r") as file:
            content = file.read()
        box.delete("1.0", tk.END)  # Clear existing content
        box.insert(tk.END, content)  # Insert new content
    except FileNotFoundError:
        INPUT_FILE_PATH.touch()  # Create an empty file if it doesn't exist

# Function to save modifications to input.txt
def save_file():
    with open(INPUT_FILE_PATH, "w") as file:
        file.write(text_box.get("1.0", tk.END).strip())

# Function to run emailSend.py
def run_email_send():
    try:
        # Run emailSend.py from the script's directory
        result = subprocess.run(['python', EMAIL_SCRIPT_PATH], capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Email Sent", "Emails enviados com sucesso!")
        else:
            messagebox.showerror("Error", f"Error running emailSend.py:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run emailSend.py:\n{e}")

def run_email_generate():
    try:
        # Run emailSend.py from the script's directory
        result = subprocess.run(['python', EMAIL_GENERATE_SCRIPT_PATH], capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Email Sent", "Emails enviados com sucesso!")
        else:
            messagebox.showerror("Error", f"Error running emailGenerate.py:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run emailGenerate.py:\n{e}")

# Function to create a new email model
def create_model():
    model_name = simpledialog.askstring("Model Name", "Enter the name of the new model:")
    if model_name:
        model_file_path = MODELS_DIR / f"{model_name}.txt"
        with open(model_file_path, "w") as file:
            file.write(text_box.get("1.0", tk.END).strip())  # Save the current text box content as the model
        update_model_list()  # Refresh the model list in the combo box

# Function to delete the selected model
def delete_model():
    selected_model = model_combo.get()
    if selected_model:
        model_file_path = MODELS_DIR / f"{selected_model}.txt"
        try:
            model_file_path.unlink()  # Delete the model file
            update_model_list()  # Refresh the model list in the combo box
            text_box.delete("1.0", tk.END)  # Clear the text box
        except FileNotFoundError:
            messagebox.showerror("Error", f"Model '{selected_model}' not found.")

def update_model():
    selected_model = model_combo.get()
    if selected_model:
        if selected_model:
            model_file_path = MODELS_DIR / f"{selected_model}.txt"
            try:
                open(model_file_path, 'w').close() # Clear the text box
                with open(model_file_path, "w") as file:
                    file.write(text_box.get("1.0", tk.END).strip())
                update_model_list()
            except FileNotFoundError:
                messagebox.showerror("Error", f"Model '{selected_model}' not found.")


# Function to update the model list in the combo box
def update_model_list():
    model_combo['values'] = [model.stem for model in MODELS_DIR.glob("*.txt")]  # Load model names without extensions
    model_combo.set("")  # Clear the combo box selection

# Function to load a selected model into input.txt and update the text box
def load_model(event=None):
    selected_model = model_combo.get()
    if selected_model:
        model_file_path = MODELS_DIR / f"{selected_model}.txt"
        try:
            with open(model_file_path, "r") as file:
                content = file.read()
            text_box.delete("1.0", tk.END)  # Clear existing content
            text_box.insert(tk.END, content)  # Insert new content
            save_file()  # Save the model content to input.txt
        except FileNotFoundError:
            messagebox.showerror("Error", f"Model '{selected_model}' not found.")

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Email Manager")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")  # Cover the entire screen
root.overrideredirect(False)

# Create a frame for the top image
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X)

# Load and display an image at the top
try:
    image = PhotoImage(file=str(IMAGE_PATH))  # Convert the path to string for compatibility
    image_label = tk.Label(top_frame, image=image)
    image_label.pack()
except Exception as e:
    messagebox.showerror("Error", f"Could not load image:\n{e}")

# Create a frame for the left side (buttons and combo box)
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Combo box to select email models
model_combo = ttk.Combobox(left_frame, state="readonly", width=30)
model_combo.pack(pady=5)
model_combo.bind("<<ComboboxSelected>>", load_model)  # Bind selection event to load_model
update_model_list()  # Populate the combo box with available models

# Button to create a new model
create_model_button = tk.Button(left_frame, text="Criar Modelo", command=create_model, width=20)
create_model_button.pack(pady=5)

# Button to delete the selected model
delete_model_button = tk.Button(left_frame, text="Apagar Modelo", command=delete_model, width=20)
delete_model_button.pack(pady=5)

#button to update the selected model
update_model_button = tk.Button(left_frame, text="Atualizar Modelo", command= update_model, width=20)
update_model_button.pack(pady=5)

# Button to save changes to input.txt
save_button = tk.Button(left_frame, text="Carregar o modelo", command=save_file, width=20)
save_button.pack(pady=5)

# Botão para gerar o conteúdo do email
generate_button = tk.Button(left_frame, text="Gerar email", command=run_email_send, width=20)
generate_button.pack(pady=5)

# Button to run emailSend.py
send_button = tk.Button(left_frame, text="Enviar Email", command=run_email_send, width=20)
send_button.pack(pady=5)

# Create a frame for the right side (text editor)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Label for instructions
# instructions = tk.Label(right_frame, text="Edite o template do modelo:", font=15)
# instructions.pack(pady=5)

right_frame = tk.Frame(root)
right_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_box = tk.Text(right_frame, wrap=tk.WORD, height=5, width=40, yscrollcommand=scrollbar.set)
text_box.pack(side= tk.LEFT, pady=(5, 5), padx=(10, 10), fill=tk.BOTH, expand=True)


output_box = tk.Text(right_frame, wrap=tk.WORD, height=5, width=40, yscrollcommand=scrollbar.set)
output_box.pack(side= tk.RIGHT, pady=(5, 5), padx=(10, 10), fill=tk.BOTH, expand=True)

# text_box.config(yscrollcommand=scrollbar.set)
# output_box.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=lambda *args: (text_box.yview(*args), output_box.yview(*args)))


# Load content from input.txt into text_box
load_file(INPUT_FILE_PATH, text_box)
load_file(OUTPUT_FILE_PATH, output_box)

# Run the Tkinter event loop
root.mainloop()
