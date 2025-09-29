# Práctica 1
Proyecto realizado para aprobar la Práctica Profesional 1.

## Resumen del Proyecto

CIMUBB ha solicitado un software de escritorio que permita analizar el tipo de objeto que pasa por una cinta transportadora y, en base al resultado, realizar movimientos automáticos con un brazo robot. Para ello se implementó un algoritmo de reconocimiento de patrones con OpenCV y comunicación serial para el brazo robot.

## Características principales

Algunas de las funcionalidades que incluye la plataforma:

* Interfaz para visualizar cámaras y enviar comandos al brazo robot.

* Análisis de imágenes con OpenCV.

* Envío de comandos por comunicación serial al brazo robot.


## Tecnologías

* Python
* PySimpleGUI
* Opencv
* PySerial

## Requisitos

Python >= 2.8

## Instalación

```bash
pip install opencv-python
pip install PySimpleGUI
pip install numpy
pip install pyserial
python Reconocimiento de Objetos.py
```
