import csv

print("Outlier detection started.")

with open('/data.csv') as csvfile:
    rows = csv.reader(csvfile, delimiter=' ')
    for r in rows:
        if int(r[1]) > 110:
            print("Outlier detected at timestep:", r[0],"- outlier value:",r[1])

print("Outlier detection finished.")