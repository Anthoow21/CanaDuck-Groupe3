# Utilise une image Python comme base
FROM python:3.11-slim

# Crée un répertoire dans le conteneur
WORKDIR /app

# Copie le contenu de ton projet
COPY . .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Lance l'application Flask
CMD ["python", "app.py"]
