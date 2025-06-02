
"""
Module pour la gestion de la récupération et du traitement des données de consommation d'énergie.
"""
import requests
import pandas as pd
from pathlib import Path # Pour la gestion des chemins multi-plateformes si sauvegarde de fichiers

API_URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-quotidienne-brute/records"

class DataHandler:
  """
  Gère la récupération, le traitement et la gestion des données de consommation d'énergie.
  """
  def __init__(self, api_url: str = API_URL):
    """
    Initialise le DataHandler.

    Args:
      api_url (str): L'URL de base pour l'API de données.
    """
    self.api_url = api_url
    self.dataframe = pd.DataFrame()
    print("DataHandler initialisé.")

  def fetch_data_from_api(self, limit: int = 100, offset: int = 0) -> bool:
    """
    Récupère les données depuis l'API ODRE.

    Args:
      limit (int): Nombre d'enregistrements à récupérer.
      offset (int): Décalage pour la pagination.

    Returns:
      bool: True si la récupération des données a réussi, False sinon.
    """
    params = {
      "limit": 100,
      # "offset": offset,
      # "order_by": "date_heure DESC" # Obtenir les données les plus récentes
    }
    print(f"Récupération des données depuis l'API : {self.api_url} avec les paramètres : {params}")
    try:
      response = requests.get(self.api_url, params=params, timeout=10)
      response.raise_for_status()  # Lève une HTTPError pour les mauvaises réponses (4XX ou 5XX)
      data = response.json()
      
      if 'results' not in data or not data['results']:
        print("Aucun résultat trouvé dans la réponse de l'API.")
        self.dataframe = pd.DataFrame() # S'assurer que le dataframe est vide
        return False

      self.dataframe = pd.DataFrame(data['results'])
      print(f"Données récupérées avec succès. {len(self.dataframe)} enregistrements obtenus.")
      self._process_data()
      return True
    except requests.exceptions.RequestException as e:
      print(f"Erreur lors de la récupération des données depuis l'API : {e}")
      self.dataframe = pd.DataFrame() # S'assurer que le dataframe est vide
      return False
    except Exception as e:
      print(f"Une erreur inattendue s'est produite lors de la récupération API : {e}")
      self.dataframe = pd.DataFrame()
      return False

  def _process_data(self):
    """
    Traite les données récupérées.
    - Convertit 'date_heure' en objets datetime.
    - Remplit les valeurs NaN dans les colonnes de consommation par 0 pour le traçage.
    """
    if self.dataframe.empty:
      print("Aucune donnée à traiter.")
      return

    print("Traitement des données...")
    if 'date_heure' in self.dataframe.columns:
      self.dataframe['date_heure'] = pd.to_datetime(self.dataframe['date_heure'], errors='coerce')
      self.dataframe.sort_values('date_heure', inplace=True) # Assurer l'ordre chronologique pour le traçage
    
    consumption_cols = [
      'consommation_brute_gaz_grtgaz', 'consommation_brute_gaz_terega',
      'consommation_brute_gaz_totale', 'consommation_brute_electricite_rte',
      'consommation_brute_totale'
    ]
    for col in consumption_cols:
      if col in self.dataframe.columns:
        # Convertir en numérique, forcer les erreurs en NaN, puis remplir NaN par 0
        self.dataframe[col] = pd.to_numeric(self.dataframe[col], errors='coerce').fillna(0)
      else:
        print(f"Avertissement : Colonne attendue '{col}' non trouvée dans les données. Création avec des 0.")
        self.dataframe[col] = 0 # Ajouter la colonne si manquante pour éviter des erreurs ultérieures
    
    print("Traitement des données terminé.")

  def get_summary(self) -> str:
    """
    Retourne un résumé textuel du dataframe actuel.
    """
    if self.dataframe.empty:
      return "Aucune donnée chargée."
    
    summary = f"Résumé des données :\n"
    summary += f"- Nombre total d'enregistrements : {len(self.dataframe)}\n"
    if 'date_heure' in self.dataframe.columns and not self.dataframe['date_heure'].dropna().empty:
      min_date = self.dataframe['date_heure'].min().strftime('%Y-%m-%d %H:%M')
      max_date = self.dataframe['date_heure'].max().strftime('%Y-%m-%d %H:%M')
      summary += f"- Plage de dates : {min_date} à {max_date}\n"
    
    for col in ['consommation_brute_electricite_rte', 'consommation_brute_gaz_totale']:
      if col in self.dataframe.columns:
        total_col = self.dataframe[col].sum()
        mean_col = self.dataframe[col].mean()
        summary += f"- Total {col}: {total_col:,.0f}\n"
        summary += f"- Moyenne {col}: {mean_col:,.0f}\n"
    return summary

  def export_to_csv(self, filepath: str) -> bool:
    """
    Exporte le dataframe actuel vers un fichier CSV.

    Args:
      filepath (str): Le chemin pour sauvegarder le fichier CSV.

    Returns:
      bool: True si l'exportation a réussi, False sinon.
    """
    if self.dataframe.empty:
      print("Aucune donnée à exporter.")
      return False
    try:
      path_obj = Path(filepath)
      self.dataframe.to_csv(path_obj, index=False, encoding='utf-8')
      print(f"Données exportées avec succès vers {filepath}")
      return True
    except Exception as e:
      print(f"Erreur lors de l'exportation des données vers CSV : {e}")
      return False

  def get_plot_options(self) -> list:
    """
    Retourne une liste des colonnes disponibles pour le traçage.
    """
    if self.dataframe.empty:
      return ["Aucune donnée"]
    
    options = [
      'consommation_brute_electricite_rte',
      'consommation_brute_gaz_totale',
      'consommation_brute_totale',
      'consommation_brute_gaz_grtgaz',
      'consommation_brute_gaz_terega'
    ]
    # Retourner uniquement les colonnes qui existent réellement dans le dataframe
    return [opt for opt in options if opt in self.dataframe.columns]
  