import os
import bz2
import urllib.request

DATA_DIR = "Japneet/data"
BZ2_PATH = os.path.join(DATA_DIR, "long15.mps.bz2")
MPS_PATH = os.path.join(DATA_DIR, "long15.mps")

def download_and_extract():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(BZ2_PATH):
        print("Downloading long15.mps.bz2...")
        url = "https://plato.asu.edu/ftp/lptestset/network/long15.mps.bz2"
        urllib.request.urlretrieve(url, BZ2_PATH)
        print("Download complete.")
    else:
        print("File already downloaded.")

    if not os.path.exists(MPS_PATH):
        print("Extracting file...")
        with bz2.open(BZ2_PATH, 'rb') as f_in:
            with open(MPS_PATH, 'wb') as f_out:
                f_out.write(f_in.read())
        print("Extraction complete.")
    else:
        print("File already extracted.")

    return MPS_PATH