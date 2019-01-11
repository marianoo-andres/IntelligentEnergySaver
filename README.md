# IntelligentEnergySaver
Proyecto personal para ahorrar energía inteligentemente, apagando la pantalla de la computadora cuando no se detecta un rostro luego de cierto tiempo (requiere de una webcam)

Intelligent Energy Saver
Desarrollado por Decoding
http://decoding.com.ar/

Descripción
    Intelligent Energy Saver utiliza inteligencia artificial para reconocer caras utilizando
    la cámera web de la computadora.
    Ahorra energía apagando la pantalla cuando no se detecta una cara enfrente del monitor.

Configuración
    tiempo_apagado_en_minutos:
        cuantos minutos deben pasar sin detectar una cara hasta que se apague la pantalla
        (valor mínimo 1 minuto).

    modo_ahorro_energia:
        el escendido automático permite reactivar la pantalla cuando se detecta nuevamente una cara.
        "si": encendido automático desactivado (dejar este modo si se quiere maximizar el ahorro de energía).
        "no": encendido automático activado.

    modo_debug:
        Uso exclusivo para el desarrollador. Dejar el valor en "no"



