# Practica 1
Proyecto realizado para aprobar la Practica Profesional 1.

## Resumen del Proyecto

CIMUBB ha solicitado un software de escritorio que permita analizar el tipo de objeto que pasa por una cinta transportadora y, en base al resultado, realizar movimientos automáticos con un brazo robot. Para ello se implementó un algoritmo de reconocimiento de patrones con OpenCV y comunicación serial para el brazo robot.

## Características principales

Algunas de las funcionalidades que incluye la plataforma:

* Interfaz para visualizar cámaras y enviar comandos al brazo robot.

* Análisis de imágenes con OpenCV.

* Envío de comandos por comunicación serial al brazo robot.


## Tecnologías

* Python
* Tkinter
* Opencv
* PySerial

## Requisitos

Python >= 2.8

## Installation

```bash
git clone https://github.com/nbarrazae/Conecta2UBB.git
cd Conecta2UBB
cd backend
python3 -m venv venv
source venv/bin/activate    # o venv\Scripts\activate en Windows
pip install -r requirements.txt
python manage.py migrate   # modificar .env
cd ../frontend
npm install   # o yarn install
npm run dev   # o npm start, preview
```
