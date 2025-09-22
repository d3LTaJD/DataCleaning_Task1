import pandas as pd

# load
df = pd.read_csv("internship/Netflix_movies_and_tv_shows_clustering.csv/Netflix_movies_and_tv_shows_clustering.csv")

print(df.shape)
print(df.head())
print(df.info())

# --- fill missing values (fixed a stray comma and kept your defaults) ---
df["director"] = df["director"].fillna("unknown")
df["cast"] = df["cast"].fillna("not available")
df["country"] = df["country"].fillna("unknown")
df["rating"] = df["rating"].fillna("unrated")

# --- parse dates safely ---
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

# --- duplicates ---
print("before removing duplicates:", df.shape)
df.drop_duplicates(inplace=True)
print("after removing duplicates:", df.shape)

# --- normalize text & whitespace ---
if "type" in df.columns:
    df["type"] = df["type"].astype(str).str.lower().str.strip()
if "country" in df.columns:
    # title-case each comma-separated country and strip whitespace
    df["country"] = df["country"].astype(str).apply(lambda x: ", ".join([p.strip().title() for p in x.split(",")]))

# --- format date as YYYY-MM-DD (will produce NaN for unparsable dates) ---
df["date_added"] = df["date_added"].dt.strftime("%Y-%m-%d")

# --- tidy column names ---
df.columns = df.columns.str.lower().str.replace(" ", "_")

print(df.dtypes)

# --- convert release_year safely to integer (nullable) ---
if "release_year" in df.columns:
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")

# --- save cleaned file ---
df.to_csv("netflix_Cleaned_dataset.csv", index=False)
print("Saved netflix_Cleaned_dataset.csv")
