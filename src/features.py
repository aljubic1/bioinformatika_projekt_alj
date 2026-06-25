"""
features.py

Funkcije za izračun bioinformatičkih značajki iz peptidnih sekvenci.
"""

# Uvoz pandas biblioteke za rad s tabličnim podacima.
import pandas as pd

# Definiramo 20 standardnih aminokiselina.
AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

# Definiramo Kyte-Doolittle vrijednosti hidrofobnosti za svaku aminokiselinu.
HYDROPHOBICITY_SCALE = {
    "A": 1.8,
    "C": 2.5,
    "D": -3.5,
    "E": -3.5,
    "F": 2.8,
    "G": -0.4,
    "H": -3.2,
    "I": 4.5,
    "K": -3.9,
    "L": 3.8,
    "M": 1.9,
    "N": -3.5,
    "P": -1.6,
    "Q": -3.5,
    "R": -4.5,
    "S": -0.8,
    "T": -0.7,
    "V": 4.2,
    "W": -0.9,
    "Y": -1.3
}


def calculate_length(sequence: str) -> int:
    """
    Računa duljinu peptidne sekvence.
    """

    # Vraćamo broj aminokiselina u sekvenci.
    return len(sequence)


def calculate_net_charge(sequence: str) -> int:
    """
    Računa pojednostavljeni neto naboj peptida.
    """

    # Brojimo pozitivno nabijene aminokiseline.
    positive_charge = sequence.count("K") + sequence.count("R") + sequence.count("H")

    # Brojimo negativno nabijene aminokiseline.
    negative_charge = sequence.count("D") + sequence.count("E")

    # Neto naboj je razlika pozitivnih i negativnih aminokiselina.
    net_charge = positive_charge - negative_charge

    # Vraćamo izračunati neto naboj.
    return net_charge


def calculate_hydrophobicity(sequence: str) -> float:
    """
    Računa prosječnu hidrofobnost peptidne sekvence.
    """

    # Ako je sekvenca prazna, vraćamo 0 kako bismo izbjegli dijeljenje s nulom.
    if len(sequence) == 0:
        return 0.0

    # Zbrajamo hidrofobnost svih aminokiselina u sekvenci.
    total_hydrophobicity = sum(HYDROPHOBICITY_SCALE[aa] for aa in sequence)

    # Računamo prosječnu hidrofobnost.
    average_hydrophobicity = total_hydrophobicity / len(sequence)

    # Vraćamo prosječnu hidrofobnost.
    return average_hydrophobicity


def calculate_aac(sequence: str) -> dict:
    """
    Računa aminokiselinski sastav sekvence.
    """

    # Računamo duljinu sekvence.
    sequence_length = len(sequence)

    # Kreiramo prazan rječnik za AAC značajke.
    aac_features = {}

    # Prolazimo kroz svih 20 standardnih aminokiselina.
    for amino_acid in AMINO_ACIDS:

        # Računamo udio pojedine aminokiseline u sekvenci.
        aac_features[f"AAC_{amino_acid}"] = sequence.count(amino_acid) / sequence_length

    # Vraćamo rječnik AAC značajki.
    return aac_features


def extract_features(df: pd.DataFrame,
                     sequence_column: str = "SEQUENCE") -> pd.DataFrame:
    """
    Izračunava sve značajke za skup peptidnih sekvenci.
    """

    # Kreiramo praznu listu u koju ćemo spremati značajke svake sekvence.
    feature_rows = []

    # Prolazimo kroz svaki redak DataFrame-a.
    for _, row in df.iterrows():

        # Dohvaćamo sekvencu iz zadanog stupca.
        sequence = row[sequence_column]

        # Kreiramo osnovni rječnik značajki za trenutnu sekvencu.
        features = {
            "ID": row["ID"],
            "SEQUENCE": sequence,
            "length": calculate_length(sequence),
            "net_charge": calculate_net_charge(sequence),
            "hydrophobicity": calculate_hydrophobicity(sequence),
            "label": row["label"]
        }

        # Računamo aminokiselinski sastav.
        aac_features = calculate_aac(sequence)

        # Dodajemo AAC značajke osnovnim značajkama.
        features.update(aac_features)

        # Dodajemo sve značajke u listu.
        feature_rows.append(features)

    # Pretvaramo listu rječnika u DataFrame.
    features_df = pd.DataFrame(feature_rows)

    # Vraćamo DataFrame sa značajkama.
    return features_df