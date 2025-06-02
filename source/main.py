# main.py
import sys
import pandas as pd # For type hinting and potential direct use if needed
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import Qt # QTimer can be added later if needed

# Import your generated UI class and DataHandler class
from design_ui import Ui_MainWindow  # Assuming your new UI file is design_ui.py
from data_handler import DataHandler

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.setWindowTitle("Analyse de Consommation d'Énergie") # Set a window title

    self.data_handler = DataHandler()

    # --- Connect UI element signals to methods ---
    self.ui.fetch_data.clicked.connect(self.handle_fetch_data_and_update_stats)
    self.ui.save_csv.clicked.connect(self.handle_save_csv)

    # --- Initial UI State ---
    self.clear_stats_labels()
    self.ui.statusbar.showMessage("Prêt. Cliquez sur 'Récupérer Les Données' pour commencer.", 5000)
    print("MainWindow initialisée. Interface utilisateur configurée.")
    
    # The QGraphicsView named 'graphicsView' is available as self.ui.graphicsView
    # Plotting logic can be added here or in a dedicated method later.
    # For now, it will be an empty view.

  def clear_stats_labels(self):
    """Resets all statistics display labels to '0.0' or 'N/A'."""
    self.ui.stats_main.setText("0.0")
    self.ui.stats_std.setText("0.0")
    self.ui.stats_variance.setText("0.0")
    self.ui.stats_max.setText("0.0")
    self.ui.stats_min.setText("0.0")
    print("Étiquettes de statistiques réinitialisées.")

  def handle_fetch_data_and_update_stats(self):
    """
    Handles the 'fetch_data' button click.
    Fetches data, calculates statistics, and updates the UI labels.
    """
    print("Bouton 'Récupérer Les Données' cliqué.")
    self.ui.statusbar.showMessage("Récupération des données en cours...", 3000)
    QApplication.processEvents()  # Keep UI responsive

    # Fetch data (e.g., 200 records for a decent sample for stats)
    success = self.data_handler.fetch_data_from_api(limit=200)

    if success and not self.data_handler.dataframe.empty:
      self.ui.statusbar.showMessage("Données récupérées. Calcul des statistiques...", 3000)
      df = self.data_handler.dataframe
      
      # --- Choose the column for statistical analysis ---
      # Let's use 'consommation_brute_totale' for this example.
      # Ensure this column exists after processing in DataHandler.
      stats_column_name = 'consommation_brute_totale'

      if stats_column_name not in df.columns:
        error_msg = f"La colonne '{stats_column_name}' est introuvable pour le calcul des statistiques."
        print(error_msg)
        QMessageBox.warning(self, "Erreur de Données", error_msg)
        self.ui.statusbar.showMessage(error_msg, 5000)
        self.clear_stats_labels()
        return

      # --- Calculate Statistics ---
      # The DataHandler already converts consumption columns to numeric and fills NaNs with 0.
      # This fillna(0) will affect statistics like min, std, variance if there were many NaNs.
      selected_series = df[stats_column_name]
      
      mean_val = selected_series.mean()
      std_val = selected_series.std()
      var_val = selected_series.var()
      max_val = selected_series.max()
      min_val = selected_series.min() # Will be 0 if there were NaNs filled with 0 and no other zeros

      print(f"Statistiques pour '{stats_column_name}':")
      print(f"  Moyenne: {mean_val:.2f}, Ecart-type: {std_val:.2f}, Variance: {var_val:.2f}")
      print(f"  Min: {min_val:.2f}, Max: {max_val:.2f}")

      # --- Update UI Labels with calculated statistics ---
      # The descriptive labels (e.g., stats_main_label) are not changed.
      self.ui.stats_main.setText(f"{mean_val:,.2f}") # Added comma for thousands
      self.ui.stats_std.setText(f"{std_val:,.2f}")
      self.ui.stats_variance.setText(f"{var_val:,.2f}")
      self.ui.stats_max.setText(f"{max_val:,.2f}")
      self.ui.stats_min.setText(f"{min_val:,.2f}")
      
      self.ui.statusbar.showMessage("Statistiques mises à jour.", 5000)

      # You could also update the QTextBrowser with a general summary if desired
      # summary_text = self.data_handler.get_summary()
      # self.ui.textBrowser.setText(summary_text) # Be careful, textBrowser has pre-filled HTML
      
      # Placeholder for updating the plot
      # self.update_plot(df) 

    elif success and self.data_handler.dataframe.empty:
      message = "Récupération API réussie, mais aucun enregistrement de données n'a été retourné."
      print(message)
      QMessageBox.information(self, "Données Vides", message)
      self.ui.statusbar.showMessage(message, 5000)
      self.clear_stats_labels()
    else:
      message = "Échec de la récupération des données depuis l'API. Vérifiez la console."
      print(message)
      QMessageBox.warning(self, "Erreur Réseau", message)
      self.ui.statusbar.showMessage(message, 5000)
      self.clear_stats_labels()

  def handle_save_csv(self):
    """
    Handles the 'save_csv' button click.
    Opens a dialog to save the current dataframe to a CSV file.
    """
    print("Bouton 'Sauvegarder en CSV' cliqué.")
    if self.data_handler.dataframe.empty:
      QMessageBox.information(self, "Aucune Donnée", "Aucune donnée à sauvegarder. Veuillez d'abord récupérer les données.")
      print("Aucune donnée à exporter.")
      return

    # Propose a default filename with a timestamp or based on data range
    default_filename = "consommation_quotidienne_export.csv"
    
    filePath, _ = QFileDialog.getSaveFileName(
      self,
      "Sauvegarder le fichier CSV",
      default_filename, # Default filename
      "Fichiers CSV (*.csv);;Tous les fichiers (*)"
    )

    if filePath:
      self.ui.statusbar.showMessage(f"Sauvegarde des données vers {filePath}...", 3000)
      QApplication.processEvents()
      if self.data_handler.export_to_csv(filePath):
        QMessageBox.information(self, "Exportation Réussie", f"Données sauvegardées avec succès dans :\n{filePath}")
        self.ui.statusbar.showMessage(f"Données sauvegardées : {filePath}", 5000)
        print(f"Données exportées avec succès vers {filePath}")
      else:
        QMessageBox.warning(self, "Échec de l'Exportation", "Impossible de sauvegarder les données en CSV. Vérifiez la console pour les erreurs.")
        self.ui.statusbar.showMessage("Échec de l'exportation CSV.", 5000)
        print(f"Échec de l'exportation des données vers {filePath}")
    else:
      self.ui.statusbar.showMessage("Sauvegarde CSV annulée.", 3000)
      print("Sauvegarde CSV annulée par l'utilisateur.")

  # def update_plot(self, dataframe):
  # """Placeholder for plot updating logic using self.ui.graphicsView."""
  # print("Mise à jour du graphique (logique à implémenter).")
  # # Example: if using pyqtgraph, you might have a PlotWidget or add a PlotItem
  # # self.ui.graphicsView.clear() # Or equivalent for your plotting library
  # # self.ui.graphicsView.plot(dataframe['date_heure'], dataframe['consommation_brute_totale'])


if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
