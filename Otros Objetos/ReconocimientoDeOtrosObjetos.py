import cv2
import PySimpleGUI as sg
import numpy as np
import sys
import time

def reconocimiento(video_capture):
	arrayRojo = [0, 18, 60, 255, 115, 255, 0, 10340.5]
	rojoBajo = np.array([0 , arrayRojo[2], arrayRojo[4]], np.uint8)
	rojoAlto = np.array([18 , arrayRojo[3], arrayRojo[5]], np.uint8)
	areaRojo = arrayRojo[7]

	arrayVerde = [42, 84, 70, 255, 165, 255, 0, 11990.0]
	verdeBajo = np.array([arrayVerde[0] , arrayVerde[2], arrayVerde[4]], np.uint8)
	verdeAlto = np.array([arrayVerde[1] , arrayVerde[3], arrayVerde[5]], np.uint8)
	areaVerde = arrayRojo[7]

	arrayAmarillo = [15, 36, 130, 255, 235, 255, 0, 135.5]
	amarilloBajo = np.array([arrayAmarillo[0] , arrayAmarillo[2], arrayAmarillo[4]], np.uint8)
	amarilloAlto = np.array([arrayAmarillo[1] , arrayAmarillo[3], arrayAmarillo[5]], np.uint8)
	areaAmarillo = arrayAmarillo[7]

	arrayRosa = [164, 179, 5, 255, 235, 255, 0, 5761.0]
	rosaBajo = np.array([arrayRosa[0] , arrayRosa[2], arrayRosa[4]], np.uint8)
	rosaAlto = np.array([arrayRosa[1] , arrayRosa[3], arrayRosa[5]], np.uint8)
	areaRosa = arrayRosa[7]

	arrayDorado = [18, 36, 75, 255, 120, 255, 0, 208.0]
	doradoBajo = np.array([arrayDorado[0] , arrayDorado[2], arrayDorado[4]], np.uint8)
	doradoAlto = np.array([arrayDorado[1] , arrayDorado[3], arrayDorado[5]], np.uint8)
	areaDorado = arrayRosa[7]

	arrayPVC = [90, 117, 80, 255, 135, 255, 0, 2830.0]
	PVCBajo = np.array([arrayPVC[0] , arrayPVC[2], arrayPVC[4]], np.uint8)
	PVCAlto = np.array([arrayPVC[1] , arrayPVC[3], arrayPVC[5]], np.uint8)
	areaPVC = arrayPVC[7]

	arrayMadera = [12, 24, 10, 255, 185, 255, 0, 3686.5]
	maderaBajo = np.array([arrayMadera[0] , arrayMadera[2], arrayMadera[4]], np.uint8)
	maderaAlto = np.array([arrayMadera[1] , arrayMadera[3], arrayMadera[5]], np.uint8)
	areaMadera = arrayMadera[7]

	arrayHsv = [0, 0, 0, 0, 0, 0, 0, 0.0]
	#arrayHsv = resaltadoDeColores()
	HsvBajo = np.array([arrayHsv[0] , arrayHsv[2], arrayHsv[4]], np.uint8)
	HsvAlto = np.array([arrayHsv[1] , arrayHsv[3], arrayHsv[5]], np.uint8)
	count0 = 0
	while count0 < 4:
		flag =False
		texto = 'No se ha detectado nada'
		ret,frame = video_capture.read()
		if ret==True:
			frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
			maskRojo = cv2.inRange(frameHSV,rojoBajo,rojoAlto)
			maskVerde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
			maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
			maskRosa = cv2.inRange(frameHSV,rosaBajo,rosaAlto)
			maskDorado = cv2.inRange(frameHSV,doradoBajo,doradoAlto)
			maskHsv     = cv2.inRange(frameHSV,HsvBajo,HsvAlto)
			maskPVC     = cv2.inRange(frameHSV,PVCBajo,PVCAlto)
			maskMadera  = cv2.inRange(frameHSV,maderaBajo,maderaAlto)

			contornosRojo, hierarchy1 = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			contornosVerde, hierarchy2 = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			contornosAmarillo, hierarchy3 = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			contornosRosa, hierarchy3 = cv2.findContours(maskRosa, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			contornosDorado, hierarchy1 = cv2.findContours(maskDorado, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			contornosHsv, hierarchy5 = cv2.findContours(maskHsv, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			contornosPVC, hierarchy5 = cv2.findContours(maskPVC, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			contornosMadera, hierarchy5 = cv2.findContours(maskMadera, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

			if flag == False:
				contornoList = []
				count = 0
				count2 = 0
				for c in contornosPVC:
					areaContorno = cv2.contourArea(c)
					epsilon = 0.02*cv2.arcLength(c,True)
					approx = cv2.approxPolyDP(c,epsilon,True)
					if areaContorno > 10000  and areaContorno < 26000:
						nuevoContorno = cv2.convexHull(c)
						contornoList.append(nuevoContorno)
						count = count + 1
						if count == 2:
							contornoList1 = []
							count1 = 0
							for c in contornosMadera:
								areaContorno1 = cv2.contourArea(c)
								epsilon1 = 0.02*cv2.arcLength(c,True)
								approx1 = cv2.approxPolyDP(c,epsilon,True)
								if areaContorno1 > 5000 and areaContorno1 < 20000:
									nuevoContorno1 = cv2.convexHull(c)
									contornoList1.append(nuevoContorno1)
									count1 = count1 + 1
									if count1 == 2:
										cv2.drawContours(frame, [contornoList1[0]], 0, (255,0,0), 1)
										cv2.drawContours(frame, [contornoList1[1]], 0, (255,0,0), 1)
										cv2.drawContours(frame, [contornoList[0]], 0, (255,0,0), 1)
										cv2.drawContours(frame, [contornoList[1]], 0, (255,0,0), 1)
										texto = 'PVC'
										flag = True

			if flag == False:
				for c in contornosRosa:
					areaContorno = cv2.contourArea(c)
					epsilon = 0.01*cv2.arcLength(c,True)
					approx = cv2.approxPolyDP(c,epsilon,True)
					if areaContorno > 5000 and len(approx) > 10:
						nuevoContorno = cv2.convexHull(c)
						cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 1)
						texto = 'Timbre Rosa'
						flag = True
						return texto

			if flag == False:
				for c in contornosVerde:
					areaContorno = cv2.contourArea(c)
					epsilon = 0.01*cv2.arcLength(c,True)
					approx = cv2.approxPolyDP(c,epsilon,True)
					if areaContorno > 10000:
						nuevoContorno = cv2.convexHull(c)
						cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 1)
						for c in contornosAmarillo:
							areaContorno = cv2.contourArea(c)
							epsilon = 0.01*cv2.arcLength(c,True)
							approx = cv2.approxPolyDP(c,epsilon,True)
							if areaContorno > 500:
								nuevoContorno = cv2.convexHull(c)
								cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 1)
								texto = 'Corchetes Torre'
								flag = True
								return texto
			count = 0
			if flag == False:
				for c in contornosDorado:
					areaContorno = cv2.contourArea(c)
					epsilon = 0.01*cv2.arcLength(c,True)
					approx = cv2.approxPolyDP(c,epsilon,True)
					if areaContorno > 100 and areaContorno > 500:
						count = count + 1
						if count == 4:
							nuevoContorno = cv2.convexHull(c)
							cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 1)
							texto = 'E-valve'
							return texto
							flag = True

			if flag == False:
				for c in contornosRojo:
					areaContorno = cv2.contourArea(c)
					epsilon = 0.01*cv2.arcLength(c,True)
					approx = cv2.approxPolyDP(c,epsilon,True)
					if areaContorno > 10500 and len(approx) >= 4:
						nuevoContorno = cv2.convexHull(c)
						cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 1)
						texto = 'Stic-Fix Pritt'
						return texto
						flag = True
			count0 = count0 + 1
			if texto != 'No se ha detectado nada':
				return texto
	return texto



video_capture = cv2.VideoCapture(0)
camera_Width  = 480 #280 # 480 # 640 # 1024 # 1280
camera_Heigth = 320 #180 # 320 # 480 # 780  # 960
frameSize = (camera_Width, camera_Heigth)

sg.theme("DarkBlue")
columna1 = [ 	[sg.Image(filename="", key="cam1",size=(280,180))],
[sg.Button("Reconocer",key='Reconocer', size=(10, 1), pad=(0, 0)),sg.Text(text=('Esperando...'),key="detectado")]	]         
colwebcam1 = sg.Column(columna1, element_justification='center')      
colslayout = [colwebcam1]
layout = [colslayout]
window    = sg.Window("Reconocimiento de Objetos", layout, 
	no_titlebar=False, alpha_channel=1, grab_anywhere=False, 
	return_keyboard_events=True, location=(200, 10))     
while True:
	start_time = time.time()
	event, values = window.read(timeout=20)
	if event == sg.WIN_CLOSED:
		break
	ret0, frame0 = video_capture.read()
	if ret0 == True:
		frame0 = cv2.resize(frame0, frameSize)
		imgbytes = cv2.imencode(".png", frame0)[1].tobytes()
		window["cam1"].update(data=imgbytes)
		if event == 'Reconocer':
			texto = reconocimiento(video_capture)
			window['detectado'].update(texto)



