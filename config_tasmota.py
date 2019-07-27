import argparse
import subprocess


def execute_command(cmd, dir=""):
    if dir:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, cwd=dir, shell=True)
    else:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

user_config_file = "src-tasmota/sonoff/user_config_override.h"

parser = argparse.ArgumentParser(description="Generador de binarios para Sonoff")
parser.add_argument("ssid", type=str, help="SSID del AP WiFi")
parser.add_argument("password", type=str, help="Clave del AP WiFi")
args = parser.parse_args()

print("Se generara un binario para las siguientes credenciales:")
print("SSID: {}\nClave: {}".format(args.ssid, args.password))
cont = input("Confirmar (y/n)?: ")
if cont.strip() not in ['Y', 'y']:
    print("Credenciales no confirmadas. Saliendo...")
    exit(1)
print("Credenciales confirmadas. Continuando...")

wifi_credentials = {
    'ssid': args.ssid,
    'pass': args.password
}

user_config_override_content = """
#ifndef _USER_CONFIG_OVERRIDE_H_
#define _USER_CONFIG_OVERRIDE_H_

#warning **** user_config_override.h: Using Settings from this File ****

// -- Master parameter control --------------------
#undef  CFG_HOLDER
#define CFG_HOLDER        4617                    // [Reset 1] Change this value to load SECTION1 configuration parameters to flash

// -- Setup your own Wifi settings  ---------------
#undef  STA_SSID1
#define STA_SSID1         "{ssid}"             // [Ssid1] Wifi SSID
#undef  STA_PASS1
#define STA_PASS1         "{pass}"     // [Password1] Wifi password

// -- Set module template  ------------------------
#undef  MODULE
#define MODULE SONOFF_DUAL_R2

#endif
""".format(**wifi_credentials)

with open(user_config_file, 'w') as ucfile:
    ucfile.write(user_config_override_content)

print("Archivo de override escrito en {}. Continuando...".format(user_config_file))

# Configure environment
pconfig_file = "src-tasmota/platformio.ini"
with open(pconfig_file, 'r') as pfile:
    data = pfile.readlines()
data[14] = "env_default = sonoff\n"
with open(pconfig_file, 'w') as pfile:
    pfile.writelines(data)

# Configure original user config
muconfig_file = "src-tasmota/sonoff/my_user_config.h"
with open(muconfig_file, 'r') as mucfile:
    data_config = mucfile.readlines()
data_config[38] = "#define USE_CONFIG_OVERRIDE   // Uncomment to use user_config_override.h file. See README.md\n"
data_config[52] = "#define MODULE SONOFF_DUAL_R2  // [Module] Select default model from sonoff_template.h\n"
with open(muconfig_file, 'w') as mucfile:
    mucfile.writelines(data_config)

print("Sobreescrito archivo /{} y /{}. Procediendo a compilar. En caso de error, revisar build.log".format(pconfig_file, muconfig_file))

for path in execute_command("pio run 2>&1 | tee ../build.log", dir="src-tasmota"):
    print(path, end="")

subprocess.check_output("cp .pioenvs/sonoff/firmware.bin ../bin/sonoff.bin", cwd="src-tasmota/", shell=True)

print("Programa compilado y listo en bin/.")

upload_check = input("Desea subir firmware al Sonoff (y/n)?: ")
if upload_check.strip() not in ['Y', 'y']:
    print("Saliendo...")
    exit(2)

repeat_upload = True

while repeat_upload:
    print("Asegure de conectar el Sonoff Dual R2 en modo de programacion. Mas detalles en README.md.")
    print("A continuacion, se borrara la memoria flash del Sonoff que haya conectado.")
    input("Aprete ENTER al estar listo...")
    for path in execute_command("esptool.py erase_flash"):
        print(path, end="")
    print("Apague el Sonoff y vuelva a conectarlo en modo de programacion.")
    print("A continuacion, se escribira el firmware contenido en bin/. Asegurese que exista el archivo sonoff.bin en bin/.")
    input("Aprete ENTER para continuar...")
    for path in execute_command("esptool.py write_flash --flash_size 1MB --flash_mode dout 0x00000 bin/sonoff.bin"):
        print(path, end="")
    repeat_str = input("El Sonoff se encuentra flasheado. Desea flashear otro con las mismas credenciales WiFi (y/n)?")
    repeat_upload = repeat_str == 'Y' or repeat_str == 'y'
    