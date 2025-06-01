"""
Main application for analyzing French energy consumption.
Uses PyQt6 for the GUI and interacts with DataHandler for data operations.
"""
import sys
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                             QFileDialog, QVBoxLayout, QWidget)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QKeySequence

# Import the generated UI class
from ui_mainwindow import Ui_MainWindow 
from data_handler import DataHandler

# Import pyqtgraph. Ensure it's installed.
try:
    import pyqtgraph as pg
    from pyqtgraph import PlotWidget
    PYQTGRAPH_AVAILABLE = True
except ImportError:
    PYQTGRAPH_AVAILABLE = False
    print("Error: pyqtgraph library is not installed. Plotting will be disabled.")
    print("Please install it: pip install pyqtgraph")
    # Fallback PlotWidget if pyqtgraph is not available, so ui_mainwindow can load
    class PlotWidget(QWidget): # pylint: disable=function-redefined
        """Placeholder for PlotWidget if pyqtgraph is not available."""
        def __init__(self, parent=None):
            super().__init__(parent)
            print("pyqtgraph.PlotWidget could not be imported. Using placeholder.")
        def plot(self, *args, **kwargs): # pylint: disable=unused-argument
            """Placeholder plot method."""
            print("Plotting unavailable: pyqtgraph not found.")
        def clear(self):
            """Placeholder clear method."""
            pass
        def addLegend(self, *args, **kwargs): # pylint: disable=unused-argument
            """Placeholder addLegend method."""
            pass
        def setLabel(self, *args, **kwargs): # pylint: disable=unused-argument
            """Placeholder setLabel method."""
            pass


class MainWindow(QMainWindow):
    """
    Main application window class.
    Manages the UI, data handling, and plotting.
    """
    def __init__(self):
        """
        Constructor for the main window.
        """
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Analyse Consommation Énergie France")

        self.data_handler = DataHandler()
        self.current_plot_item = None

        if not PYQTGRAPH_AVAILABLE:
            QMessageBox.critical(self, "Dependency Error",
                                 "pyqtgraph is not installed. Plotting will be disabled.\n"
                                 "Please install it via pip: pip install pyqtgraph")
            # Disable plot-related UI elements if pyqtgraph is not available
            self.ui.comboPlotSelection.setEnabled(False)

        self._setup_ui_connections()
        self._populate_plot_options()
        
        self.ui.statusbar.showMessage("Application started. Ready to fetch data.", 5000)
        print("MainWindow initialized.")

    def _setup_ui_connections(self):
        """
        Connects UI element signals to their respective slots (methods).
        """
        # Menu actions
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionFetchData.triggered.connect(self.fetch_and_update_all)
        self.ui.actionExportCSV.triggered.connect(self.export_data_to_csv)
        
        # Button
        self.ui.btnFetchData.clicked.connect(self.fetch_and_update_all)

        # ComboBox for plot selection
        self.ui.comboPlotSelection.currentTextChanged.connect(self.update_plot_view)
        
        print("UI connections established.")

    def _populate_plot_options(self):
        """
        Populates the plot selection combobox based on available data columns.
        """
        self.ui.comboPlotSelection.clear()
        options = self.data_handler.get_plot_options()
        self.ui.comboPlotSelection.addItems(options)
        if not options or options == ["No data"]:
            self.ui.comboPlotSelection.setEnabled(False)
        else:
            self.ui.comboPlotSelection.setEnabled(PYQTGRAPH_AVAILABLE)
        print(f"Plot options populated: {options}")

    def fetch_and_update_all(self):
        """
        Fetches data using DataHandler and updates the UI (summary and plot).
        """
        self.ui.statusbar.showMessage("Fetching data from API...")
        print("Attempting to fetch and update all...")
        QApplication.processEvents() # Keep UI responsive

        success = self.data_handler.fetch_data_from_api(limit=200) # Fetch more for a better plot

        if success and not self.data_handler.dataframe.empty:
            self.ui.statusbar.showMessage("Data fetched successfully. Processing and plotting...", 5000)
            summary = self.data_handler.get_summary()
            self.ui.textDataSummary.setText(summary)
            self._populate_plot_options() # Re-populate in case columns changed
            self.update_plot_view() # Update plot with current selection
            print("Data fetch and UI update successful.")
        elif success and self.data_handler.dataframe.empty:
            self.ui.statusbar.showMessage("API request successful, but no data returned.", 5000)
            self.ui.textDataSummary.setText("No data returned from the API.")
            self.ui.plotWidget.clear()
            self._populate_plot_options()
            print("API success, but no data.")
        else:
            self.ui.statusbar.showMessage("Failed to fetch data. Check console for errors.", 5000)
            self.ui.textDataSummary.setText("Failed to fetch data. See console for details.")
            self.ui.plotWidget.clear()
            self._populate_plot_options()
            QMessageBox.warning(self, "Data Fetch Error",
                                "Could not fetch data from the API. Please check your internet connection and the API status.")
            print("Data fetch failed.")

    def update_plot_view(self):
        """
        Updates the plot based on the current selection in the combobox.
        """
        if not PYQTGRAPH_AVAILABLE or self.data_handler.dataframe.empty:
            self.ui.plotWidget.clear()
            return

        selected_column = self.ui.comboPlotSelection.currentText()
        print(f"Updating plot for: {selected_column}")

        if not selected_column or selected_column == "No data" or selected_column not in self.data_handler.dataframe.columns:
            self.ui.plotWidget.clear()
            print(f"Selected column '{selected_column}' not available for plotting or no data.")
            return

        df = self.data_handler.dataframe
        
        if 'date_heure' not in df.columns or df['date_heure'].isnull().all():
            print("Date/time column 'date_heure' is missing or all null, cannot plot time series.")
            QMessageBox.warning(self, "Plot Error", "Date/time information is missing in the data.")
            self.ui.plotWidget.clear()
            return

        # Ensure 'date_heure' is suitable as x-axis (e.g., convert to timestamps for pyqtgraph)
        # pyqtgraph typically handles datetime objects if axis is set up correctly,
        # but timestamps can be more robust.
        x_axis_data = df['date_heure'].astype('int64') // 10**9 # Convert to Unix timestamp (seconds)
        
        y_axis_data = df[selected_column]

        self.ui.plotWidget.clear() # Clear previous plot
        
        # Set up axis labels
        self.ui.plotWidget.setLabel('left', selected_column, units='MWh or similar') # Adjust units as needed
        self.ui.plotWidget.setLabel('bottom', 'Date / Heure')

        # Add a DateAxisItem for the bottom axis
        axis = pg.DateAxisItem(orientation='bottom')
        self.ui.plotWidget.setAxisItems({'bottom': axis})

        # Plot data
        pen_color = pg.mkPen(color=(50, 100, 200), width=2) # Blueish pen
        try:
            self.current_plot_item = self.ui.plotWidget.plot(x=x_axis_data.values, y=y_axis_data.values, pen=pen_color, name=selected_column)
            self.ui.plotWidget.addLegend()
            self.ui.statusbar.showMessage(f"Displaying plot for {selected_column}", 3000)
            print(f"Plot updated for {selected_column}.")
        except Exception as e:
            print(f"Error during plotting with pyqtgraph: {e}")
            QMessageBox.critical(self, "Plotting Error", f"An error occurred while trying to plot the data: {e}")


    def export_data_to_csv(self):
        """
        Handles exporting the current data to a CSV file.
        """
        if self.data_handler.dataframe.empty:
            QMessageBox.information(self, "Export CSV", "No data available to export.")
            print("Export CSV: No data.")
            return

        options = QFileDialog.Options()
        options |= QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Data as CSV", 
            "", # Default directory
            "CSV Files (*.csv);;All Files (*)", 
            options=options
        )

        if file_path:
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
            
            print(f"Attempting to export data to: {file_path}")
            if self.data_handler.export_to_csv(file_path):
                QMessageBox.information(self, "Export Successful", f"Data exported to:\n{file_path}")
                self.ui.statusbar.showMessage(f"Data exported to {file_path}", 5000)
            else:
                QMessageBox.warning(self, "Export Failed", "Could not save the data to CSV. Check console for details.")
                self.ui.statusbar.showMessage("CSV export failed.", 5000)
        else:
            print("CSV export cancelled by user.")
            self.ui.statusbar.showMessage("CSV export cancelled.", 3000)


    def closeEvent(self, event):
        """
        Handles the close event of the window.
        """
        reply = QMessageBox.question(self, 'Quitter',
                                     "Êtes-vous sûr de vouloir quitter l'application ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            print("Exiting application...")
            event.accept()
        else:
            event.ignore()

def main():
    """
    Main function to run the application.
    """
    print("Starting application...")
    app = QApplication(sys.argv)
    
    # Apply a simple stylesheet for better look (optional)
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0;
        }
        QPushButton {
            background-color: #c0d0e0;
            border: 1px solid #a0b0c0;
            padding: 5px;
            min-width: 80px;
        }
        QPushButton:hover {
            background-color: #d0e0f0;
        }
        QPushButton:pressed {
            background-color: #b0c0d0;
        }
        QComboBox {
            padding: 3px;
        }
        QTextEdit {
            background-color: white;
            border: 1px solid #c0c0c0;
        }
        QGroupBox {
            font-weight: bold;
        }
        QMenuBar {
            background-color: #e0e0e0;
        }
        QStatusBar {
            font-style: italic;
        }
    """)

    # Check for pyqtgraph availability before creating MainWindow
    if not PYQTGRAPH_AVAILABLE:
        # Show a critical message and exit if pyqtgraph is not available.
        # MainWindow's __init__ already shows a message, but this can be an earlier exit.
        # However, the current setup tries to run even without it, disabling plotting.
        pass

    window = MainWindow()
    window.show()
    print("Application window displayed.")
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
    