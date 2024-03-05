import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def encrypt_image():
    global img_path
    key = key_entry.get()

    if not img_path or not key:
        messagebox.showerror("Error", "Please select an image and enter a key.")
        return

    try:
        key = tuple(map(int, key.split(',')))
    except ValueError:
        messagebox.showerror("Error", "Invalid key format. Please enter comma-separated integers.")
        return

    try:
        image = Image.open(img_path)
        width, height = image.size
        image = image.convert('RGB')
    except Exception as e:
        messagebox.showerror("Error", f"Error opening image: {str(e)}")
        return

    encrypted_pixels = []
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            encrypted_pixel = tuple((pixel[i] + key[i]) % 256 for i in range(3))
            encrypted_pixels.append(encrypted_pixel)

    encrypted_image = Image.new('RGB', (width, height))
    encrypted_image.putdata(encrypted_pixels)

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        encrypted_image.save(save_path)
        messagebox.showinfo("Success", "Image encrypted successfully.")

def decrypt_image():
    global img_path
    key = key_entry.get()

    if not img_path or not key:
        messagebox.showerror("Error", "Please select an image and enter a key.")
        return

    try:
        key = tuple(map(int, key.split(',')))
    except ValueError:
        messagebox.showerror("Error", "Invalid key format. Please enter comma-separated integers.")
        return

    try:
        encrypted_image = Image.open(img_path)
        width, height = encrypted_image.size
    except Exception as e:
        messagebox.showerror("Error", f"Error opening encrypted image: {str(e)}")
        return

    decrypted_pixels = []
    for y in range(height):
        for x in range(width):
            pixel = encrypted_image.getpixel((x, y))
            decrypted_pixel = tuple((pixel[i] - key[i]) % 256 for i in range(3))
            decrypted_pixels.append(decrypted_pixel)

    decrypted_image = Image.new('RGB', (width, height))
    decrypted_image.putdata(decrypted_pixels)

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        decrypted_image.save(save_path)
        messagebox.showinfo("Success", "Image decrypted successfully.")

def select_image():
    global img_path
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if img_path:
        img_label.config(text=f"Selected Image: {img_path}")

# Create the main window
root = tk.Tk()
root.title("Image Encryption Tool")

# Global variable to store the path of the selected image
img_path = ""

# UI elements
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

img_label = tk.Label(root, text="Selected Image: None")
img_label.pack()

key_label = tk.Label(root, text="Encryption/Decryption Key (comma-separated integers):")
key_label.pack(pady=5)

key_entry = tk.Entry(root)
key_entry.pack(pady=5)

encrypt_button = tk.Button(root, text="Encrypt Image", command=encrypt_image)
encrypt_button.pack(pady=5)

decrypt_button = tk.Button(root, text="Decrypt Image", command=decrypt_image)
decrypt_button.pack(pady=5)

root.mainloop()
