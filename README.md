## Criar ambiente
```
python3 -m venv venv'

## Criar arquivo requirments
pip freeze > requirements.txt

## Instalar Dependencias
pip3 install -r requirements.txt

## Entrando ambiente venv
source venv/bin/activate

# Utilizando Docker

## Build Image
docker build --tag api-cotacao .

## Run Docker
docker run -d --name api-cotacao -p 80:80 api-cotacao

```