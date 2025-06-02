# main.py
import sys
import pandas as pd # Pour l'annotation de type et une utilisation directe potentielle si nécessaire
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import Qt # QTimer peut être ajouté plus tard si nécessaire

# Importer votre classe UI générée et la classe DataHandler
from design_ui import Ui_MainWindow  # En supposant que votre nouveau fichier UI est design_ui.py
from data_handler import DataHandler

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.setWindowTitle("Analyse de Consommation d'Énergie") # Définir un titre de fenêtre

    self.data_handler = DataHandler()

    # --- Connecter les signaux des éléments UI aux méthodes ---
    self.ui.fetch_data.clicked.connect(self.handle_fetch_data_and_update_stats)
    self.ui.save_csv.clicked.connect(self.handle_save_csv)

    # --- État initial de l'interface utilisateur ---
    self.clear_stats_labels()
    self.ui.statusbar.showMessage("Prêt. Cliquez sur 'Récupérer Les Données' pour commencer.", 5000)
    print("MainWindow initialisée. Interface utilisateur configurée.")
    
    # Le QGraphicsView nommé 'graphicsView' est disponible via self.ui.graphicsView
    # La logique de traçage peut être ajoutée ici ou dans une méthode dédiée plus tard.
    # Pour l'instant, ce sera une vue vide.

  def clear_stats_labels(self):
    """Réinitialise toutes les étiquettes d'affichage des statistiques à '0.0' ou 'N/A'."""
    self.ui.stats_main.setText("0.0")
    self.ui.stats_std.setText("0.0")
    self.ui.stats_variance.setText("0.0")
    self.ui.stats_max.setText("0.0")
    self.ui.stats_min.setText("0.0")
    print("Étiquettes de statistiques réinitialisées.")

  def handle_fetch_data_and_update_stats(self):
    """
    Gère le clic sur le bouton 'fetch_data'.
    Récupère les données, calcule les statistiques et met à jour les étiquettes de l'interface utilisateur.
    """
    print("Bouton 'Récupérer Les Données' cliqué.")
    self.ui.statusbar.showMessage("Récupération des données en cours...", 3000)
    QApplication.processEvents()  # Garder l'interface utilisateur réactive

    # Récupérer les données (par exemple, 200 enregistrements pour un échantillon décent pour les statistiques)
    success = self.data_handler.fetch_data_from_api(limit=200)

    if success and not self.data_handler.dataframe.empty:
      self.ui.statusbar.showMessage("Données récupérées. Calcul des statistiques...", 3000)
      df = self.data_handler.dataframe
      
      # --- Choisir la colonne pour l'analyse statistique ---
      # Utilisons 'consommation_brute_totale' pour cet exemple.
      # S'assurer que cette colonne existe après le traitement dans DataHandler.
      stats_column_name = 'consommation_brute_totale'

      if stats_column_name not in df.columns:
        error_msg = f"La colonne '{stats_column_name}' est introuvable pour le calcul des statistiques."
        print(error_msg)
        QMessageBox.warning(self, "Erreur de Données", error_msg)
        self.ui.statusbar.showMessage(error_msg, 5000)
        self.clear_stats_labels()
        return

      # --- Calculer les statistiques ---
      # Le DataHandler convertit déjà les colonnes de consommation en numérique et remplit les NaN avec 0.
      # Ce fillna(0) affectera les statistiques comme min, std, variance s'il y avait beaucoup de NaN.
      selected_series = df[stats_column_name]
      
      mean_val = selected_series.mean()
      std_val = selected_series.std()
      var_val = selected_series.var()
      max_val = selected_series.max()
      min_val = selected_series.min() # Sera 0 s'il y avait des NaN remplis avec 0 et aucun autre zéro

      print(f"Statistiques pour '{stats_column_name}':")
      print(f"  Moyenne: {mean_val:.2f}, Ecart-type: {std_val:.2f}, Variance: {var_val:.2f}")
      print(f"  Min: {min_val:.2f}, Max: {max_val:.2f}")

      # --- Mettre à jour les étiquettes de l'interface utilisateur avec les statistiques calculées ---
      # Les étiquettes descriptives (par exemple, stats_main_label) ne sont pas modifiées.
      self.ui.stats_main.setText(f"{mean_val:,.2f}") # Ajout d'une virgule pour les milliers
      self.ui.stats_std.setText(f"{std_val:,.2f}")
      self.ui.stats_variance.setText(f"{var_val:,.2f}")
      self.ui.stats_max.setText(f"{max_val:,.2f}")
      self.ui.stats_min.setText(f"{min_val:,.2f}")
      
      self.ui.statusbar.showMessage("Statistiques mises à jour.", 5000)

      # Vous pourriez également mettre à jour le QTextBrowser avec un résumé général si vous le souhaitez
      # summary_text = self.data_handler.get_summary()
      # self.ui.textBrowser.setText(summary_text) # Attention, textBrowser a du HTML pré-rempli
      
      # Espace réservé pour la mise à jour du graphique
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
    Gère le clic sur le bouton 'save_csv'.
    Ouvre une boîte de dialogue pour enregistrer le dataframe actuel dans un fichier CSV.
    """
    print("Bouton 'Sauvegarder en CSV' cliqué.")
    if self.data_handler.dataframe.empty:
      QMessageBox.information(self, "Aucune Donnée", "Aucune donnée à sauvegarder. Veuillez d'abord récupérer les données.")
      print("Aucune donnée à exporter.")
      return

    # Proposer un nom de fichier par défaut avec un horodatage ou basé sur la plage de données
    default_filename = "consommation_quotidienne_export.csv"
    
    filePath, _ = QFileDialog.getSaveFileName(
      self,
      "Sauvegarder le fichier CSV",
      default_filename, # Nom de fichier par défaut
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
  # """Espace réservé pour la logique de mise à jour du graphique utilisant self.ui.graphicsView."""
  # print("Mise à jour du graphique (logique à implémenter).")
  # # Exemple : si vous utilisez pyqtgraph, vous pourriez avoir un PlotWidget ou ajouter un PlotItem
  # # self.ui.graphicsView.clear() # Ou équivalent pour votre bibliothèque de traçage
  # # self.ui.graphicsView.plot(dataframe['date_heure'], dataframe['consommation_brute_totale'])


if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())

