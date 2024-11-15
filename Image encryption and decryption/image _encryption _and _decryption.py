import os
import numpy as np
from tkinter import Tk, Label, Button, StringVar, filedialog, Entry
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

def pad(data, block_size=16):
    padding_len = block_size - (len(data) % block_size)
    return data + bytes([padding_len] * padding_len)

def unpad(data):
    padding_len = data[-1]
    if padding_len > 16:
        raise ValueError("Invalid padding encountered.")
    return data[:-padding_len]

def encrypt_image(image_path, output_path, password):
    try:
        # Convert the image to bytes
        image = Image.open(image_path).convert("RGB")
        width, height = image.size
        image_data = np.array(image)
        image_bytes = image_data.tobytes()

        # Generate a random salt and derive a key and IV
        salt = get_random_bytes(16)
        key = PBKDF2(password, salt, dkLen=32)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Encrypt the image data with padding
        encrypted_data = cipher.encrypt(pad(image_bytes))

        # Save the salt, iv, dimensions, and encrypted data to the output file
        with open(output_path, "wb") as f:
            f.write(salt + iv)
            f.write(width.to_bytes(4, 'big') + height.to_bytes(4, 'big'))
            f.write(encrypted_data)

        status.set(f"Encrypted image saved at {output_path}")
    except Exception as e:
        status.set(f"Encryption error: {e}")

def decrypt_image(image_path, output_path, password):
    try:
        with open(image_path, "rb") as f:
            # Read salt, iv, width, and height from the file
            salt = f.read(16)
            iv = f.read(16)
            width = int.from_bytes(f.read(4), 'big')
            height = int.from_bytes(f.read(4), 'big')
            encrypted_data = f.read()

        # Derive the key from the password and salt
        key = PBKDF2(password, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt and unpad the data
        decrypted_data = unpad(cipher.decrypt(encrypted_data))

        # Convert decrypted data back to image format
        image_array = np.frombuffer(decrypted_data, dtype=np.uint8).reshape((height, width, 3))
        decrypted_image = Image.fromarray(image_array)
        decrypted_image.save(output_path)

        status.set(f"Decrypted image saved at {output_path}")
    except ValueError as ve:
        status.set(f"Decryption error (possibly wrong password): {ve}")
    except Exception as e:
        status.set(f"General decryption error: {e}")

def process_image(mode):
    if not image_path.get():
        status.set("Please select or drop an image file.")
        return
    if not password.get():
        status.set("Please enter a password.")
        return

    base_filename = os.path.basename(image_path.get())
    if mode == 'e':
        output_default = "encrypted_" + base_filename + ".enc"
        output_path = filedialog.asksaveasfilename(defaultextension=".enc",
                                                   initialfile=output_default,
                                                   filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")])
        if output_path:
            encrypt_image(image_path.get(), output_path, password.get())
    elif mode == 'd':
        output_default = "decrypted_" + base_filename.replace(".enc", ".png")
        output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                   initialfile=output_default,
                                                   filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if output_path:
            decrypt_image(image_path.get(), output_path, password.get())

def on_drop(event):
    image_path.set(event.data)
    status.set("File selected: " + event.data)

def select_image():
    file_types = [("Image and Encrypted files", "*.png;*.jpg;*.jpeg;*.bmp;*.enc"), ("All files", "*.*")]
    file_path = filedialog.askopenfilename(filetypes=file_types)
    if file_path:
        image_path.set(file_path)
        status.set("File selected: " + file_path)

root = TkinterDnD.Tk()
root.title("AES Image Encryptor/Decryptor")
root.geometry("400x300")

Label(root, text="Drag and Drop an Image or Select File").pack(pady=10)
image_path = StringVar()
Label(root, textvariable=image_path, wraplength=300).pack()
Button(root, text="Select Image", command=select_image).pack(pady=5)

Label(root, text="Enter Password:").pack()
password = StringVar()
Entry(root, textvariable=password, show="*").pack()

status = StringVar()
Label(root, textvariable=status, wraplength=300, fg="blue").pack(pady=10)

Button(root, text="Encrypt and Save As", command=lambda: process_image('e')).pack(side="left", padx=10, pady=10)
Button(root, text="Decrypt and Save As", command=lambda: process_image('d')).pack(side="right", padx=10, pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

root.mainloop()

#follow for more
#github-paradox_suraj