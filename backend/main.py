import sys
import os


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QTabWidget, QPushButton, QLabel, QFileDialog,
                             QMessageBox, QLineEdit, QHBoxLayout, QFrame, QScrollArea)
from api import (
    hideTextInLSB,
    mixTwoImagesMagic,
    getTextFromLSB,
    mixColorChannels,
    separateColorChannels,
    hideTextByMakingImageLarger,
    getTextFromLargeImage
)


class LSBTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Main scrollable area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Description label
        description_label = QLabel("""
        <h2>LSB Text Hider</h2>
        <p>Hide your secret messages in image files using the Least Significant Bit (LSB) technique.<br>
        Select an image, type your message, and save the modified image securely!</p>
        """)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-weight: bold; background: transparent; border: none;")

        # Message input
        self.message_field = QLineEdit()
        self.message_field.setPlaceholderText("Enter message to hide")
        self.message_field.setToolTip("Type the secret message you want to embed into the image")
        self.message_field.setFixedSize(400, 40)  # Adjusted size for a larger and wider input field
        self.message_field.setStyleSheet("padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")

        # File selection button
        self.file_button = QPushButton("Select Image File")
        self.file_button.setFixedSize(200, 30)
        self.file_button.setToolTip("Click to choose an image file to hide the message")
        self.file_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.file_button.clicked.connect(self.select_file)

        # Process button
        self.start_button = QPushButton("Hide Message")
        self.start_button.setFixedSize(200, 30)
        self.start_button.setToolTip("Start the process of embedding the message into the selected image")
        self.start_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.start_button.clicked.connect(self.start_hiding_process)

        # Download button
        self.download_button = QPushButton("Download Result")
        self.download_button.setFixedSize(200, 30)
        self.download_button.setToolTip("Save the modified image with the hidden message")
        self.download_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        # Image box with centered layout
        self.image_box = QFrame()
        self.image_box.setFrameStyle(QFrame.Box)
        self.image_box.setLineWidth(2)
        self.image_box.setStyleSheet("background-color: white;")
        self.image_box.setFixedSize(550, 450)  # Adjusted size for a larger box

        # Centering layout for the image inside the box
        image_box_layout = QVBoxLayout(self.image_box)
        image_box_layout.setAlignment(Qt.AlignCenter)  # Ensure the image is centered both vertically and horizontally

        # Image preview label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(480, 380)  # Slightly smaller than the box
        self.image_label.hide()

        # Add the image_label to the box's layout
        image_box_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Status label
        self.status_label = QLabel("Select a file and enter message")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #333; border: none; background: transparent;")

        # Add widgets to the scroll layout
        scroll_layout.addWidget(description_label)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.message_field, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.file_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.download_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.image_box, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.status_label)

        # Set the scroll area's widget to the scroll content
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        # Add the scroll area to the main layout
        layout.addWidget(scroll_area)
        self.setLayout(layout)

        # Set overall style
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                background-color: white;
                color: black;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:disabled {
                background-color: #ddd;
                color: #666;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                margin: 5px 0;
            }
            QFrame {
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Internal attributes
        self.file_path = None
        self.finished_file_path = None

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                   "Images (*.png *.jpg)", options=options)
        if file_path:
            self.file_path = file_path
            self.status_label.setText(f"Selected: {file_path}")

    def start_hiding_process(self):
        if not self.file_path or not self.message_field.text():
            QMessageBox.warning(self, "Error", "Please provide an image and message")
            return

        try:
            # Generate the output image with hidden text
            self.finished_file_path = "res.png"
            hideTextInLSB(self.file_path, self.message_field.text())  # Ensure the function saves to "res.png"

            # Display the processed image
            pixmap = QPixmap(self.finished_file_path)
            if pixmap.isNull():
                print("Error: Unable to load the processed image.")
            else:
                self.image_label.setPixmap(pixmap)
                self.image_label.show()

            self.status_label.setText("Process completed. You can now download the result.")
            self.download_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def download_file(self):
        if not self.finished_file_path:
            QMessageBox.warning(self, "Error", "No processed file available")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Result", "",
                                                   "Images (*.png *.jpg)")
        if save_path:
            try:
                os.replace(self.finished_file_path, save_path)
                self.status_label.setText(f"Saved to: {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))


    def download_file(self):
        if not self.finished_file_path:
            QMessageBox.warning(self, "Error", "No processed file available")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Result", "",
                                                   "Images (*.png *.jpg)")
        if save_path:
            try:
                os.replace(self.finished_file_path, save_path)
                self.status_label.setText(f"Saved to: {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

class RGBTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Main scrollable area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Description label
        description_label = QLabel("""
        <h2>RGB Channel Combination</h2>
        <p>Select separate images for the Red, Green, and Blue channels,<br>
        combine them to create a full RGB image, and save the result!</p>
        """)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-weight: bold; background: transparent; border: none;")

        # File selection buttons
        self.red_button = QPushButton("Select Red Channel")
        self.green_button = QPushButton("Select Green Channel")
        self.blue_button = QPushButton("Select Blue Channel")

        for btn in [self.red_button, self.green_button, self.blue_button]:
            btn.setFixedSize(200, 30)
            btn.setStyleSheet("padding: 8px; font-size: 14px;")

        self.red_button.setToolTip("Select an image file for the Red channel")
        self.green_button.setToolTip("Select an image file for the Green channel")
        self.blue_button.setToolTip("Select an image file for the Blue channel")

        self.red_button.clicked.connect(lambda: self.select_file('red'))
        self.green_button.clicked.connect(lambda: self.select_file('green'))
        self.blue_button.clicked.connect(lambda: self.select_file('blue'))

        # Process button
        self.start_button = QPushButton("Combine Channels")
        self.start_button.setFixedSize(200, 30)
        self.start_button.setToolTip("Combine the selected RGB channel images")
        self.start_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.start_button.clicked.connect(self.start_rgb_process)

        # Download button
        self.download_button = QPushButton("Download Result")
        self.download_button.setFixedSize(200, 30)
        self.download_button.setToolTip("Save the combined RGB image")
        self.download_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        # Image box with centered layout
        self.image_box = QFrame()
        self.image_box.setFrameStyle(QFrame.Box)
        self.image_box.setLineWidth(2)
        self.image_box.setStyleSheet("background-color: white;")
        self.image_box.setFixedSize(550, 450)  # Adjusted size for a larger box

        # Centering layout for the image inside the box
        image_box_layout = QVBoxLayout(self.image_box)
        image_box_layout.setAlignment(Qt.AlignCenter)

        # Image preview label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(480, 380)  # Slightly smaller than the box
        self.image_label.hide()

        # Add the image_label to the box's layout
        image_box_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Status label
        self.status_label = QLabel("Select RGB channel images")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #333; border: none; background: transparent;")

        # Add widgets to the scroll layout
        scroll_layout.addWidget(description_label)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.red_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(5)
        scroll_layout.addWidget(self.green_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(5)
        scroll_layout.addWidget(self.blue_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.download_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.image_box, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.status_label)

        # Set the scroll area's widget to the scroll content
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        # Add the scroll area to the main layout
        layout.addWidget(scroll_area)
        self.setLayout(layout)

        # Set overall style
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                background-color: white;
                color: black;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:disabled {
                background-color: #ddd;
                color: #666;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                margin: 5px 0;
            }
            QFrame {
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Internal attributes
        self.channels = {'red': None, 'green': None, 'blue': None}
        self.finished_file_path = None

    def select_file(self, channel):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, f"Select {channel.title()} Channel", 
                                                 "", "Images (*.png *.jpg)", options=options)
        if file_path:
            self.channels[channel] = file_path
            self.status_label.setText(f"Selected {channel} channel: {file_path}")

    def start_rgb_process(self):
        if not all(self.channels.values()):
            QMessageBox.warning(self, "Error", "Please select all channels")
            return

        try:
            self.finished_file_path = mixColorChannels(
                self.channels['red'],
                self.channels['green'],
                self.channels['blue']
            )
            self.status_label.setText("Channels combined successfully")
            self.download_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def download_file(self):
        if not self.finished_file_path:
            QMessageBox.warning(self, "Error", "No processed file available")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Result", "", 
                                                 "Images (*.png *.jpg)")
        if save_path:
            try:
                os.replace(self.finished_file_path, save_path)
                self.status_label.setText(f"Saved to: {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

class MagicTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Main scrollable area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Description label
        description_label = QLabel("""
        <h2>Magic Combination</h2>
        <p>Combine two images to create a magical result!<br>
        One image appears on light backgrounds, and the other on dark backgrounds.<br>
        Select two images, and let the magic happen!</p>
        """)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet(
            "font-weight: bold; background: transparent; border: none;")  # No border or background

        # File selection buttons
        self.image1_button = QPushButton("Select First Image")
        self.image2_button = QPushButton("Select Second Image")

        for btn in [self.image1_button, self.image2_button]:
            btn.setFixedSize(200, 30)
            btn.setToolTip("Click to select an image file")

        self.image1_button.clicked.connect(lambda: self.select_file(1))
        self.image2_button.clicked.connect(lambda: self.select_file(2))

        # Process button
        self.start_button = QPushButton("Combine Images")
        self.start_button.setFixedSize(200, 30)
        self.start_button.setToolTip("Combine the two selected images")
        self.start_button.clicked.connect(self.start_magic_process)

        # Download button
        self.download_button = QPushButton("Download Result")
        self.download_button.setFixedSize(200, 30)
        self.download_button.setToolTip("Save the combined image to your computer")
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        # Image box with centered layout
        self.image_box = QFrame()
        self.image_box.setFrameStyle(QFrame.Box)
        self.image_box.setLineWidth(2)
        self.image_box.setStyleSheet("background-color: white;")
        self.image_box.setFixedSize(550, 450)  # Adjusted size for a larger box

        # Centering layout for the image inside the box
        image_box_layout = QVBoxLayout(self.image_box)
        image_box_layout.setAlignment(Qt.AlignCenter)  # Ensure the image is centered both vertically and horizontally

        # Image preview label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(480, 380)  # Slightly smaller than the box
        self.image_label.hide()

        # Add the image_label to the box's layout
        image_box_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Toggle background button
        self.toggle_background_button = QPushButton("Toggle Box Background")
        self.toggle_background_button.setFixedSize(200, 30)
        self.toggle_background_button.setToolTip("Toggle the box background color between white and black")
        self.toggle_background_button.clicked.connect(self.toggle_box_background)
        self.toggle_background_button.hide()

        # Status label
        self.status_label = QLabel("Select two images to combine")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #333; border: none; background: transparent;")

        # Add widgets to the scroll layout
        scroll_layout.addWidget(description_label)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.image1_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(5)
        scroll_layout.addWidget(self.image2_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(5)
        scroll_layout.addWidget(self.download_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.image_box, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(5)
        scroll_layout.addWidget(self.toggle_background_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.status_label)

        # Set the scroll area's widget to the scroll content
        scroll_area.setWidget(scroll_content)

        # Add the scroll area to the main layout
        layout.addWidget(scroll_area)
        self.setLayout(layout)

        # Set overall style
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                background-color: white;
                color: black;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:disabled {
                background-color: #ddd;
                color: #666;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                margin: 5px 0;
            }
            QFrame {
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Internal attributes
        self.images = {1: None, 2: None}
        self.finished_file_path = None
        self.current_box_background = "white"  # Default background for the box

    def select_file(self, image_num):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, f"Select Image {image_num}",
                                                   "", "Images (*.png *.jpg)", options=options)
        if file_path:
            self.images[image_num] = file_path
            self.status_label.setText(f"Selected image {image_num}: {file_path}")

    def start_magic_process(self):
        if not all(self.images.values()):
            QMessageBox.warning(self, "Error", "Please select both images")
            return

        try:
            self.finished_file_path = mixTwoImagesMagic(
                self.images[1],
                self.images[2]
            )
            self.status_label.setText("Images combined successfully!")
            self.download_button.setEnabled(True)

            # Display the combined image
            pixmap = QPixmap(self.finished_file_path)
            if pixmap.isNull():
                print("Error: Unable to load the processed image.")
            else:
                self.image_label.setPixmap(pixmap)
                self.image_label.show()
                self.toggle_background_button.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def toggle_box_background(self):
        if self.current_box_background == "white":
            self.image_box.setStyleSheet("background-color: black;")
            self.current_box_background = "black"
        else:
            self.image_box.setStyleSheet("background-color: white;")
            self.current_box_background = "white"

    def download_file(self):
        if not self.finished_file_path:
            QMessageBox.warning(self, "Error", "No processed file available")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Result", "",
                                                   "Images (*.png *.jpg)")
        if save_path:
            try:
                os.replace(self.finished_file_path, save_path)
                self.status_label.setText(f"Saved to: {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

class ExtractLSBTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Description label
        description_label = QLabel("""
        <h2>Extract Hidden Text</h2>
        <p>Extract hidden messages embedded in the Least Significant Bits of an image.<br>
        Select an image, specify the bit depth, and uncover the hidden text!</p>
        """)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-weight: bold; background: transparent; border: none;")

        # File selection button
        self.file_button = QPushButton("Select Image File")
        self.file_button.setFixedSize(200, 30)
        self.file_button.setToolTip("Click to choose an image file for extracting hidden text")
        self.file_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.file_button.clicked.connect(self.select_file)

        # Bit depth input
        self.bit_depth_field = QLineEdit()
        self.bit_depth_field.setPlaceholderText("Enter bit depth (default is 1)")
        self.bit_depth_field.setToolTip("Specify the number of Least Significant Bits used for embedding the text")
        self.bit_depth_field.setFixedSize(300, 40)  # Larger input box for better visibility
        self.bit_depth_field.setStyleSheet(
            "padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")

        # Process button
        self.start_button = QPushButton("Extract Hidden Text")
        self.start_button.setFixedSize(200, 30)
        self.start_button.setToolTip("Start extracting hidden text from the selected image")
        self.start_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.start_button.clicked.connect(self.start_extraction)

        # Box for results
        self.result_box = QFrame()
        self.result_box.setFrameStyle(QFrame.Box)
        self.result_box.setLineWidth(2)
        self.result_box.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ccc; padding: 10px;")
        self.result_box.setFixedSize(550, 150)

        # Result display inside the box
        result_layout = QVBoxLayout(self.result_box)
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; color: #333;")
        result_layout.addWidget(self.result_label)

        # Status label
        self.status_label = QLabel("Select an image file to extract hidden text.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #333; border: none; background: transparent;")

        # Add widgets to the main layout
        layout.addWidget(description_label)
        layout.addSpacing(10)
        layout.addWidget(self.file_button, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.bit_depth_field, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.result_box, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.status_label)

        # Set the main layout
        self.setLayout(layout)

        # Set overall style
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                background-color: white;
                color: black;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:disabled {
                background-color: #ddd;
                color: #666;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                margin: 5px 0;
            }
            QFrame {
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Internal attributes
        self.file_path = None

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.jpg)", options=options)
        if file_path:
            self.file_path = file_path
            self.status_label.setText(f"Selected file: {file_path}")

    def start_extraction(self):
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Please select an image file.")
            return

        try:
            # Get bit depth from the input field or use the default value
            bit_depth = int(self.bit_depth_field.text()) if self.bit_depth_field.text().isdigit() else 1

            # Call the API to extract text
            extracted_text = getTextFromLSB(self.file_path, bitDepth=bit_depth)
            if extracted_text:
                self.status_label.setText("Text extracted successfully!")
                self.result_label.setText(f"<b>Extracted Text:</b><br>{extracted_text}")
            else:
                self.status_label.setText("No hidden text found.")
                self.result_label.setText("No hidden text found in the image.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class SeparateChannelsTab(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        # Main scrollable area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Description label
        description_label = QLabel("""
        <h2>Separate RGB Channels</h2>
        <p>Select an RGB image to split it into its Red, Green, and Blue channels.<br>
        Preview each channel and download them individually after processing.</p>
        """)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-weight: bold; background: transparent; border: none;")

        # File selection button
        self.file_button = QPushButton("Select RGB Image")
        self.file_button.setFixedSize(200, 30)
        self.file_button.setToolTip("Click to select an RGB image")
        self.file_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.file_button.clicked.connect(self.select_file)

        # Process button
        self.start_button = QPushButton("Separate Channels")
        self.start_button.setFixedSize(200, 30)
        self.start_button.setToolTip("Start separating the image into RGB channels")
        self.start_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.start_button.clicked.connect(self.start_separation)

        # Check channel buttons
        self.check_red_button = QPushButton("Check Red Channel")
        self.check_green_button = QPushButton("Check Green Channel")
        self.check_blue_button = QPushButton("Check Blue Channel")

        for button in [self.check_red_button, self.check_green_button, self.check_blue_button]:
            button.setFixedSize(200, 30)
            button.setStyleSheet("padding: 8px; font-size: 14px;")
            button.setToolTip("Preview the selected channel")
            button.setEnabled(False)

        self.check_red_button.clicked.connect(lambda: self.preview_channel("red"))
        self.check_green_button.clicked.connect(lambda: self.preview_channel("green"))
        self.check_blue_button.clicked.connect(lambda: self.preview_channel("blue"))

        # Image box for preview
        self.image_box = QFrame()
        self.image_box.setFrameStyle(QFrame.Box)
        self.image_box.setLineWidth(2)
        self.image_box.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.image_box.setFixedSize(550, 450)

        # Centering layout for image preview
        image_box_layout = QVBoxLayout(self.image_box)
        image_box_layout.setAlignment(Qt.AlignCenter)

        # Image preview label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(480, 380)
        self.image_label.hide()

        # Add the image label to the box's layout
        image_box_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Dynamic download button
        self.download_channel_button = QPushButton("Download Channel")
        self.download_channel_button.setFixedSize(200, 30)
        self.download_channel_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.download_channel_button.setToolTip("Download the currently displayed channel")
        self.download_channel_button.setEnabled(False)
        self.download_channel_button.clicked.connect(self.download_selected_channel)

        # Status label
        self.status_label = QLabel("Select an RGB image to separate into channels.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #333; border: none; background: transparent;")

        # Add widgets to the scroll layout
        scroll_layout.addWidget(description_label)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.file_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.check_red_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(5)
        scroll_layout.addWidget(self.check_green_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(5)
        scroll_layout.addWidget(self.check_blue_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.image_box, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.download_channel_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.status_label)

        # Set the scroll area's widget to the scroll content
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Set overall style
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                background-color: white;
                color: black;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:disabled {
                background-color: #ddd;
                color: #666;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                margin: 5px 0;
            }
            QFrame {
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Internal attributes
        self.file_path = None
        self.channel_paths = {"red": None, "green": None, "blue": None}
        self.current_channel = None  # Track the currently selected channel

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select RGB Image", "", "Images (*.png *.jpg)", options=options)
        if file_path:
            self.file_path = file_path
            self.status_label.setText(f"Selected file: {file_path}")

    def start_separation(self):
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Please select an RGB image.")
            return

        try:
            # Call the API to separate color channels
            red_path, green_path, blue_path = separateColorChannels(self.file_path)
            self.channel_paths["red"] = red_path
            self.channel_paths["green"] = green_path
            self.channel_paths["blue"] = blue_path

            self.status_label.setText("Channels separated successfully!")
            for button in [self.check_red_button, self.check_green_button, self.check_blue_button]:
                button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def preview_channel(self, channel):
        """Display the selected channel in the image box."""
        if self.channel_paths[channel]:
            self.image_label.setPixmap(QPixmap(self.channel_paths[channel]))
            self.image_label.show()
            self.download_channel_button.setText(f"Download {channel.capitalize()} Channel")
            self.download_channel_button.setEnabled(True)
            self.current_channel = channel
            self.status_label.setText(f"Previewing {channel.capitalize()} Channel.")
        else:
            self.status_label.setText(f"{channel.capitalize()} channel not available.")

    def download_selected_channel(self):
        """Download the currently displayed channel."""
        if self.current_channel and self.channel_paths[self.current_channel]:
            self.download_file(self.current_channel)
        else:
            self.status_label.setText("No channel selected for download.")

    def download_file(self, channel):
        if not self.channel_paths[channel]:
            QMessageBox.warning(self, "Error", f"No {channel} channel file available.")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, f"Save {channel.title()} Channel", "", "Images (*.png *.jpg)")
        if save_path:
            try:
                os.replace(self.channel_paths[channel], save_path)
                self.status_label.setText(f"{channel.title()} channel saved to: {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

class HideTextInLargerImageTab(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        # Main scrollable area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Description label
        description_label = QLabel("""
        <h2>Hide Text in Larger Image</h2>
        <p>Select an image file, enter the text you want to hide, and save the modified image.</p>
        """)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-weight: bold; background: transparent; border: none;")

        # File selection button
        self.file_button = QPushButton("Select Image File")
        self.file_button.setFixedSize(200, 30)
        self.file_button.setToolTip("Click to select an image file")
        self.file_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.file_button.clicked.connect(self.select_file)

        # Text input field
        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText("Enter the text to hide")
        self.text_field.setToolTip("Type the secret text you want to hide in the image")
        self.text_field.setFixedSize(400, 40)  # Larger and wider input field
        self.text_field.setStyleSheet("padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")

        # Process button
        self.start_button = QPushButton("Hide Text in Larger Image")
        self.start_button.setFixedSize(200, 30)
        self.start_button.setToolTip("Start hiding text in the selected image")
        self.start_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.start_button.clicked.connect(self.start_hiding_process)

        # Download button
        self.download_button = QPushButton("Download Modified Image")
        self.download_button.setFixedSize(200, 30)
        self.download_button.setToolTip("Download the image with hidden text")
        self.download_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.download_file)

        # Image box for preview with border
        self.image_box = QFrame()
        self.image_box.setFrameStyle(QFrame.Box)
        self.image_box.setLineWidth(2)
        self.image_box.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 5px;")
        self.image_box.setFixedSize(550, 450)

        # Centering layout for image preview
        image_box_layout = QVBoxLayout(self.image_box)
        image_box_layout.setAlignment(Qt.AlignCenter)

        # Image preview label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(480, 380)
        self.image_label.hide()

        # Add the image label to the box's layout
        image_box_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Status label
        self.status_label = QLabel("Select an image file and enter text to hide.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #333; border: none; background: transparent;")

        # Add widgets to the scroll layout
        scroll_layout.addWidget(description_label)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.file_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.text_field, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.download_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.image_box, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.status_label)

        # Set the scroll area's widget to the scroll content
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Set overall style
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                background-color: white;
                color: black;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:disabled {
                background-color: #ddd;
                color: #666;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                margin: 5px 0;
            }
            QFrame {
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Internal attributes
        self.file_path = None
        self.finished_file_path = None

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.jpg)", options=options)
        if file_path:
            self.file_path = file_path
            self.status_label.setText(f"Selected file: {file_path}")

    def start_hiding_process(self):
        if not self.file_path or not self.text_field.text():
            QMessageBox.warning(self, "Error", "Please provide an image and text to hide.")
            return

        try:
            # Call the API to hide text by making the image larger
            self.finished_file_path = hideTextByMakingImageLarger(self.file_path, self.text_field.text())

            # Display the processed image in the preview box
            pixmap = QPixmap(self.finished_file_path)
            if pixmap.isNull():
                self.status_label.setText("Error: Unable to load the processed image.")
            else:
                self.image_label.setPixmap(pixmap)
                self.image_label.show()
                self.status_label.setText("Text hidden successfully in the enlarged image! Preview displayed.")
                self.download_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def download_file(self):
        if not self.finished_file_path:
            QMessageBox.warning(self, "Error", "No processed file available.")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Modified Image", "", "Images (*.png *.jpg)")
        if save_path:
            try:
                os.replace(self.finished_file_path, save_path)
                self.status_label.setText(f"Modified image saved to: {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

class ExtractTextFromLargeImageTab(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        # Scrollable area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Description label
        description_label = QLabel("""
        <h2>Extract Hidden Text</h2>
        <p>Select an enlarged image to extract hidden text embedded in it.</p>
        """)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-weight: bold; background: transparent; border: none;")

        # File selection button
        self.file_button = QPushButton("Select Enlarged Image")
        self.file_button.setFixedSize(200, 30)
        self.file_button.setToolTip("Click to select an enlarged image")
        self.file_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.file_button.clicked.connect(self.select_file)

        # Image box for preview
        self.image_box = QFrame()
        self.image_box.setFrameStyle(QFrame.Box)
        self.image_box.setLineWidth(2)
        self.image_box.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.image_box.setFixedSize(500, 400)  # Box size

        # Centering layout for image preview
        image_box_layout = QVBoxLayout(self.image_box)
        image_box_layout.setAlignment(Qt.AlignCenter)

        # Image preview label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(460, 360)  # Slightly smaller than the box
        self.image_label.hide()

        # Add the image label to the box's layout
        image_box_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Process button
        self.start_button = QPushButton("Extract Hidden Text")
        self.start_button.setFixedSize(200, 30)
        self.start_button.setToolTip("Start extracting hidden text from the selected image")
        self.start_button.setStyleSheet("padding: 8px; font-size: 14px;")
        self.start_button.clicked.connect(self.start_extraction)

        # Status label
        self.status_label = QLabel("Select an enlarged image to extract hidden text.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #333; border: none; background: transparent;")

        # Result display
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("border: 1px solid #ccc; padding: 12px; border-radius: 5px; background-color: #f9f9f9;")
        self.result_label.setFixedSize(480, 150)  # Adjusted size for a larger box

        # Add widgets to the scroll layout
        scroll_layout.addWidget(description_label)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.file_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.image_box, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(self.status_label)

        # Set scroll content layout
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Set overall style
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                background-color: white;
                color: black;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:disabled {
                background-color: #ddd;
                color: #666;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                margin: 5px 0;
            }
            QFrame {
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Internal attributes
        self.file_path = None

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Enlarged Image", "", "Images (*.png *.jpg)", options=options)
        if file_path:
            self.file_path = file_path
            self.status_label.setText(f"Selected file: {file_path}")

            # Display the selected image in the box
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.show()

    def start_extraction(self):
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Please select an enlarged image.")
            return

        try:
            # Call the API to extract hidden text
            extracted_text = getTextFromLargeImage(self.file_path)
            if extracted_text:
                self.status_label.setText("Text extracted successfully!")
                self.result_label.setText(f"Extracted Text:\n{extracted_text}")
            else:
                self.result_label.setText("No hidden text found.")
                self.status_label.setText("No hidden text found in the image.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Steganography Tool")

        # Set the window size to match the one in the image
        self.resize(900, 700)  # Adjust width and height as needed
        self.setMinimumSize(900, 700)  # Optionally set a minimum size to prevent resizing smaller than this

        # Create tab widget
        tabs = QTabWidget()
        tabs.addTab(LSBTab(), "LSB Steganography")
        tabs.addTab(RGBTab(), "RGB Channels")
        tabs.addTab(MagicTab(), "Magic Combination")
        tabs.addTab(ExtractLSBTab(), "LSB text extraction")
        tabs.addTab(SeparateChannelsTab(), "Separate Channels")
        tabs.addTab(HideTextInLargerImageTab(), "Hide Text in Larger Image")
        tabs.addTab(ExtractTextFromLargeImageTab(), "Extract Text from Large Image")

        self.setCentralWidget(tabs)

        # Optionally make the app start maximized
        # self.showMaximized()  # Uncomment if needed

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()