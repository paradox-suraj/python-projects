
import tkinter as tk
from tkinter import ttk, messagebox

# Utility Functions
def decimal_to_binary(n):
    return bin(n)[2:]

def decimal_to_octal(n):
    return oct(n)[2:]

def decimal_to_hex(n):
    return hex(n)[2:].upper()

def binary_to_decimal(b):
    return int(b, 2)

def octal_to_decimal(o):
    return int(o, 8)

def hex_to_decimal(h):
    return int(h, 16)

def binary_to_gray(b):
    b = int(b, 2)
    gray = b ^ (b >> 1)
    return bin(gray)[2:]

def decimal_to_bcd(n):
    bcd = ""
    for digit in str(n):
        bcd += f"{int(digit):04b} "
    return bcd.strip()

def binary_addition(b1, b2):
    return bin(int(b1, 2) + int(b2, 2))[2:]

def binary_subtraction(b1, b2):
    result = int(b1, 2) - int(b2, 2)
    if result < 0:
        return f"-{bin(-result)[2:]}"
    return bin(result)[2:]

# GUI Implementation
class NumberSystemConverterUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Number System Converter")
        self.master.geometry("400x400")
        self.master.configure(bg="#f0f8ff")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(pady=10, expand=True)

        self.dec_frame = tk.Frame(self.notebook, bg="#add8e6")
        self.bin_frame = tk.Frame(self.notebook, bg="#add8e6")
        self.oct_frame = tk.Frame(self.notebook, bg="#add8e6")
        self.hex_frame = tk.Frame(self.notebook, bg="#add8e6")
        self.gray_frame = tk.Frame(self.notebook, bg="#add8e6")
        self.bcd_frame = tk.Frame(self.notebook, bg="#add8e6")
        self.binary_add_frame = tk.Frame(self.notebook, bg="#add8e6")
        self.binary_sub_frame = tk.Frame(self.notebook, bg="#add8e6")

        self.notebook.add(self.dec_frame, text="Decimal to Binary/Octal/Hexadecimal")
        self.notebook.add(self.bin_frame, text="Binary to Decimal")
        self.notebook.add(self.oct_frame, text="Octal to Decimal")
        self.notebook.add(self.hex_frame, text="Hexadecimal to Decimal")
        self.notebook.add(self.gray_frame, text="Binary to Gray Code")
        self.notebook.add(self.bcd_frame, text="Decimal to BCD")
        self.notebook.add(self.binary_add_frame, text="Binary Addition")
        self.notebook.add(self.binary_sub_frame, text="Binary Subtraction")

        self.dec_to_bin_oct_hex()
        self.bin_to_dec()
        self.oct_to_dec()
        self.hex_to_dec()
        self.bin_to_gray()
        self.dec_to_bcd()
        self.binary_add()
        self.binary_sub()

    def dec_to_bin_oct_hex(self):
        tk.Label(self.dec_frame, text="Enter decimal number:", bg="#add8e6").pack(pady=5)
        self.dec_entry = tk.Entry(self.dec_frame, width=30)
        self.dec_entry.pack(pady=5)

        tk.Button(self.dec_frame, text="Convert", command=self.dec_to_bin_oct_hex_convert, bg="#90ee90").pack(pady=5)
        self.bin_oct_hex_label = tk.Label(self.dec_frame, text="", bg="#add8e6")
        self.bin_oct_hex_label.pack(pady=5)

        tk.Button(self.dec_frame, text="Copy", command=lambda: self.copy(self.bin_oct_hex_label.cget("text")), bg="#ffcccb").pack(pady=5)

    def dec_to_bin_oct_hex_convert(self):
        num = self.dec_entry.get()
        try:
            num = int(num)
            bin_num = decimal_to_binary(num)
            oct_num = decimal_to_octal(num)
            hex_num = decimal_to_hex(num)
            self.bin_oct_hex_label.config(text=f"Binary: {bin_num}\nOctal: {oct_num}\nHexadecimal: {hex_num}")
        except ValueError:
            self.bin_oct_hex_label.config(text="Please enter a valid decimal number")

    def bin_to_dec(self):
        tk.Label(self.bin_frame, text="Enter binary number:", bg="#add8e6").pack(pady=5)
        self.bin_entry = tk.Entry(self.bin_frame, width=30)
        self.bin_entry.pack(pady=5)

        tk.Button(self.bin_frame, text="Convert", command=self.bin_to_dec_convert, bg="#90ee90").pack(pady=5)

        self.bin_dec_label = tk.Label(self.bin_frame, text="", bg="#add8e6")
        self.bin_dec_label.pack(pady=5)

        tk.Button(self.bin_frame, text="Copy", command=lambda: self.copy(self.bin_dec_label.cget("text")), bg="#ffcccb").pack(pady=5)

    def bin_to_dec_convert(self):
        bin_num = self.bin_entry.get()
        try:
            dec_num = binary_to_decimal(bin_num)
            self.bin_dec_label.config(text=f"Decimal: {dec_num}")
        except ValueError:
            self.bin_dec_label.config(text="Please enter a valid binary number")

    def oct_to_dec(self):
        tk.Label(self.oct_frame, text="Enter octal number:", bg="#add8e6").pack(pady=5)
        self.oct_entry = tk.Entry(self.oct_frame, width=30)
        self.oct_entry.pack(pady=5)

        tk.Button(self.oct_frame, text="Convert", command=self.oct_to_dec_convert, bg="#90ee90").pack(pady=5)

        self.oct_dec_label = tk.Label(self.oct_frame, text="", bg="#add8e6")
        self.oct_dec_label.pack(pady=5)

        tk.Button(self.oct_frame, text="Copy", command=lambda: self.copy(self.oct_dec_label.cget("text")), bg="#ffcccb").pack(pady=5)

    def oct_to_dec_convert(self):
        oct_num = self.oct_entry.get()
        try:
            dec_num = octal_to_decimal(oct_num)
            self.oct_dec_label.config(text=f"Decimal: {dec_num}")
        except ValueError:
            self.oct_dec_label.config(text="Please enter a valid octal number")

    def hex_to_dec(self):
        tk.Label(self.hex_frame, text="Enter hexadecimal number:", bg="#add8e6").pack(pady=5)
        self.hex_entry = tk.Entry(self.hex_frame, width=30)
        self.hex_entry.pack(pady=5)

        tk.Button(self.hex_frame, text="Convert", command=self.hex_to_dec_convert, bg="#90ee90").pack(pady=5)

        self.hex_dec_label = tk.Label(self.hex_frame, text="", bg="#add8e6")
        self.hex_dec_label.pack(pady=5)

        tk.Button(self.hex_frame, text="Copy", command=lambda: self.copy(self.hex_dec_label.cget("text")), bg="#ffcccb").pack(pady=5)

    def hex_to_dec_convert(self):
        hex_num = self.hex_entry.get()
        try:
            dec_num = hex_to_decimal(hex_num)
            self.hex_dec_label.config(text=f"Decimal: {dec_num}")
        except ValueError:
            self.hex_dec_label.config(text="Please enter a valid hexadecimal number")

    def bin_to_gray(self):
        tk.Label(self.gray_frame, text="Enter binary number:", bg="#add8e6").pack(pady=5)
        self.gray_entry = tk.Entry(self.gray_frame, width=30)
        self.gray_entry.pack(pady=5)

        tk.Button(self.gray_frame, text="Convert", command=self.bin_to_gray_convert, bg="#90ee90").pack(pady=5)

        self.gray_label = tk.Label(self.gray_frame, text="", bg="#add8e6")
        self.gray_label.pack(pady=5)

        tk.Button(self.gray_frame, text="Copy", command=lambda: self.copy(self.gray_label.cget("text")), bg="#ffcccb").pack(pady=5)

    def bin_to_gray_convert(self):
        bin_num = self.gray_entry.get()
        try:
            gray_num = binary_to_gray(bin_num)
            self.gray_label.config(text=f"Gray Code: {gray_num}")
        except ValueError:
            self.gray_label.config(text="Please enter a valid binary number")

    def dec_to_bcd(self):
        tk.Label(self.bcd_frame, text="Enter decimal number:", bg="#add8e6").pack(pady=5)
        self.bcd_entry = tk.Entry(self.bcd_frame, width=30)
        self.bcd_entry.pack(pady=5)

        tk.Button(self.bcd_frame, text="Convert", command=self.dec_to_bcd_convert, bg="#90ee90").pack(pady=5)

        self.bcd_label = tk.Label(self.bcd_frame, text="", bg="#add8e6")
        self.bcd_label.pack(pady=5)

        tk.Button(self.bcd_frame, text="Copy", command=lambda: self.copy(self.bcd_label.cget("text")), bg="#ffcccb").pack(pady=5)

    def dec_to_bcd_convert(self):
        dec_num = self.bcd_entry.get()
        try:
            dec_num = int(dec_num)
            bcd_num = decimal_to_bcd(dec_num)
            self.bcd_label.config(text=f"BCD: {bcd_num}")
        except ValueError:
            self.bcd_label.config(text="Please enter a valid decimal number")

    def binary_add(self):
        tk.Label(self.binary_add_frame, text="Enter first binary number:", bg="#add8e6").pack(pady=5)
        self.binary_add_entry1 = tk.Entry(self.binary_add_frame, width=30)
        self.binary_add_entry1.pack(pady=5)

        tk.Label(self.binary_add_frame, text="Enter second binary number:", bg="#add8e6").pack(pady=5)
        self.binary_add_entry2 = tk.Entry(self.binary_add_frame, width=30)
        self.binary_add_entry2.pack(pady=5)

        tk.Button(self.binary_add_frame, text="Add", command=self.binary_add_convert, bg="#90ee90").pack(pady=5)

        self.binary_add_label = tk.Label(self.binary_add_frame, text="", bg="#add8e6")
        self.binary_add_label.pack(pady=5)

        tk.Button(self.binary_add_frame, text="Copy", command=lambda: self.copy(self.binary_add_label.cget("text")), bg="#ffcccb").pack(pady=5)

    def binary_add_convert(self):
        bin1 = self.binary_add_entry1.get()
        bin2 = self.binary_add_entry2.get()
        try:
            result = binary_addition(bin1, bin2)
            self.binary_add_label.config(text=f"Sum: {result}")
        except ValueError:
            self.binary_add_label.config(text="Please enter valid binary numbers")

    def binary_sub(self):
        tk.Label(self.binary_sub_frame, text="Enter first binary number:", bg="#add8e6").pack(pady=5)
        self.binary_sub_entry1 = tk.Entry(self.binary_sub_frame, width=30)
        self.binary_sub_entry1.pack(pady=5)

        tk.Label(self.binary_sub_frame, text="Enter second binary number:", bg="#add8e6").pack(pady=5)
        self.binary_sub_entry2 = tk.Entry(self.binary_sub_frame, width=30)
        self.binary_sub_entry2.pack(pady=5)

        tk.Button(self.binary_sub_frame, text="Subtract", command=self.binary_sub_convert, bg="#90ee90").pack(pady=5)

        self.binary_sub_label = tk.Label(self.binary_sub_frame, text="", bg="#add8e6")
        self.binary_sub_label.pack(pady=5)

        tk.Button(self.binary_sub_frame, text="Copy", command=lambda: self.copy(self.binary_sub_label.cget("text")), bg="#ffcccb").pack(pady=5)

    def binary_sub_convert(self):
        bin1 = self.binary_sub_entry1.get()
        bin2 = self.binary_sub_entry2.get()
        try:
            result = binary_subtraction(bin1, bin2)
            self.binary_sub_label.config(text=f"Difference: {result}")
        except ValueError:
            self.binary_sub_label.config(text="Please enter valid binary numbers")

    def copy(self, text):
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        self.master.update()

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberSystemConverterUI(root)
    root.mainloop()