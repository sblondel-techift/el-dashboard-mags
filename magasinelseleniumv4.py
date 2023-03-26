from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Lecture du fichier CSV contenant les URLs
df_urls = pd.read_csv("url_mag.csv")

# Spécification du nombre d'URL à extraire
num_urls = 10  # modifier ce chiffre pour spécifier le nombre d'URL à extraire

# Création de la liste des URLs à extraire
urls = df_urls["URL"].tolist()[:num_urls]

# Fonction d'extraction de l'adresse à partir d'une URL
def extract_address(url):
    options = Options()
    options.headless = True
    service = Service('/path/to/chromedriver') # changer le chemin vers votre exécutable chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    try:
        # Recherche de la balise contenant l'adresse
        address_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'col-card-body-title')]/following-sibling::div[1]"))
        )
        # Extraction de l'adresse
        address = address_div.text.replace("<br>", "").replace("\t", " ").strip()
        return address
    except:
        # Si l'adresse ne peut pas être extraite, retourner None
        return None
    finally:
        driver.quit()

# Extraction des adresses pour chaque URL de la liste
data = []  # initialisation de la liste des données
count = 0  # initialisation du compteur d'URL traitées

for url in urls:
    address = extract_address(url)
    data.append({"URL": url, "Adresse": address})
    count += 1
    print(f"Adresse extraite pour {count} URL(s)")  # affichage de l'avancée de l'extraction

# Conversion de la liste des données en DataFrame et enregistrement dans un fichier CSV
df = pd.DataFrame(data)
df.to_csv("adresses_magasins.csv", index=False)
