# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

# Import the generated UI class from your .py file
# Make sure 'design_ui' matches the filename where you saved the generated code.
from design_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create an instance of the UI_MainWindow class
        self.ui = Ui_MainWindow()
        # Call the setupUi method to populate the MainWindow with your designed widgets
        self.ui.setupUi(self)

        # You can add connections to your widgets here if needed
        # For example, if your pushButton was named "mySpecificButton" in Designer
        # and you wanted to connect its click to a method:
        # self.ui.mySpecificButton.clicked.connect(self.on_button_clicked)

        # For the pushButton you have (named "pushButton" by default in your UI code):
        self.ui.pushButton.clicked.connect(self.print_message)

    def print_message(self):
        print("Button clicked!")
        # You can also interact with other UI elements here, e.g.,
        # self.ui.statusbar.showMessage("Button was clicked!", 3000) # Show for 3 seconds


if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create the QApplication
    window = MainWindow()         # Create an instance of your MainWindow
    window.show()                 # Show the window
    sys.exit(app.exec())          # Start the event loop
