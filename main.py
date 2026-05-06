import face_recognition
import cv2
import os
from flask import Flask, Response

app = Flask(__name__)

# Confirguration
DOSSIER_VISAGES = "visages_connus"

# Chargement des visages connus de mon dossier
encodages_connus = []
noms_connus = []

for nom_fichier in os.listdir(DOSSIER_VISAGES):
    if nom_fichier.endswith(".jpg") or nom_fichier.endswith(".png"):
        chemin = os.path.join(DOSSIER_VISAGES, nom_fichier)
        image = face_recognition.load_image_file(chemin)
        encodages = face_recognition.face_encodings(image)
        if len(encodages) > 0:
            encodages_connus.append(encodages[0])
            noms_connus.append(os.path.splitext(nom_fichier)[0])
            print(f"Visage chargé : {os.path.splitext(nom_fichier)[0]}")

print(f"\n{len(noms_connus)} visage(s) chargé(s) : {noms_connus}")

# Flux vidéo avec reconnaissance
def generer_flux():
    cap = cv2.VideoCapture(0)
    compteur = 0
    derniers_noms = []
    dernieres_positions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Analyse d'une seule image sur 3 pour améliorer les performances
        if compteur % 3 == 0:
            petit_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = cv2.cvtColor(petit_frame, cv2.COLOR_BGR2RGB)
            dernieres_positions = face_recognition.face_locations(rgb_frame)
            encodages_frame = face_recognition.face_encodings(rgb_frame, dernieres_positions)
            derniers_noms = []

            for encodage in encodages_frame:
                correspondances = face_recognition.compare_faces(encodages_connus, encodage)
                nom = "Inconnu"
                if True in correspondances:
                    index = correspondances.index(True)
                    nom = noms_connus[index]
                derniers_noms.append(nom)

        # Dessiner les rectangles et noms sur l'image
        for (position, nom) in zip(dernieres_positions, derniers_noms):
            haut, droite, bas, gauche = position
            haut, droite, bas, gauche = haut*4, droite*4, bas*4, gauche*4
            cv2.rectangle(frame, (gauche, haut), (droite, bas), (0, 255, 0), 2)
            cv2.putText(frame, nom, (gauche, haut - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        compteur += 1
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Routes flask pour interface par le web
@app.route('/')
def index():
    return '''
    <html>
    <head><title>Reconnaissance Faciale</title></head>
    <body style="background:black; display:flex; justify-content:center; align-items:center; height:100vh; margin:0">
        <img src="/video" style="max-width:100%">
    </body>
    </html>
    '''

@app.route('/video')
def video():
    return Response(generer_flux(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Lancement
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)