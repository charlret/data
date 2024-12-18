import datetime as d
import pandas as pd
import zstandard as zstd
import io
import os
from pathlib import Path

def decompress_zst(file_path):
    with open(file_path, 'rb') as compressed_file:
        dctx = zstd.ZstdDecompressor()
        decompressed_data = dctx.stream_reader(compressed_file)
        return decompressed_data

def parse_pgn_to_dataframe(pgn_data):
    games = []
    current_game = {}
    
    for line in pgn_data:
        line = line.strip()
        if line.startswith("["):  # Métadonnées de la partie
            key, value = line[1:-1].split(" ", 1)
            current_game[key] = value.strip('"')
        elif line == "":  # Fin d'une partie
            if current_game:
                games.append(current_game)
                current_game = {}
    
    # Convertir les données en DataFrame
    return pd.DataFrame(games)

file_path = "D:\\Data.zst"
if os.path.exists(file_path):
    print("Le fichier existe.")
else:
    print("Le fichier est introuvable.")
