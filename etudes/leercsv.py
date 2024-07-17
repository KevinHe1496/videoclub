import csv
# toma el fichedo de nuestra carpeta data
fichero = open("data/directores.csv", "r", newline="")
# aqui decimos que cuando llegue al ; de ese fichero salte a la otra linea
lector_csv = csv.reader(fichero, delimiter=";")
# aqui recorremos toda la lista que se hizo en el lector_csv
for registro in lector_csv:
    print(registro)

fichero.close()

#ahora como diccionario
fichero = open("data/directores.csv", "r", newline="")

lector_csv = csv.DictReader(fichero, delimiter=";", quotechar="'")

for registro in lector_csv:
    print(registro)

fichero.close()
