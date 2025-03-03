# Basis-Image
FROM python:3.9-slim

# Systempakete installieren: ffmpeg, nginx, supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    nginx \
    supervisor

# Arbeitsverzeichnis setzen
WORKDIR /app

# Kopiere nur die notwendigen Dateien direkt nach /app
COPY whisper-api/main.py ./           
COPY whisper-api/requirements.txt ./  
COPY nginx/ ./nginx/
COPY deploy/preload-models.py ./deploy/
COPY deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Python-Abhängigkeiten für die Whisper-API installieren
RUN pip install --no-cache-dir -r requirements.txt

# Whisper-Modelle vorladen
RUN python deploy/preload-models.py

# Nginx-Konfiguration und Dateien kopieren (überschreibt die Default-Konfiguration)
COPY nginx/single-container.conf /etc/nginx/conf.d/default.conf
COPY nginx/public/ /usr/share/nginx/html/

# Unnötige Dateien entfernen, um das Image zu verschlanken
RUN rm -rf /app/deploy/preload-models.py \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Ports freigeben: 8076 (API) und 8077 (Nginx) 
EXPOSE 8076 8077

# Startbefehl: Supervisord übernimmt den Start und die Überwachung beider Prozesse
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]