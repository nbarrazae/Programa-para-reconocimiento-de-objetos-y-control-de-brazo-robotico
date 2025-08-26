import cv2
import PySimpleGUI as sg
import numpy as np
import serial
import time
import sys


def reconocimiento_pieza(video_capture3):
    texto = 'No se ha detectado pieza de madera'
    arrayHsv =  [15,  33,  15, 255, 140, 255, 0, 27058.0]
    arrayHsv2 = [99, 132, 105, 255, 170, 255, 0, 26158.0]
    maderaBajo = np.array([15 , arrayHsv[2], arrayHsv[4]], np.uint8)
    maderaAlto = np.array([35, arrayHsv[3], arrayHsv[5]], np.uint8)

    rojoBajo = np.array([0 , arrayHsv2[2], arrayHsv2[4]], np.uint8)
    rojoAlto = np.array([10 , arrayHsv2[3], arrayHsv2[5]], np.uint8)

    azulBajo = np.array([105 , arrayHsv2[2], arrayHsv2[4]], np.uint8)
    azulAlto = np.array([130 , arrayHsv[3], arrayHsv2[5]], np.uint8)

    verdeBajo = np.array([50 , arrayHsv2[2], arrayHsv2[4]], np.uint8)
    verdeAlto = np.array([95 , arrayHsv2[3], arrayHsv2[5]], np.uint8)   

    black_lower = np.array([0,0,0],np.uint8)
    black_upper = np.array([180,255,100],np.uint8)

    area = arrayHsv[7]
    count = 0
    while count <= 4:
        flag =False
        ret,frame = video_capture3.read()
        #frame = frame0[]
        if ret==True:
            frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            maskMadera = cv2.inRange(frameHSV,maderaBajo,maderaAlto)            
            maskRojo = cv2.inRange(frameHSV,rojoBajo,rojoAlto)            
            maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)            
            maskVerde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
            maskNegro = cv2.inRange(frameHSV,black_lower,black_upper)
            arrayMascaras = [maskRojo,maskAzul,maskVerde,maskNegro]#agregar maskNegro
            contornosMadera, hierarchy0 = cv2.findContours(maskMadera, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for mascaras in arrayMascaras:
                if flag == False:
                    contornosMascara, hierarchy = cv2.findContours(mascaras,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                    for c in contornosMascara:
                        areaContorno = cv2.contourArea(c)
                        #print(area)
                        epsilon = 0.02*cv2.arcLength(c,True)
                        approx = cv2.approxPolyDP(c,epsilon,True)
                        if areaContorno > 1000:
                            nuevoContorno = cv2.convexHull(c)
                            if len(approx)==4 and ( areaContorno > (area * 0.9) ):
                                cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 1)
                                flag = True
                                texto = 'Pieza Hembra'
                                x,y,w,h = cv2.boundingRect(c)
                                madera = frame[y:y+h,x:x+w]
                                #cv2.imshow('madera',madera)
                            elif areaContorno < (area * 0.9):
                                for c in contornosMadera:
                                    areaContorno = cv2.contourArea(c)
                                    #print(area)
                                    epsilon = 0.02*cv2.arcLength(c,True)
                                    approx = cv2.approxPolyDP(c,epsilon,True)
                                    if areaContorno > 1000:
                                        nuevoContorno = cv2.convexHull(c)
                                        if len(approx)==4 and ( areaContorno > (area * 0.9) ):
                                            #cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 1)
                                            texto = 'Pieza Macho'
                                            flag = True
                                            cv2.drawContours(frame, [nuevoContorno], 0, (0,0,0), 1)
                                            x,y,w,h = cv2.boundingRect(c)
                                            madera = frame[y:y+h,x:x+w]
                                            #cv2.imshow('madera',madera)
            if flag == False:
                for c in contornosMadera:
                    areaContorno = cv2.contourArea(c)
                    #print(area)
                    epsilon = 0.02*cv2.arcLength(c,True)
                    approx = cv2.approxPolyDP(c,epsilon,True)
                    if areaContorno > 1000:
                        nuevoContorno = cv2.convexHull(c)
                        if len(approx)==4 and ( areaContorno > (area * 0.9) ):
                            cv2.drawContours(frame, [nuevoContorno], 0, (0,0,0), 1)
                            flag = True
                            texto = 'Pieza Virgen'
                            x,y,w,h = cv2.boundingRect(c)
                            madera = frame[y:y+h,x:x+w]
                            #cv2.imshow('madera',madera)

        cv2.putText(frame,texto,(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255, 255, 255), 1)
        #cv2.imshow('frame',frame)
        count = count + 1
        if cv2.waitKey(1) & 0xFF == 27 or texto != 'No se ha detectado pieza de madera':
            #print(texto)
            count = 0
            madera = cv2.resize(madera, frameSize)
            break
        if count == 4:
            #print(texto)
            madera = 0
            count = 0
            break
    return texto,madera,flag

def movimiento_brazo(textEnviado):
    if len(textEnviado) >0:
        res = ''
        list_res = []
        flag_no_resq = False
        order = str.encode(textEnviado)
        robot.write(order+b'\r')
        while 'Done' not in res:
            res = str(robot.readline())
            if 'r*** E' in res :
                flag_no_resq = True
                break
            if (res not in list_res) and (len(res)>4) and ('\\r\\n' not in res):
                list_res.append(res)
        for indice,res in enumerate(list_res):
            if('Done.' in res):
                list_res[indice] = (f'>>{res[6:-2]}')
            else:
                list_res[indice] = (f'>>{res[2:-1]}')
        if flag_no_resq == True:
            list_res.append('Comando no encontrado')
            flag_error = True
            return list_res,flag_error
        else:
            flag_error = False
        return list_res,flag_error
    else:
        print("no hay nada escrito")
        

camera_Width  = 280 # 480 # 640 # 1024 # 1280
camera_Heigth = 180 # 320 # 480 # 780  # 960
frameSize = (camera_Width, camera_Heigth)

video_capture1 = cv2.VideoCapture(1)
video_capture2 = cv2.VideoCapture(2)
video_capture3 = cv2.VideoCapture(0)

flag_robot = 'DESCONECTADO'
flag_serial = True
flag_no_resq = False
flag_cam1 = False
flag_cam2 = False
flag_cam3 = False
flag_auto = False
count = 0

sg.theme("DarkBlue")
Enviado_array  = ['>>Enviado']
req_array   = ['>>Recibido']
columna1 = [    [sg.Text(text='ROBOT',font=("Arial", 20), pad=(0,10))],
                [sg.Button("Conectar Robot",key='conectarR', size=(15, 3), pad=(10, 0))],
                [sg.Listbox(values=(Enviado_array),key=('Enviado'), size=(25, 16))],
                [sg.InputText('',key=('EnviadoText'), size=(27, 5))],
                [sg.Text(text='', size=(20,1), pad=(0,0))],
                [sg.Text(text='', size=(20,1), pad=(0,0))], 
                [sg.Text(text='Tipo De Pieza', size=(20,1), pad=(0,0))],
                [sg.Text(text='No se ha iniciado el reconocimiento',key=('Pieza'), size=(20,2))],
                [sg.Text(text='  ', size=(20,1), pad=(0,35))],
                [sg.Text(text='  ', pad=(0,0), justification=('center')) ]]
colwebcam1 = sg.Column(columna1, element_justification='center')

columna2 = [    [sg.Text(text='  ',font=("Arial", 20), pad=(0,10))],
                [sg.Text(text='DESCONECTADO',key=('colorR'), size=(20,3),background_color=('red'),justification=('center'))],
                [sg.Listbox(values=(req_array),key=('Recibido'), size=(40, 16))],  
                [sg.Button("Enviar",key='enviarR', size=(10, 1), pad=(0,0)) , sg.Button("Automatico", key='auto', size=(10,1)) , sg.Text(text='',key=('colorAuto'), size=(5,1),background_color=('red'))    ],
                [sg.Image(filename="", key="cam3",size=(280,180),background_color='gray')],
                [sg.Text(text='   ', pad=(0,0), justification=('center')) ] ]  

colwebcam2 = sg.Column(columna2, element_justification='center')

columna3 = [    [sg.Text(text='CAMARAS',font=("Arial", 20), pad=(0,10))],
                [sg.Image(filename="", key="cam1",size=(280,180),background_color='gray')],
                [sg.Image(filename="", key="cam2",size=(280,180),background_color='gray')],
                [sg.Image(filename="", key="cam4",size=(280,180),background_color='gray',pad=(0,0))],
                [sg.Text(text='Desarrollado por Nicolás Baraza, 2022-2', pad=(0,0), justification=('center')) ]  ]         
colwebcam3 = sg.Column(columna3, element_justification='center')

columna4 = [    [sg.Text(text='  ',font=("Arial", 20), pad=(0,10))],
                [sg.Button("Camara 1",key='conectar1', size=(10, 1),    pad=(10, 0))],
                [sg.Button("Camara 2",key='conectar2', size=(10, 1),    pad=(10, 165),)],
                [sg.Button("Camara 3",key='conectar3', size=(10, 1),    pad=(10, 0))],
                [sg.Button("Reconocer",key='Reconocer3', size=(10, 1),  pad=(10, 10))],
                [sg.Button("Terminar",key=('terminar'),size=(15,1),pad=(0,38))],
                [sg.Text(text='  ', pad=(0,0), justification=('center')) ]   ]         
colwebcam4 = sg.Column(columna4)
colslayout = [colwebcam1,colwebcam2,colwebcam3, colwebcam4]
layout = [colslayout]

window    = sg.Window("Reconocimiento de Objetos", layout, 
                    no_titlebar=False, alpha_channel=1, grab_anywhere=False, 
                    return_keyboard_events=True, location=(200, 10))        

while True:
    start_time = time.time()
    event, values = window.read(timeout=20)
    if event == sg.WIN_CLOSED or event == 'terminar':
        break
    if event == 'conectarR':
        #conectar robot...
        if flag_robot == 'DESCONECTADO':
            try:
                robot = serial.Serial(port='COM1',baudrate=9600,timeout=0)
            except:
                textEnviado = 'No se pudo conectar la serial'
                req_array.append(f'>>{textEnviado}')
                window["Recibido"].update(req_array)
                window["EnviadoText"].update('')
                flag_serial = False
            if flag_serial == True:
                #order0 = str.encode('move 600')
                #robot.write(order0+b'\r')
                window["conectarR"].update('Desconectar Robot')
                window["colorR"].update('CONECTADO',background_color=("green"))
                flag_robot = 'CONECTADO'
        elif flag_robot == 'CONECTADO':
            window["conectarR"].update('Conectar Robot')
            window["colorR"].update('DESCONECTADO',background_color=("red"))
            flag_robot = 'DESCONECTADO' 
            robot.close()
    
    if event == 'enviarR':
        if flag_robot=='CONECTADO':
            textEnviado = values['EnviadoText']
            if len(textEnviado) > 0:
                list_res, flag_error = movimiento_brazo((textEnviado))
                Enviado_array.append(f'>>{textEnviado}')
                window["Enviado"].update(Enviado_array)
                window["EnviadoText"].update('')
                if flag_error == False:
                    req_array.extend(list_res)
                    window["Recibido"].update(req_array)
                else:
                    text_req = 'Comando no encontrado'
                    req_array.append(f'>>{text_req}')
                    window["Recibido"].update(req_array)
        elif flag_robot=='DESCONECTADO':
            textEnviado = 'El robot no esta conectado'
            req_array.append(f'>>{textEnviado}')
            window["Recibido"].update(req_array)
            window["EnviadoText"].update('')
    if event == 'auto':
        if flag_auto == False:
            if flag_robot=='CONECTADO':
                textEnviado = 'move 600'
                list_res, flag_error = movimiento_brazo((textEnviado))
                Enviado_array.append(f'>>{textEnviado}')
                window["Enviado"].update(Enviado_array)
                window["EnviadoText"].update('')
                if flag_error == False:
                    req_array.extend(list_res)
                    window["Recibido"].update(req_array)
                else:
                    text_req = 'Comando no encontrado'
                    req_array.append(f'>>{text_req}')
                    window["Recibido"].update(req_array)
                if flag_cam3==True:
                    if ret3 == True:
                        flag_auto = True
                        textEnviado = 'Modo automatico activado'
                        window['colorAuto'].update('',background_color=('green'))
                        req_array.append(f'>>{textEnviado}')
                        window["Recibido"].update(req_array)
                else:
                    window["conectar3"].update('Camara 3')
                    textEnviado = 'Error al conectar cam3'
                    req_array.append(f'>>{textEnviado}')
                    window["Recibido"].update(req_array)
                    window["EnviadoText"].update('')
            elif flag_robot=='DESCONECTADO':
                textEnviado = 'El robot no esta conectado'
                req_array.append(f'>>{textEnviado}')
                window["Recibido"].update(req_array)
                window["EnviadoText"].update('')
        else:
            flag_auto = False
            textEnviado = 'Modo automatico desactivado'
            window['colorAuto'].update('',background_color=('red'))
            req_array.append(f'>>{textEnviado}')
            window["Recibido"].update(req_array)

    if flag_auto: 
        texto , madera ,flag = reconocimiento_pieza(video_capture3)
        if flag != False:
            window["Pieza"].update(texto)
            imgbytes = cv2.imencode(".png", madera)[1].tobytes()
            window["cam4"].update(data=imgbytes)
        elif madera == False:
            window["Pieza"].update(texto)
            window["cam4"].update('',size=(280,180))


    if event == 'conectar1':
        if flag_cam1 == False:
            flag_cam1 = True
            window["conectar1"].update('Desconectar')
        elif flag_cam1 == True:
            flag_cam1 = False
            window["cam1"].update('',size=(280,180))
            window["conectar1"].update('Camara 1')

    if flag_cam1==True:
        ret1, frameOrig1 = video_capture1.read()
        if ret1 == True:
            frame1 = cv2.resize(frameOrig1, frameSize)
            imgbytes = cv2.imencode(".png", frame1)[1].tobytes()
            window["cam1"].update(data=imgbytes)
        else:
            window["conectar1"].update('Camara 1')
            textEnviado = 'Error al conectar camara 1'
            req_array.append(f'>>{textEnviado}')
            window["Recibido"].update(req_array)
            window["EnviadoText"].update('')
            flag_cam1=False
    
    if event == 'conectar2':
        if flag_cam2 == False:
            flag_cam2 = True
            window["conectar2"].update('Desconectar')
        elif flag_cam2 == True:
            flag_cam2 = False
            window["cam2"].update('',size=(280,180))
            window["conectar2"].update('Camara 2')
    # get camera frame
    if flag_cam2==True:
        ret2, frameOrig2 = video_capture2.read()
        if ret2 == True:
            frame2 = cv2.resize(frameOrig2, frameSize)
            imgbytes = cv2.imencode(".png", frame2)[1].tobytes()
            window["cam2"].update(data=imgbytes)
        else:
            window["conectar2"].update('Camara 2')
            textEnviado = 'Error al conectar camara 2'
            req_array.append(f'>>{textEnviado}')
            window["Recibido"].update(req_array)
            window["EnviadoText"].update('')
            flag_cam2=False

    if event == 'conectar3':
        if flag_cam3 == False:
            flag_cam3 = True
            window["conectar3"].update('Desconectar')
        elif flag_cam3 == True:
            flag_cam3 = False
            window["cam3"].update('',size=(280,180))
            window["cam4"].update('',size=(280,180))
            window["Pieza"].update('Camara Desconectada')
            window["conectar3"].update('Camara 3')
    # get camera frame
    if flag_cam3==True:
        ret3, frameOrig3 = video_capture3.read()
        if ret3 == True:
            frame3 = cv2.resize(frameOrig3, frameSize)
            imgbytes = cv2.imencode(".png", frame3)[1].tobytes()
            window["cam3"].update(data=imgbytes)
            if event == 'Reconocer3':
                texto , madera ,flag = reconocimiento_pieza(video_capture3)
                if flag != False:
                    window["Pieza"].update(texto)
                    imgbytes = cv2.imencode(".png", madera)[1].tobytes()
                    window["cam4"].update(data=imgbytes)
                elif madera == False:
                    window["Pieza"].update(texto)
                    window["cam4"].update('',size=(280,180))
        else:
            window["conectar3"].update('Camara 3')
            textEnviado = 'Error al conectar cam3'
            req_array.append(f'>>{textEnviado}')
            window["Recibido"].update(req_array)
            window["EnviadoText"].update('')
    

cv2.destroyAllWindows()