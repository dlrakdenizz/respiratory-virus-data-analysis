
import csv
from pathlib import Path

import requests

API_URL = "https://data.cdc.gov/resource/jqxy-cyu2.json"
OUTPUT_FILE = Path("raw_data/cdc_respiratory_viruses_raw.csv")
PAGE_SIZE = 5000

COLUMNS = [
    "pathogen",
    "mmwr_week_start",
    "mmwr_week_end",
    "geography_type",
    "geography_value",
    "test_count",
    "positive_count",
    "percent_pos",
]


def collect_data():
    all_records = []
    offset = 0

    while True:
        params = {
            "$limit": PAGE_SIZE,
            "$offset": offset,
            "$order": ":id",
        }

        response = requests.get(
            API_URL,
            params=params,
            timeout=60,
        )
        response.raise_for_status()

        records = response.json()
        all_records.extend(records)

        print(
            f"Downloaded {len(records)} records "
            f"(total: {len(all_records)})"
        )

        if len(records) < PAGE_SIZE:
            break

        offset += PAGE_SIZE

    return all_records


def save_csv(records):
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=COLUMNS,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(records)

    print(f"Saved to: {OUTPUT_FILE}")


def main():
    records = collect_data()

    if not records:
        print("No records received.")
        return

    save_csv(records)
    print(f"Total records collected: {len(records)}")


if __name__ == "__main__":
    main()
