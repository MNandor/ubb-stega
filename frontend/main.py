import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit, QComboBox
)
from PyQt5.QtCore import Qt


class Tab1(QWidget):
    """First Tab: Hide Text in a File"""
    def __init__(self):
        super().__init__()

        # Layout for the tab
        layout = QVBoxLayout()

        # Input field for the message
        self.message_field = QLineEdit(self)
        self.message_field.setPlaceholderText("Enter the text message to hide...")

        # File selection button
        self.file_button = QPushButton("Select File to Hide Text In", self)
        self.file_button.setFixedSize(200, 30)
        self.file_button.clicked.connect(self.select_file)

        # Start hiding process button
        self.start_button = QPushButton("Start Hiding Process", self)
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_hiding_process)

        # Download file button
        self.download_button = QPushButton("Download Finished File", self)
        self.download_button.setFixedSize(200, 30)
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        # Status label
        self.status_label = QLabel("Status will be displayed here.", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(self.message_field)
        layout.addWidget(self.file_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.status_label)

        # Set layout
        self.setLayout(layout)

        # Internal attributes
        self.file_path = None
        self.finished_file_path = None

    def select_file(self):
        """Select the input file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if file_path:
            self.file_path = file_path
            self.status_label.setText(f"Selected file: {file_path}")

    def start_hiding_process(self):
        """Start hiding the text in the selected file."""
        if not self.file_path or not self.message_field.text():
            QMessageBox.warning(self, "Missing Information", "Please provide both a file and a message.")
            return

        # Simulating a successful process (backend logic will replace this)
        self.finished_file_path = os.path.join(os.path.dirname(self.file_path), "finished_file.txt")
        self.status_label.setText(f"Process completed successfully. Finished file: {self.finished_file_path}")
        self.download_button.setEnabled(True)

    def download_file(self):
        """Save/download the finished file."""
        if not self.finished_file_path:
            QMessageBox.warning(self, "No Finished File", "There is no finished file to download.")
            return

        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Finished File", "", "All Files (*)", options=options)
        if save_path:
            # Simulating saving the file (backend logic will provide actual file content)
            with open(self.finished_file_path, "w") as f:
                f.write("This is a simulated finished file.")
            self.status_label.setText(f"File saved to: {save_path}")


class Tab2(QWidget):
    """Second Tab: Hide a File in Another File"""
    def __init__(self):
        super().__init__()

        # Layout for the tab
        layout = QVBoxLayout()

        # File selection button for the file to be hidden
        self.file_to_hide_button = QPushButton("Select File to Hide", self)
        self.file_to_hide_button.setFixedSize(200, 30)
        self.file_to_hide_button.clicked.connect(self.select_file_to_hide)

        # File selection button for the container file
        self.container_file_button = QPushButton("Select Container File", self)
        self.container_file_button.setFixedSize(200, 30)
        self.container_file_button.clicked.connect(self.select_container_file)

        # Start hiding process button
        self.start_button = QPushButton("Start Hiding Process", self)
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_hiding_process)

        # Download file button
        self.download_button = QPushButton("Download Finished File", self)
        self.download_button.setFixedSize(200, 30)
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        # Status label
        self.status_label = QLabel("Status will be displayed here.", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(self.file_to_hide_button)
        layout.addWidget(self.container_file_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.status_label)

        # Set layout
        self.setLayout(layout)

        # Internal attributes
        self.file_to_hide_path = None
        self.container_file_path = None
        self.finished_file_path = None

    def select_file_to_hide(self):
        """Select the file to be hidden."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Hide", "", "All Files (*)", options=options)
        if file_path:
            self.file_to_hide_path = file_path
            self.status_label.setText(f"Selected file to hide: {file_path}")

    def select_container_file(self):
        """Select the container file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Container File", "", "All Files (*)", options=options)
        if file_path:
            self.container_file_path = file_path
            self.status_label.setText(f"Selected container file: {file_path}")

    def start_hiding_process(self):
        """Start hiding the file in the container file."""
        if not self.file_to_hide_path or not self.container_file_path:
            QMessageBox.warning(self, "Missing Information", "Please select both files.")
            return

        # Simulating a successful process (backend logic will replace this)
        self.finished_file_path = os.path.join(os.path.dirname(self.container_file_path), "hidden_file_output.txt")
        self.status_label.setText(f"Process completed successfully. Finished file: {self.finished_file_path}")
        self.download_button.setEnabled(True)

    def download_file(self):
        """Save/download the finished file."""
        if not self.finished_file_path:
            QMessageBox.warning(self, "No Finished File", "There is no finished file to download.")
            return

        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Finished File", "", "All Files (*)", options=options)
        if save_path:
            # Simulating saving the file (backend logic will provide actual file content)
            with open(self.finished_file_path, "w") as f:
                f.write("This is a simulated finished file with hidden content.")
            self.status_label.setText(f"File saved to: {save_path}")


class MagicTab(QWidget):
    """Third Tab: Magic - Combine Two Images"""
    def __init__(self):
        super().__init__()

        # Layout for the tab
        layout = QVBoxLayout()

        # File selection for image 1
        self.image1_button = QPushButton("Upload First Image", self)
        self.image1_button.setFixedSize(200, 30)
        self.image1_button.clicked.connect(self.upload_image1)

        # File selection for image 2
        self.image2_button = QPushButton("Upload Second Image", self)
        self.image2_button.setFixedSize(200, 30)
        self.image2_button.clicked.connect(self.upload_image2)

        # Start process button
        self.start_button = QPushButton("Start Magic Process", self)
        self.start_button.setFixedSize(200, 30)
        self.start_button.clicked.connect(self.start_magic_process)

        # Download button
        self.download_button = QPushButton("Download Final Product", self)
        self.download_button.setFixedSize(200, 30)
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        # Status label
        self.status_label = QLabel("Status will be displayed here.", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(self.image1_button)
        layout.addWidget(self.image2_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.status_label)

        # Set layout
        self.setLayout(layout)

        # Internal attributes
        self.image1_path = None
        self.image2_path = None
        self.result_path = None

    def upload_image1(self):
        """Upload the first image."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload First Image", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            self.image1_path = file_path
            self.status_label.setText(f"First image selected: {file_path}")

    def upload_image2(self):
        """Upload the second image."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Second Image", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            self.image2_path = file_path
            self.status_label.setText(f"Second image selected: {file_path}")

    def start_magic_process(self):
        """Start the magic process."""
        if not self.image1_path or not self.image2_path:
            QMessageBox.warning(self, "Missing Information", "Please upload both images.")
            return

        # Simulate the process (backend logic will replace this)
        self.result_path = os.path.join(os.path.dirname(self.image1_path), "magic_result.png")
        self.status_label.setText(f"Magic process completed. Result file: {self.result_path}")
        self.download_button.setEnabled(True)

    def download_file(self):
        """Save/download the final product."""
        if not self.result_path:
            QMessageBox.warning(self, "No Final Product", "There is no final product to download.")
            return

        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Final Product", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if save_path:
            # Simulate saving the file (backend logic will provide actual file content)
            with open(self.result_path, "w") as f:
                f.write("This is a simulated magic result.")
            self.status_label.setText(f"File saved to: {save_path}")

class CheckSteganographyTab(QWidget):
    """Fourth Tab: Check if Steganography is Applied"""
    def __init__(self):
        super().__init__()

        # Layout for the tab
        layout = QVBoxLayout()

        # File selection button
        self.file_button = QPushButton("Upload File", self)
        self.file_button.setFixedSize(200, 30)
        self.file_button.clicked.connect(self.upload_file)

        # Dropdown to select expected content
        self.dropdown = QComboBox(self)
        self.dropdown.addItems(["Select Expected Content", "Text", "File"])
        self.dropdown.setFixedSize(200, 30)

        # Check steganography button
        self.check_button = QPushButton("Check for Steganography", self)
        self.check_button.setFixedSize(200, 30)
        self.check_button.clicked.connect(self.check_steganography)

        # Status label
        self.status_label = QLabel("Status will be displayed here.", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Download button (enabled only if a file is found)
        self.download_button = QPushButton("Download Hidden File", self)
        self.download_button.setFixedSize(200, 30)
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.download_file)

        # Add widgets to layout
        layout.addWidget(self.file_button)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.check_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.status_label)

        # Set layout
        self.setLayout(layout)

        # Internal attributes
        self.file_path = None
        self.hidden_file_path = None
        self.extracted_text = None

    def upload_file(self):
        """Upload the file to be checked."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload File", "", "All Files (*)", options=options)
        if file_path:
            self.file_path = file_path
            self.status_label.setText(f"Selected file: {file_path}")

    def check_steganography(self):
        """Check for steganography in the uploaded file."""
        if not self.file_path:
            QMessageBox.warning(self, "Missing File", "Please upload a file to check.")
            return

        if self.dropdown.currentText() == "Select Expected Content":
            QMessageBox.warning(self, "Missing Selection", "Please select what you expect to find (Text or File).")
            return

        # Simulated backend logic
        expected_content = self.dropdown.currentText()

        # Simulate result for "Text"
        if expected_content == "Text":
            # Simulate detecting hidden text
            self.extracted_text = "This is hidden steganographic text."
            self.hidden_file_path = None
            self.status_label.setText("Hidden text found! Displaying content below:")
            QMessageBox.information(self, "Hidden Content Found", f"Text Content: {self.extracted_text}")

        # Simulate result for "File"
        elif expected_content == "File":
            # Simulate detecting a hidden file
            self.extracted_text = None
            self.hidden_file_path = os.path.join(os.path.dirname(self.file_path), "hidden_file.txt")
            self.status_label.setText("Hidden file found! You can now download it.")
            self.download_button.setEnabled(True)

        # If nothing is found
        else:
            self.extracted_text = None
            self.hidden_file_path = None
            self.status_label.setText("No hidden content found.")
            QMessageBox.information(self, "No Content Found", "The file does not contain any hidden content.")

    def download_file(self):
        """Save/download the hidden file."""
        if not self.hidden_file_path:
            QMessageBox.warning(self, "No File to Download", "No hidden file was found.")
            return

        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Hidden File", "", "All Files (*)", options=options)
        if save_path:
            # Simulate saving the file (backend logic will provide actual file content)
            with open(self.hidden_file_path, "w") as f:
                f.write("This is the hidden file content.")  # Simulated content
            self.status_label.setText(f"File saved to: {save_path}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Steganography Application")
        self.setGeometry(100, 100, 600, 400)

        # Create Tab Widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add Tabs
        self.tabs.addTab(Tab1(), "Hide Text")
        self.tabs.addTab(Tab2(), "Hide File")
        self.tabs.addTab(MagicTab(), "Magic")
        self.tabs.addTab(CheckSteganographyTab(), "Check Steganography")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
