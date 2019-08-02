# Sonoff-Zippedi

Este repositorio contiene software que permite configurar una red WiFi en el firmware Tasmota y luego programar un rele Sonoff Dual R2 con dicho firmware. Adicionalmente, se incluye una libreria que permite controlor el rele.

## Instrucciones

1. Ejecutar `. install_env.sh` o `source install_env.sh`.
2. Reinicar computador. Verificar que el usuario que vaya usar se encuentre en el grupo `dialout` mediante el comando `id`.
3. Activar ambiente virtual corriendo `. tasmota/bin/activate`. El terminal incluira un `(tasmota)` al comienzo de cada linea.
    1. Si es la primera vez que instala el ambiente virtual, debe instalar los requisitos mediante el comando `pip install -r requirements.txt`.
4. Ejecutar configurador mediante `python config_tasmota.py -s <SSID> -p <Clave>`. Si necesita ayuda, ejecute `python config_tasmota.py -h`.
5. El codigo `example.py` contiene un ejemplo de uso de la libreria `sonoff_control`. Si necesita mas ayuda, revise la documentacion presente en `sonoff_control/control.py`.
6. Si desea eliminar los directorios y ambientes creados, ejecutar `. clean.sh`

## `config_tasmota.py`

Este programa permite compilar una version del firmware Tasmota preconfigurada para la red WiFi que uno le indique. El codigo que compila se encuentra comprimado en `Sonoff-Tasmota.zip`. Mediante la opcion `--skip-compilation` o `-sc` es posible saltar la compilacion del firmware y saltar directamente a subirlo a un Sonoff. El codigo asume que el firmware se encuentra en `bin/sonoff.bin` (el directorio es creado junto a `install_env.sh`). Al finalizar la compilacion, se ofrece subir el codigo al Sonoff, lo cual se repite indefinidamente hasta que se le solicita parar al programa.

Para conectar el Sonoff, es necesario usar un adaptador FTDI-USB (o cualquier conversor RS-232 a USB valido) y un cable hembra-hembra o un jumper. Conectar el conversor serial al Sonoff. Para eso, no es necesario soldar conectores al Sonoff, pues basta con la conexion que se logra mediante jumpers macho. Si se energiza el Sonoff en este momento, pasara a parpadear el LED azul de poder. Para configurar el Sonoff, se debe usar el modo de programacion. Este modo se activa conectado GND con BUTTON 0 en los pines header macho. Luego de encender el Sonoff se puede desconectar. Es muy importante recordar remover el jumper luego de haber configurado el Sonoff, pues no permitira que el Sonoff se encienda sin entrar a modo de configuracion.

Finalmente, durante el proceso de subida de firmware, el programa pide reiniciar el Sonoff. Esto se puede lograr desconectador el conversial serial y luego conectandolo nuevamente, con tal que se apague bien el Sonoff. Esto se debe a que despues de cada operacion en el modo de programacion (lectura, grabado, borrado, etc.), el Sonoff queda en un modo indeterminado hasta que sea reiniciado. Si se intenta proceder sin reiniciarlo, no se podra subir el firmware generado y el programa no avanzara.