import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QTabWidget, QPushButton, QLabel, QFileDialog,
                            QMessageBox, QLineEdit)
from backend.api import (
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

        # Message input
        self.message_field = QLineEdit()
        self.message_field.setPlaceholderText("Enter message to hide")

        # File selection button
        self.file_button = QPushButton("Select Image File")
        self.file_button.setFixedSize(200, 30)
        self.file_button.clicked.connect(self.select_file)

        # Process button
        self.start_button = QPushButton("Hide Message")
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_hiding_process)

        # Download button
        self.download_button = QPushButton("Download Result")
        self.download_button.setFixedSize(200, 30)
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        # Status label
        self.status_label = QLabel("Select a file and enter message")

        # Add widgets to layout
        layout.addWidget(self.message_field)
        layout.addWidget(self.file_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

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
            QMessageBox.warning(self, "Error", "Please provide image and message")
            return

        try:
            self.finished_file_path = hideTextInLSB(self.file_path, 
                                                   self.message_field.text())
            self.status_label.setText("Process completed")
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

class RGBTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # File selection buttons
        self.red_button = QPushButton("Select Red Channel")
        self.green_button = QPushButton("Select Green Channel")
        self.blue_button = QPushButton("Select Blue Channel")

        for btn in [self.red_button, self.green_button, self.blue_button]:
            btn.setFixedSize(200, 30)

        self.red_button.clicked.connect(lambda: self.select_file('red'))
        self.green_button.clicked.connect(lambda: self.select_file('green'))
        self.blue_button.clicked.connect(lambda: self.select_file('blue'))

        # Process button
        self.start_button = QPushButton("Combine Channels")
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_rgb_process)

        # Download button
        self.download_button = QPushButton("Download Result")
        self.download_button.setFixedSize(200, 30)
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        # Status label
        self.status_label = QLabel("Select RGB channel images")

        # Add widgets to layout
        for widget in [self.red_button, self.green_button, self.blue_button,
                      self.start_button, self.download_button, self.status_label]:
            layout.addWidget(widget)
        self.setLayout(layout)

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

        # File selection buttons
        self.image1_button = QPushButton("Select First Image")
        self.image2_button = QPushButton("Select Second Image")

        for btn in [self.image1_button, self.image2_button]:
            btn.setFixedSize(200, 30)

        self.image1_button.clicked.connect(lambda: self.select_file(1))
        self.image2_button.clicked.connect(lambda: self.select_file(2))

        # Process button
        self.start_button = QPushButton("Combine Images")
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_magic_process)

        # Download button
        self.download_button = QPushButton("Download Result")
        self.download_button.setFixedSize(200, 30)
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        # Status label
        self.status_label = QLabel("Select two images to combine")

        # Add widgets to layout
        for widget in [self.image1_button, self.image2_button,
                      self.start_button, self.download_button, self.status_label]:
            layout.addWidget(widget)
        self.setLayout(layout)

        # Internal attributes
        self.images = {1: None, 2: None}
        self.finished_file_path = None

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
            self.status_label.setText("Images combined successfully")
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

class ExtractLSBTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # File selection button
        self.file_button = QPushButton("Select Image File")
        self.file_button.setFixedSize(200, 30)
        self.file_button.clicked.connect(self.select_file)

        # Bit depth input
        self.bit_depth_field = QLineEdit()
        self.bit_depth_field.setPlaceholderText("Enter bit depth (default is 1)")

        # Process button
        self.start_button = QPushButton("Extract Hidden Text")
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_extraction)

        # Status label
        self.status_label = QLabel("Select an image file to extract hidden text.")

        # Result display
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)

        # Add widgets to layout
        layout.addWidget(self.file_button)
        layout.addWidget(self.bit_depth_field)
        layout.addWidget(self.start_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

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
                self.result_label.setText(f"Extracted Text: {extracted_text}")
            else:
                self.status_label.setText("No hidden text found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class SeparateChannelsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # File selection button
        self.file_button = QPushButton("Select RGB Image")
        self.file_button.setFixedSize(200, 30)
        self.file_button.clicked.connect(self.select_file)

        # Process button
        self.start_button = QPushButton("Separate Channels")
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_separation)

        # Download buttons for channels
        self.download_red_button = QPushButton("Download Red Channel")
        self.download_green_button = QPushButton("Download Green Channel")
        self.download_blue_button = QPushButton("Download Blue Channel")
        for button in [self.download_red_button, self.download_green_button, self.download_blue_button]:
            button.setFixedSize(200, 30)
            button.setEnabled(False)

        self.download_red_button.clicked.connect(lambda: self.download_file("red"))
        self.download_green_button.clicked.connect(lambda: self.download_file("green"))
        self.download_blue_button.clicked.connect(lambda: self.download_file("blue"))

        # Status label
        self.status_label = QLabel("Select an RGB image to separate into channels.")

        # Add widgets to layout
        layout.addWidget(self.file_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.download_red_button)
        layout.addWidget(self.download_green_button)
        layout.addWidget(self.download_blue_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        # Internal attributes
        self.file_path = None
        self.channel_paths = {"red": None, "green": None, "blue": None}

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
            for button in [self.download_red_button, self.download_green_button, self.download_blue_button]:
                button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

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
        layout = QVBoxLayout()

        # File selection button
        self.file_button = QPushButton("Select Image File")
        self.file_button.setFixedSize(200, 30)
        self.file_button.clicked.connect(self.select_file)

        # Text input field
        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText("Enter the text to hide")

        # Process button
        self.start_button = QPushButton("Hide Text in Larger Image")
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_hiding_process)

        # Download button
        self.download_button = QPushButton("Download Modified Image")
        self.download_button.setFixedSize(200, 30)
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.download_file)

        # Status label
        self.status_label = QLabel("Select an image file and enter text to hide.")

        # Add widgets to layout
        layout.addWidget(self.file_button)
        layout.addWidget(self.text_field)
        layout.addWidget(self.start_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

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
            self.status_label.setText("Text hidden successfully in the enlarged image!")
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
        layout = QVBoxLayout()

        # File selection button
        self.file_button = QPushButton("Select Enlarged Image")
        self.file_button.setFixedSize(200, 30)
        self.file_button.clicked.connect(self.select_file)

        # Process button
        self.start_button = QPushButton("Extract Hidden Text")
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_extraction)

        # Status label
        self.status_label = QLabel("Select an enlarged image to extract hidden text.")

        # Result display
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)

        # Add widgets to layout
        layout.addWidget(self.file_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        # Internal attributes
        self.file_path = None

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Enlarged Image", "", "Images (*.png *.jpg)", options=options)
        if file_path:
            self.file_path = file_path
            self.status_label.setText(f"Selected file: {file_path}")

    def start_extraction(self):
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Please select an enlarged image.")
            return

        try:
            # Call the API to extract hidden text
            extracted_text = getTextFromLargeImage(self.file_path)
            if extracted_text:
                self.status_label.setText("Text extracted successfully!")
                self.result_label.setText(f"Extracted Text: {extracted_text}")
            else:
                self.status_label.setText("No hidden text found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Steganography Tool")
        self.setGeometry(100, 100, 800, 600)

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


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()