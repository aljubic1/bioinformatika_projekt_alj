"""
data_utils.py

Funkcije za učitavanje, provjeru i pripremu peptidnih sekvenci
za projekt klasifikacije antimikrobnih peptida.
"""

# Uvoz biblioteke pandas za rad s tabličnim podacima.
import pandas as pd

# Uvoz Path klase za sigurniji rad s putanjama datoteka.
from pathlib import Path

# Definiramo skup od 20 standardnih aminokiselina.
STANDARD_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Sigurno učitava CSV datoteku i vraća DataFrame.
    """

    # Pretvaramo putanju u Path objekt.
    file_path = Path(file_path)

    # Provjeravamo postoji li datoteka.
    if not file_path.exists():
        raise FileNotFoundError(f"Datoteka ne postoji: {file_path}")

    # Učitavamo CSV datoteku.
    df = pd.read_csv(file_path)

    # Provjeravamo je li datoteka prazna.
    if df.empty:
        raise ValueError("Učitana datoteka je prazna.")

    # Vraćamo učitani DataFrame.
    return df


def check_required_columns(df: pd.DataFrame, required_columns: list) -> None:
    """
    Provjerava postoje li potrebni stupci u DataFrame-u.
    """

    # Pronalaženje stupaca koji nedostaju.
    missing_columns = [column for column in required_columns if column not in df.columns]

    # Ako neki stupci nedostaju, zaustavljamo program.
    if missing_columns:
        raise ValueError(f"Nedostaju obavezni stupci: {missing_columns}")


def print_dataset_info(df: pd.DataFrame) -> None:
    """
    Ispisuje osnovne informacije o skupu podataka.
    """

    # Ispis broja redaka i stupaca.
    print(f"Broj redaka: {df.shape[0]}")

    # Ispis broja stupaca.
    print(f"Broj stupaca: {df.shape[1]}")

    # Ispis naziva stupaca.
    print(f"Stupci: {list(df.columns)}")


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Vraća broj nedostajućih vrijednosti po stupcima.
    """

    # Računamo broj nedostajućih vrijednosti za svaki stupac.
    missing_values = df.isna().sum()

    # Vraćamo rezultat.
    return missing_values


def filter_monomers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Zadržava samo monomerne peptide.
    """

    # Provjeravamo postoji li stupac COMPLEXITY.
    check_required_columns(df, ["COMPLEXITY"])

    # Zadržavamo samo retke gdje je COMPLEXITY jednak Monomer.
    monomer_df = df[df["COMPLEXITY"] == "Monomer"].copy()

    # Resetiramo indeks nakon filtriranja.
    monomer_df = monomer_df.reset_index(drop=True)

    # Vraćamo filtrirani DataFrame.
    return monomer_df


def standardize_sequence(sequence: str) -> str:
    """
    Standardizira zapis peptidne sekvence.
    """

    # Ako je vrijednost prazna, vraćamo prazan string.
    if pd.isna(sequence):
        return ""

    # Pretvaramo sekvencu u string.
    sequence = str(sequence)

    # Uklanjamo praznine na početku i kraju.
    sequence = sequence.strip()

    # Pretvaramo sekvencu u velika slova.
    sequence = sequence.upper()

    # Vraćamo standardiziranu sekvencu.
    return sequence


def is_valid_sequence(sequence: str) -> bool:
    """
    Provjerava sadrži li sekvenca samo standardne aminokiseline.
    """

    # Standardiziramo sekvencu prije provjere.
    sequence = standardize_sequence(sequence)

    # Ako je sekvenca prazna, nije valjana.
    if len(sequence) == 0:
        return False

    # Provjeravamo sadrži li sekvenca samo dopuštene aminokiseline.
    return set(sequence).issubset(STANDARD_AMINO_ACIDS)


def clean_sequences(df: pd.DataFrame) -> pd.DataFrame:
    """
    Čisti sekvence i uklanja neispravne zapise.
    """

    # Provjeravamo postoji li stupac SEQUENCE.
    check_required_columns(df, ["SEQUENCE"])

    # Kopiramo podatke kako ne bismo mijenjali originalni DataFrame.
    cleaned_df = df.copy()

    # Standardiziramo sve sekvence.
    cleaned_df["SEQUENCE"] = cleaned_df["SEQUENCE"].apply(standardize_sequence)

    # Dodajemo pomoćni stupac koji označava ispravnost sekvence.
    cleaned_df["VALID_SEQUENCE"] = cleaned_df["SEQUENCE"].apply(is_valid_sequence)

    # Zadržavamo samo ispravne sekvence.
    cleaned_df = cleaned_df[cleaned_df["VALID_SEQUENCE"]].copy()

    # Uklanjamo pomoćni stupac.
    cleaned_df = cleaned_df.drop(columns=["VALID_SEQUENCE"])

    # Uklanjamo duplikate prema sekvenci.
    cleaned_df = cleaned_df.drop_duplicates(subset=["SEQUENCE"])

    # Resetiramo indeks nakon čišćenja.
    cleaned_df = cleaned_df.reset_index(drop=True)

    # Vraćamo očišćeni DataFrame.
    return cleaned_df


def add_label(df: pd.DataFrame, label: int) -> pd.DataFrame:
    """
    Dodaje oznaku klase u DataFrame.
    """

    # Provjeravamo je li label ispravan.
    if label not in [0, 1]:
        raise ValueError("Label mora biti 0 ili 1.")

    # Kopiramo DataFrame.
    labeled_df = df.copy()

    # Dodajemo stupac label.
    labeled_df["label"] = label

    # Vraćamo DataFrame s oznakom.
    return labeled_df


def save_processed_dataset(df: pd.DataFrame, output_path: str) -> None:
    """
    Sprema obrađeni skup podataka u CSV datoteku.
    """

    # Pretvaramo izlaznu putanju u Path objekt.
    output_path = Path(output_path)

    # Kreiramo direktorij ako ne postoji.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Spremamo DataFrame u CSV bez indeksa.
    df.to_csv(output_path, index=False)


    " dodajemo non-AMP"
    def load_ampbenchmark_fasta(file_path: str) -> pd.DataFrame:
    """
    Učitava AMPBenchmark FASTA datoteku i izdvaja sekvence s oznakama.
    """

    # Pretvaramo putanju u Path objekt.
    file_path = Path(file_path)

    # Provjeravamo postoji li FASTA datoteka.
    if not file_path.exists():
        raise FileNotFoundError(f"Datoteka ne postoji: {file_path}")

    # Kreiramo praznu listu za zapise iz FASTA datoteke.
    records = []

    # Otvaramo FASTA datoteku u načinu za čitanje.
    with open(file_path, "r", encoding="utf-8") as fasta_file:

        # Postavljamo početne vrijednosti za zaglavlje i sekvencu.
        header = None
        sequence_parts = []

        # Prolazimo kroz svaki redak FASTA datoteke.
        for line in fasta_file:

            # Uklanjamo praznine i prijelome redova.
            line = line.strip()

            # Preskačemo prazne retke.
            if not line:
                continue

            # Provjeravamo je li redak FASTA zaglavlje.
            if line.startswith(">"):

                # Ako već imamo prethodni zapis, spremamo ga.
                if header is not None:

                    # Spajamo dijelove sekvence u jedan string.
                    sequence = "".join(sequence_parts)

                    # Dodajemo zapis u listu.
                    records.append({
                        "ID": header,
                        "SEQUENCE": sequence
                    })

                # Spremamo novo zaglavlje bez znaka >.
                header = line[1:]

                # Resetiramo listu dijelova sekvence.
                sequence_parts = []

            else:

                # Dodajemo redak sekvence u listu dijelova.
                sequence_parts.append(line)

        # Spremamo zadnji FASTA zapis nakon završetka petlje.
        if header is not None:

            # Spajamo dijelove zadnje sekvence.
            sequence = "".join(sequence_parts)

            # Dodajemo zadnji zapis u listu.
            records.append({
                "ID": header,
                "SEQUENCE": sequence
            })

    # Pretvaramo listu zapisa u DataFrame.
    df = pd.DataFrame(records)

    # Vraćamo DataFrame.
    return df


def extract_ampbenchmark_by_label(df: pd.DataFrame, label: int) -> pd.DataFrame:
    """
    Izdvaja zapise iz AMPBenchmark skupa prema oznaci AMP=0 ili AMP=1.
    """

    # Provjeravamo je li label ispravan.
    if label not in [0, 1]:
        raise ValueError("Label mora biti 0 ili 1.")

    # Kopiramo DataFrame.
    filtered_df = df.copy()

    # Kreiramo tekstualni uzorak koji tražimo u ID stupcu.
    label_pattern = f"AMP={label}"

    # Zadržavamo samo zapise koji u ID-u sadrže traženi label.
    filtered_df = filtered_df[filtered_df["ID"].str.contains(label_pattern, regex=False)].copy()

    # Dodajemo numeričku oznaku klase.
    filtered_df["label"] = label

    # Resetiramo indeks.
    filtered_df = filtered_df.reset_index(drop=True)

    # Vraćamo filtrirani DataFrame.
    return filtered_df