"""Clean the Netflix titles snapshot and create analysis-ready tables."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "netflix_titles.csv"
OUT = ROOT / "data" / "cleaned"

RATING_GROUPS = {
    "TV-Y": "Kids", "TV-Y7": "Kids", "TV-G": "Kids", "G": "Kids", "TV-Y7-FV": "Kids",
    "TV-PG": "Teens", "PG": "Teens", "PG-13": "Teens", "TV-14": "Teens",
    "R": "Adults", "NC-17": "Adults", "TV-MA": "Adults",
}

def clean_data(raw_path=RAW, output_dir=OUT):
    """Return a cleaned frame and save normalized one-value-per-row tables."""
    raw_path, output_dir = Path(raw_path), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(raw_path)
    # Normalize text first, then remove exact duplicate records.
    text_columns = df.select_dtypes(include="object").columns
    for column in text_columns:
        df[column] = df[column].str.strip()
    rows_before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    # These descriptive fields can contain several values; Unknown preserves titles
    # while keeping missingness explicit. Rating/date/duration stay missing if unknown.
    for column in ["director", "cast", "country"]:
        df[column] = df[column].fillna("Unknown")
    # The source occasionally stores a duration (for example "74 min") in rating.
    misplaced = df["rating"].str.fullmatch(r"\d+\s*min", case=False, na=False)
    df.loc[misplaced & df["duration"].isna(), "duration"] = df.loc[misplaced & df["duration"].isna(), "rating"]
    df.loc[misplaced, "rating"] = pd.NA
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month.astype("Int64")
    df["month_name_added"] = df["date_added"].dt.month_name()
    parts = df["duration"].str.extract(r"(?P<duration_value>\d+)\s*(?P<duration_unit>min|Season|Seasons)", expand=True)
    df["duration_value"] = pd.to_numeric(parts["duration_value"], errors="coerce").astype("Int64")
    df["duration_unit"] = parts["duration_unit"].str.lower()
    df["movie_minutes"] = df["duration_value"].where(df["type"].eq("Movie") & df["duration_unit"].eq("min"))
    df["seasons"] = df["duration_value"].where(df["type"].eq("TV Show") & df["duration_unit"].str.startswith("season", na=False))
    df["rating_group"] = df["rating"].map(RATING_GROUPS).fillna("Not Rated")
    df["content_age"] = df["year_added"] - df["release_year"].astype("Int64")
    df.to_csv(output_dir / "netflix_cleaned.csv", index=False)
    # Explode delimited dimensions so each title contributes once per value.
    for column, filename in [("country", "netflix_by_country.csv"), ("listed_in", "netflix_by_genre.csv"), ("cast", "netflix_by_cast.csv"), ("director", "netflix_by_director.csv")]:
        exploded = df.assign(**{column: df[column].fillna("Unknown").str.split(r",\s*")}).explode(column)
        exploded[column] = exploded[column].str.strip()
        exploded.to_csv(output_dir / filename, index=False)
    summary = {"rows_before": rows_before, "rows_after": len(df), "duplicates_removed": rows_before-len(df),
               "nulls_before": pd.read_csv(raw_path).isna().sum().to_dict(), "nulls_after": df.isna().sum().to_dict(),
               "misplaced_rating_rows": int(misplaced.sum())}
    return df, summary

if __name__ == "__main__":
    frame, summary = clean_data()
    print(f"Rows: {summary['rows_before']:,} -> {summary['rows_after']:,}; duplicates removed: {summary['duplicates_removed']:,}")
    print("Nulls after cleaning:")
    print(frame.isna().sum().to_string())
