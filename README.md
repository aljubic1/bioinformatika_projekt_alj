# Klasifikacija antimikrobnih peptida primjenom strojnog učenja

## Opis projekta

Ovaj projekt izrađen je u sklopu kolegija iz bioinformatike.

Cilj projekta je razviti model strojnog učenja koji razlikuje antimikrobne peptide (AMP) od neantimikrobnih peptida (non-AMP) na temelju bioinformatičkih značajki dobivenih iz njihovih aminokiselinskih sekvenci.

Projekt obuhvaća cijeli postupak analize podataka:
- pripremu i čišćenje podataka,
- izračun bioinformatičkih značajki,
- treniranje modela strojnog učenja,
- evaluaciju rezultata i interpretaciju modela.

---

## Struktura projekta

```
bioinformatics-ds-project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling.ipynb
│   └── 04_evaluation.ipynb
│
├── results/
│
├── src/
│   ├── data_utils.py
│   └── features.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Skupovi podataka

Projekt koristi dva izvora podataka:

- **DBAASP** – antimikrobni peptidi (AMP)
- **AMPBenchmark** – neantimikrobni peptidi (non-AMP)

Nakon čišćenja i pripreme formiran je uravnotežen skup podataka koji sadrži:

- 1672 AMP sekvence
- 1672 non-AMP sekvence

Ukupno:

- **3344 peptidne sekvence**

---

## Izračunate značajke

Za svaku peptidnu sekvencu izračunate su sljedeće značajke:

- duljina sekvence (Length)
- neto naboj (Net charge)
- prosječna hidrofobnost (Hydrophobicity)
- aminokiselinski sastav (AAC)

---

## Primijenjeni modeli

Za klasifikaciju peptida korištena su dva modela strojnog učenja:

- Random Forest
- Support Vector Machine (SVM)

---

## Rezultati

Dobiveni rezultati pokazali su vrlo visoku uspješnost oba modela.

| Model | Accuracy | Precision | Recall | F1-score |
|--------|---------:|----------:|-------:|---------:|
| Random Forest | 93.12 % | 92.35 % | 94.01 % | 93.18 % |
| SVM | 92.97 % | 93.09 % | 92.81 % | 92.95 % |

Random Forest ostvario je nešto bolje ukupne performanse te je odabran kao uspješniji model.

---

## Pokretanje projekta

1. Klonirati repozitorij:

```bash
git clone https://github.com/aljubic1/bioinformatika_projekt_alj.git
```

2. Instalirati potrebne biblioteke:

```bash
pip install -r requirements.txt
```

3. Pokrenuti notebooke redom:

- 01_data_preparation.ipynb
- 02_feature_engineering.ipynb
- 03_modeling.ipynb
- 04_evaluation.ipynb

---

## Korištene biblioteke

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- BioPython

---

## Autor
Ana Ljubić

Projekt izrađen iz kolegija Bioinformatika.