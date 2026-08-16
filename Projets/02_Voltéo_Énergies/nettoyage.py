import pandas as pd
import numpy as np

# Lecture
df = pd.read_csv("production_brute.csv", sep=";")

# 1. Noms de sites
df["site"] = (
    df["site"]
    .str.lower()
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

df["site"] = df["site"].replace({
    "mistral": "parc mistral"
})

# 2. Virgule décimale -> point
df["production"] = (
    df["production"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df["production"] = pd.to_numeric(
    df["production"],
    errors="coerce"
)

# 3. Valeurs manquantes
df["production"] = df["production"].replace(
    -9999,
    np.nan
)

# 4. Valeurs négatives
df.loc[
    df["production"] < 0,
    "production"
] = np.nan

# 5. MW -> kW
mw = df["unite"].str.lower() == "mw"

df.loc[mw, "production"] *= 1000

df["unite"] = "kW"

# 6. Suppression des doublons stricts
df = df.drop_duplicates()

# 7. Même site + même horodatage
df = df.drop_duplicates(
    subset=["site", "horodatage"],
    keep="first"
)

# Export
df.to_csv(
    "production_propre.csv",
    sep=";",
    index=False,
    na_rep="NaN"
)

print(df.shape)
print(df.head())