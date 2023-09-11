import tkinter as tk
import qrcode
from PIL import ImageTk, Image
from pyzbar.pyzbar import decode
from tkinter import messagebox, filedialog


class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator and Scanner")
        self.text_zoom_level = 1.0
        self.hidden_message = ""

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()

        self.data_label = tk.Label(self.frame, text="Enter secret message:")
        self.data_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.data_entry = tk.Entry(self.frame, show="*")
        self.data_entry.grid(row=0, column=1, padx=10, pady=10)

        self.generate_button = tk.Button(self.frame, text="Generate Hidden QR Code", command=self.generate_hidden_qr_code)
        self.generate_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.scan_button = tk.Button(self.frame, text="Scan QR Code", command=self.scan_qr_code)
        self.scan_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.save_button = tk.Button(self.frame, text="Save QR Code Image", command=self.save_qr_code_image)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.qr_code_label = tk.Label(root)
        self.qr_code_label.pack()

        # Bind the mouse wheel event to the text zoom function
        self.root.bind("<Control-MouseWheel>", self.zoom_text)

    def generate_hidden_qr_code(self):
        self.hidden_message = self.data_entry.get()

        if self.hidden_message:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(self.hidden_message)
            qr.make(fit=True)

            qr_image = qr.make_image(fill_color="black", back_color="white")

            qr_image_pil = ImageTk.PhotoImage(qr_image)
            self.qr_code_label.config(image=qr_image_pil)
            self.qr_code_label.image = qr_image_pil

            # Store the QR code image for saving later
            self.qr_image = qr_image
        else:
            messagebox.showinfo("QR Code Generation", "Please enter a hidden message!")

    def scan_qr_code(self):
        qr_code_path = filedialog.askopenfilename(title="Select QR Code Image",
                                                  filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])

        if qr_code_path:
            qr_image = Image.open(qr_code_path)
            decoded_objects = decode(qr_image)

            if decoded_objects:
                decoded_data = decoded_objects[0].data.decode("utf-8")
                if decoded_data == self.hidden_message:
                    messagebox.showinfo("QR Code Scan Result", f"Hidden Message: {decoded_data}")
                else:
                    messagebox.showinfo("QR Code Scan Result", "Invalid QR code!")
            else:
                messagebox.showinfo("QR Code Scan Result", "No QR code found!")

    def save_qr_code_image(self):
        if hasattr(self, "qr_image"):
            qr_image_path = filedialog.asksaveasfilename(title="Save QR Code Image", defaultextension=".png",
                                                         filetypes=[("PNG files", "*.png")])
            if qr_image_path:
                # Save the QR code image using the PIL (Pillow) library
                self.qr_image.save(qr_image_path, "PNG")
                messagebox.showinfo("QR Code Image Saved", "QR Code image saved successfully!")

    # Event handler for zooming text using the control key and mouse wheel
    def zoom_text(self, event):
        if event.delta > 0:
            self.text_zoom_level += 0.1
        else:
            self.text_zoom_level -= 0.1
        self.update_text_zoom()

    # Update the text labels with the current zoom level
    def update_text_zoom(self):
        font_size = int(12 * self.text_zoom_level)
        self.data_label.config(font=("Helvetica", font_size))
        self.generate_button.config(font=("Helvetica", font_size))
        self.scan_button.config(font=("Helvetica", font_size))
        self.save_button.config(font=("Helvetica", font_size))


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
