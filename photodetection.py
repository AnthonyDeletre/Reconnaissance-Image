import cv2 # OpenCV
import argparse # Arguments en ligne de commande
import numpy as np # Calculs
import sys # Systeme
import os # Ecriture / suppression de fichier
from imutils import paths # QoL commands
import time # Temps de calcul, pas obligé
import pytesseract
from PIL import Image # Pour Tesseract
import distance # Distance de levenshtein

# LOCAL
class Reponse:
    def __init__(self):
        self.textDetection = ""
        self.textLines = []
        self.text = ""
        self.dnnClass = None
        self.dnnConfiance = 0

    def __str__(self):
        r = "Resultats:\n"
        r += "Texte détecté:\n - - -\n"
        r += self.textDetection
        r += "\n - - -\nClasses détectées: "
        r += self.dnnClass
        r += " (conf: {})".format(self.dnnConfiance)
        return r

    def guess(self):
        self.textLines = self.textDetection.split("\n")
        self.text = self.textDetection.lower()
        r = {"Batiment": None, "Salle": None}
        # Dans l'ordre de précision: Texte, DNN
        for l in self.textLines:
            l = l.lower()
            if "amphi" in l:
                if "100" in l or "175" in l:
                    r["Batiment"] = "ISTV2"
                    r["Salle"] = l.strip()
            if "salle" in l:
                l = l.replace("salle", "")
                if "s" in l:
                    r["Batiment"] = "ISTV1"
                    r["Salle"] = l.strip()
                if "e" in l:
                    r["Batiment"] = "ISTV2"
                    r["Salle"] = l.strip()
                if "t" in l:
                    r["Batiment"] = "ISTV3"
                    r["Salle"] = l.strip()
        # DNN
        if r["Batiment"] == None:
            if self.dnnClass == "planetarium":
                r["Batiment"] = "ISTV2"
                r["Salle"] = "Exterieur"
            if "glasshouse" in self.dnnClass:
                r["Batiment"] = "ISTV3"
                r["Salle"] = "Interieur ou Exterieur"
            if "prison" in self.dnnClass:
                r["Salle"] = "Interieur"
            if r["Batiment"] == None:
                r["Batiment"] = "ISTV1?"
        return r

def main(imgfile):
    rep = Reponse()

    # Definition du lien vers Tesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

    # Creation des variables
    image = cv2.imread(imgfile)

    #  - - - Detection de texte - - - #
    # On passe l'image en niveaux de gris, puis on applique la méthode de treshold
    # pour avoir l'image en N/B
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_treshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # On stocke l'image dans un fichier temporaire pour appliquer Tesseract
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray_treshold)
    # Lecture de l'image par Tesseract. On supprime ensuite l'image temporaire
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    rep.textDetection = text

    # - - - Deep Neural Network - - - #
    # Selection du backend pour aller vite
    # ainsi que les liens vers les réseaux Caffe, et de config.
    # Ils doivent être dans le même dossier que le .py. SINON.
    backend = cv2.dnn.DNN_BACKEND_DEFAULT
    target = cv2.dnn.DNN_TARGET_CPU
    model = "bvlc_googlenet.caffemodel"
    prototxt = "bvlc_googlenet.prototxt"
    classes = "classification_classes_ILSVRC2012.txt"
    # Ouverture des fichiers
    with open(classes, 'r') as f:
        classes = f.read().rstrip('\n').split('\n')
    # On crée le "détecteur"
    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    net.setPreferableBackend(backend)
    net.setPreferableTarget(target)
    # Lecture de l'image
    cap = cv2.VideoCapture(imgfile)
    _, frame = cap.read()
    # Preprocessing:
    # On crée le blob de l'image: On change l'image de sorte qu'elle soit lisible par
    # OpenCV.dnn
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), [0,0,0], crop = False)
    # On indique au détecteur que l'image a analyser est le blob créé
    net.setInput(blob)
    out = net.forward()
    out = out.flatten()
    # Le réseau de neurones trouve la similarité la plus proche
    # On demande a Numpy de sélectionner le meilleur résultat
    classId = np.argmax(out)
    confidence = out[classId]
    rep.dnnClass = classes[classId]
    rep.dnnConfiance = out[classId]

    # print(rep)
    print(rep.guess())

if __name__ == "__main__":
    # Arguments: -i <nom de la photo>
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="Nom du fichier")
    args = vars(ap.parse_args())
    main(args["image"])
