# figma_style_checker.py

import os
import requests
from PIL import Image
from io import BytesIO
from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2
from dotenv import load_dotenv

# === CARREGAR VARIÁVEIS DE AMBIENTE ===
load_dotenv(dotenv_path=".env")

FIGMA_TOKEN = os.environ.get("FIGMA_TOKEN")
SCREENSHOT_API_KEY = os.environ.get("SCREENSHOT_API_KEY")  # Ex: apiflash, urlbox, etc.

if not FIGMA_TOKEN or not SCREENSHOT_API_KEY:
    raise EnvironmentError("Certifique-se de definir FIGMA_TOKEN e SCREENSHOT_API_KEY no arquivo .env")

# === 1. PEGAR ESTILOS DO FIGMA ===
def get_figma_styles(file_key, figma_node_key):
    url = f"https://api.figma.com/v1/files/{file_key}?id={figma_node_key}"
    headers = {
        "X-Figma-Token": f"{FIGMA_TOKEN}"
    }
    # response = requests.get(url, headers=headers)
    print("Acessando Figma:", url)
    print("Authorization:", headers["X-Figma-Token"])
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.json()
        styles = []
        for page in data['document']['children']:
            for node in page.get('children', []):
                styles.append({
                    'name': node.get('name'),
                    'type': node.get('type'),
                    'style': node.get('styles', {})
                })
        return styles
    else:
        print("Erro ao acessar Figma:", response.text)
        return []

# === 2. TIRAR PRINT DA TELA ===
def get_screenshot_from_url(url):
    screenshot_url = f"https://api.apiflash.com/v1/urltoimage?access_key={SCREENSHOT_API_KEY}&url={url}"
    print("Capturando screenshot de:", url)
    print("URL de screenshot:", screenshot_url)
    print("SCREENSHOT_API_KEY:", SCREENSHOT_API_KEY)

    response = requests.get(screenshot_url, verify=False)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print("Erro ao capturar screenshot:", response.text)
        return None

# === 3. COMPARAR DUAS IMAGENS ===
def compare_images(img1, img2):
    img1_gray = cv2.cvtColor(np.array(img1), cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(np.array(img2), cv2.COLOR_BGR2GRAY)

    img1_gray = cv2.resize(img1_gray, (min(img1_gray.shape[1], img2_gray.shape[1]), min(img1_gray.shape[0], img2_gray.shape[0])))
    img2_gray = cv2.resize(img2_gray, img1_gray.shape[::-1])

    score, diff = ssim(img1_gray, img2_gray, full=True)
    diff = (diff * 255).astype("uint8")

    print(f"SSIM Score: {score:.4f}")
    return score, diff

# === 4. EXEMPLO DE USO ===
if __name__ == "__main__":
    figma_file_key = input("Digite o Figma File Key: ")
    figma_node_key = input("Digite o Figma Node Key: ")
    site_url = input("Digite a URL do site: ")

    figma_url = f"https://www.figma.com/design/{figma_file_key}?node-id={figma_node_key}"

    styles = get_figma_styles(figma_file_key, figma_node_key)
    print("Estilos do Figma:", styles[:3])  # mostra os 3 primeiros

    figma_img = get_screenshot_from_url(figma_url)
    site_img = get_screenshot_from_url(site_url)

    if figma_img and site_img:
        score, diff_img = compare_images(figma_img, site_img)
        print("Comparacao concluida.")
        # Se quiser salvar a diferença:
        diff_path = "diff_output.png"
        Image.fromarray(diff_img).save(diff_path)
        print(f"Imagem de diferença salva em {diff_path}")
