FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN chmod +x postinstall.sh
RUN ./postinstall.sh
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
