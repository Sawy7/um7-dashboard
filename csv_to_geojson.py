import sys, csv, json

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Error: You need to provide .csv file (only).\nSyntax: python {sys.argv[0]} [file.csv]")

    geojson = {
        "type": "LineString",
        "coordinates": []
    }

    with open(sys.argv[1], "r") as csv_file:
        csvreader = csv.DictReader(csv_file)
        for row in csvreader:
            try:
                long = float(row["gps_longitude"])
                lat = float(row["gps_latitude"])
                alt = float(row["gps_altitude"])
                if long == 0 or lat == 0 or alt == 0:
                    continue
                geojson["coordinates"].append([long, lat, alt])
            except:
                pass
    print(json.dumps(geojson))
