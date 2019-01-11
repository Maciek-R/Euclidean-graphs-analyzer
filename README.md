# Projekt GIS

## Badanie właściwości grafów Euklidesowych

Należy zaimplementować generator sieci euklidesowych, a następnie zbadać prawdopodobieństwo spójności sieci i okreslić rozmiar największej składowej spójnej w zależności od liczby i zasięgu wierzchołków.

Aby uruchomić program testujący, uruchom plik `analyze_graphs.py`. Przykład użycia:
```sh
python3 ./analyze_graphs.py -v
	--start_size=10000 --stop_size=20000 --size_step=100
	--start_radius=0.01 --stop_radius=0.02 --radius_step=0.001
	--jobs=8 --repeats=100 --output_dir=output
```

## Autorzy

1. Maciej Ruszczyk
2. Adam Kowalewski
