import subprocess
import sys

def install_and_import(package, import_name=None):

    import_name = import_name or package
    
    try:
        __import__(import_name)
        
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        __import__(import_name)
        print(f"{package} installed succesfully!\n\n")

# Ensure required packages are installed
install_and_import("Pillow", "PIL")
install_and_import("requests")

from PIL import Image
import requests, os

url = input('Image\'s URL: ')

res = requests.get(url, stream = True)

img = Image.open(res.raw)

width = int(input("Maximal width of the output text (Adviced 120): "))

if img.size[0] > img.size[1]:           #size : (width, height)
    img = img.resize((width,int(img.size[1]*(width/2)/img.size[0])))
    type = "paysage"
else:
    img = img.resize((int(img.size[0]*width/img.size[1]),int(width/2)))
    type = "portrait"

img = img.convert('L')
valeurs = []

for pixel in img.getdata():
    valeurs.append(pixel)


characters = "@%#=+:-. "
n = len(characters) - 1
for i in range(len(valeurs)):
    valeurs[i] = characters[int(valeurs[i]/255 * n)]

if type == "paysage" :
    valeurs = ["".join(valeurs[i:i+width]) + "\n" for i in range(0, len(valeurs), width)]
else :
    valeurs = ["".join(valeurs[i:i+img.size[0]]) + "\n" for i in range(0, len(valeurs), img.size[0])]

filename = input("Enter the desired name of the output file (if empty, the name will be output.txt): ")
if filename == "" :
    filename = "output.txt"
elif filename[-4:] != ".txt" :
    filename += ".txt"
if filename[0] == "\\" :
    filename = filename[1:]

filepath = input("Enter the desired path of the download folder (if empty, the file will be downloaded to the same folder as the Python script): ")

if filepath == "" :
    filepath = os.path.dirname(os.path.realpath(__file__))
elif filepath[-1] != "\\" :
    filepath += "\\"
filepath = os.path.join(filepath, filename)

with open(filepath, "w") as file :
    file.writelines(valeurs)
    print("Text file saved !")
