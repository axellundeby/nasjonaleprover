
import csv
import requests

def get_coordinates(address):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            location = response.json()[0]
            return (location['lat'], location['lon'])
        except (IndexError, KeyError):
            print(f"Could not find coordinates for {address}")
    return None

def csv_handler(read_path, write_path):
    with open(read_path, "rt", encoding='iso-8859-1') as f, \
         open(write_path, "w", newline='', encoding='iso-8859-1') as outfile:
        
        writer = csv.writer(outfile, delimiter=",")
        writer.writerow(["School Name", "Latitude", "Longitude", "Engelsk", "Matte", "Norsk", "Fylke", "Kommune"])
        
        reader = csv.reader((line.replace('\0', '') for line in f), delimiter="|")

        for row in reader:
            if len(row) < 16:  # Ensure row has sufficient columns
                continue
            organisasjonsnummer = row[4] 
            enhetNavn = row[8] 
            kommune = row[7]  
            fylke = row[6]

            engRes = row[9]
            norskRes = row[12]
            matteRes = row[15]

            if len(organisasjonsnummer) != 9:
                writer.writerow([enhetNavn, "0", "0", engRes, norskRes, matteRes, fylke, kommune])
            else:
                address = f"{enhetNavn}, {fylke}, {kommune}"
                tupleCord = get_coordinates(address)
                if tupleCord:
                    lat, lon = tupleCord
                else:
                    lat, lon = "0", "0"
                writer.writerow([enhetNavn, lat, lon, engRes, norskRes, matteRes, fylke, kommune])

# Set the correct paths
read_path = "data.csv"
write_path = "dataWithCords.csv"

csv_handler(read_path, write_path)

print("CSV processing complete. Output saved to:", write_path)
