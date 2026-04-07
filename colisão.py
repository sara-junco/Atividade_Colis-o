from ultralytics import YOLO

# Verificar colisão entre dois objetos
def ha_colisao(boxA, boxB, limiar=0.10):
 # Coordenadas das caixas
    x1A, y1A, x2A, y2A = boxA
    x1B, y1B, x2B, y2B = boxB

# Calcula área de interseção
    x1 = max(x1A, x1B)
    y1 = max(y1A, y1B)
    x2 = min(x2A, x2B)
    y2 = min(y2A, y2B)

    largura = max(0, x2 - x1)
    altura = max(0, y2 - y1)
    
    intersecao = largura * altura

# Área de cada objeto
    area1 = (x2A - x1A) * (y2A - y1A)
    area2 = (x2B - x1B) * (y2B - y1B)
    
    menor_area = min(area1, area2)
    
    if menor_area <= 0:
      return False, 0.0
    percentual = intersecao / menor_area
    
    return percentual >= limiar, percentual

# Carrega modelo
model = YOLO("yolo26n.pt")

# Importa video de colisão
import cv2
cap = cv2.VideoCapture("video.mp4")

while True:
    ret, imagem = cap.read()
    if not ret:
        break

    results = model(imagem)

    # Lista para armazenar carros detectados
    veiculos = []

 # FILTRAR CARROS
    for c in results:
        for box in c.boxes:
            classe = int(box.cls[0])
            if classe == 2:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                veiculos.append((x1, y1, x2, y2))

                cv2.rectangle(imagem, (x1,y1), (x2,y2), (0,255,0), 2)

# VERIFICAR COLISÕES
    for i in range(len(veiculos)):
        for j in range(i+1, len(veiculos)):
              colisao, percentual = ha_colisao(veiculos[i], veiculos[j])

              if colisao:
                   print(f"Colisão entre veículo {i} e {j}")
                   print(f"Percentual: {percentual*100:.2f}%")
                  