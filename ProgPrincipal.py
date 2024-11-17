# Programa de sistemas de reserva de Vuelos
import time
import random 
import os
import json
import re
from datetime import datetime, timedelta

# Funciones 
def menuInicial():
    """Funcion que permite seleccionar una opcion de accion de sesion de usuario."""
    ok = True
    while ok:
        print("*****************************************")
        print("*           Sistema de Vuelos           *")
        print("*****************************************")
        print("*                                       *")
        print("*        1. Registro de Usuarios        *")
        print("*        2. Iniciar Sesion              *")
        print("*        3. Salir                       *")
        print("*                                       *")
        print("*****************************************")
        
        try:
            opcion = int(input("Seleccionar una opción: "))
            if opcion >= 1 and opcion < 4:
                ok = False
                return opcion
            else:
                print("Por favor, elige una opción válida (1-3).")
        except ValueError:
            print("Error: Debes ingresar un número.")

    return -1

def menuVuelos():
    """Funcion que permite seleccionar una opcion de accion relacionada a los vuelos segun el usuario ingresado."""
    ok=True
    while ok:
        print("***************************************************")
        print("*       Menú Principal de Selección Vuelos        *")
        print("***************************************************")
        print("*                                                 *")
        print("*          1. Búsqueda de Vuelos                  *")
        print("*          2. Reserva de Vuelos                   *")
        print("*          3. Historial de Vuelos                 *")
        print("*          4. Cancelar Reservas                   *")
        print("*          5. Cerrar Sesión                       *")
        print("*                                                 *")
        print("***************************************************")

        try:
            opcion = int(input("\nSeleccionar una opción: "))
            
            if opcion >= 1 and opcion < 6:
                ok = False
                return opcion
            else:
                print("Por favor, elige una opción válida (1-5)")
        except ValueError:
            print("Error: Debes ingresar un número.")

    return -1



# Funciones
def generar_fecha_hora():
    """Genera una fecha y hora aleatoria dentro de los próximos 30 días."""
    # Obtener la fecha actual
    fecha_actual = datetime.now()
    # Generar un número aleatorio de días y horas
    dias_adelante = random.randint(1, 30)
    horas = random.randint(0, 23)
    minutos = random.randint(0, 59)
    
    # Calcular la fecha y hora programada
    fecha_programada = fecha_actual + timedelta(days=dias_adelante, hours=horas, minutes=minutos)
    return fecha_programada.strftime("%Y-%m-%d"), fecha_programada.strftime("%H:%M")


def generarVuelos(matriz):
    """Genera una cantidad establecida de vuelos entre países de Sudamérica y América del Norte o combinación de ambas."""
    vuelosJson = []
    vuelos = []
    estados = ["A tiempo"] * 7 + ["Retrasado"] * 2 + ["Cancelado"]
    
    for i in range(len(matriz)):
        random.shuffle(matriz)
        for j in range(i + 1, len(matriz)):
            # Se limita a 50 vuelos para realizar prueba
            if len(vuelos) < 50:
                random.shuffle(matriz)
                origen_pais, origen_capital = matriz[i]
                destino_pais, destino_capital = matriz[j]
                fecha, hora = generar_fecha_hora()
                estado_vuelo = random.choice(estados)
                vuelos.append((origen_pais, origen_capital, destino_pais, destino_capital, fecha, hora, estado_vuelo))

                vuelosJson.append({
                    "origen_pais": origen_pais,
                    "origen_capital": origen_capital,
                    "destino_pais": destino_pais,
                    "destino_capital": destino_capital,
                    "fecha": fecha,
                    "hora": hora,
                    "estado_vuelo": estado_vuelo
                })

    guardarVuelosEnJson(vuelosJson,'vuelos.json')
    
    return vuelos



def guardarVuelosEnJson(vuelos, nombre_archivo):
    """Guarda la lista de vuelos en un archivo JSON dentro de la carpeta 'vuelos'."""
    os.makedirs('BDvuelos', exist_ok=True)
    
    # Ruta completa del archivo apuntando a la carpeta BDvuelos/vuelos.json
    ruta_archivo = os.path.join('BDvuelos', nombre_archivo)
    
    # se utiliza [encoding='utf-8'] y [ensure_ascii=False] para evitar que los caracteres especiales sean codificados en el archivo
    with open(ruta_archivo, 'wt', encoding='utf-8') as archivo_json:
        json.dump(vuelos, archivo_json, indent=4, ensure_ascii=False) 


def imprimirMatrizOrdenada(matriz):
    """Funcion que permite la prueba rápida de matriz y datos"""
    ancho_pais = 20
    ancho_capital = 20
    
    print("\n")
    print('-' * 130)
    print("\t    Ubicación de Origen\t\t\t    Ubicación de Llegada\t\t          Fecha\t\tHora")
    print('-' * 130)
    
    imprimir_vuelo = lambda vuelo: print(f"{vuelo[0]:<{ancho_pais}},{vuelo[1]:<{ancho_capital}}-->   {vuelo[2]:<{ancho_pais}},{vuelo[3]:<{ancho_capital}}\t{vuelo[4]}\t{vuelo[5]}")

    list(map(imprimir_vuelo, matriz))
    
    print('-' * (ancho_pais + ancho_capital + ancho_pais + ancho_capital + 50))


#Usuario
def registrarUsuario(diccionario_usuarios): 
    """Funcion que permite a nuevos usuarios crear una cuenta en el sistema de reservas. Recibe la lista de usuarios existente"""
    os.system('cls' if os.name == 'nt' else 'clear')
    nombre_apellido=input("Ingrese su nombre y apellido: \n")
    os.system('cls' if os.name == 'nt' else 'clear')
    nuevo_usuario = int(input("Ingrese un pin de 4 dígitos que lo identificará como nuevo usuario: \n"))
    
    bandera = True

    while bandera:
        if nuevo_usuario < 1000 or nuevo_usuario > 9999 or nuevo_usuario in diccionario_usuarios:
            print("Número de usuario inválido o ya existente\n")
            nuevo_usuario = int(input("Ingrese un pin de 4 dígitos que lo identificará como nuevo usuario: \n"))
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            bandera = False

    while True:
        nueva_contraseña = input("Ingrese una contraseña de al menos 8 caracteres con al menos un número, una letra minúscula y una letra mayúscula: \n")
        
        # Expresión regular para validar la contraseña
        patron = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$')
        
        if patron.match(nueva_contraseña):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Usuario registrado con éxito\n")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')

            break
        else:
            print("Contraseña inválida. Debe tener al menos:\n")
            print(". 8 caracteres\n. 1 letra mayúscula\n. 1 letra minúscula\n. 1 número")

    diccionario_usuarios[nuevo_usuario] = {
                                            'nombre_apellido': nombre_apellido,
                                            'contrasena': nueva_contraseña
                                            }

    print(diccionario_usuarios)



def iniciarSesion(diccionario_usuarios, intentos): 
    """Funcion que permite a los usuarios existentes iniciar sesión en el sistema para acceder a sus reservas y realizar nuevas transacciones."""
    usuario_actual = 0
    iniciarSesion = int(input("Ingrese su número de usuario: \n"))
    bandera = True

    while bandera:
        if iniciarSesion not in diccionario_usuarios:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Usuario no existente\n")
            intentos += 1
            
            iniciarSesion = int(input("Ingrese su número de usuario: \n"))
            if intentos == 4:
                intentos = 1
                print("Demasiados intentos fallidos.")
                bandera = False
        else:
            # Solicitar la contraseña
            contrasena = input("\nIngrese su contraseña: \n")
            if diccionario_usuarios[iniciarSesion] ["contrasena"] == contrasena:
                os.system('cls' if os.name == 'nt' else 'clear')    
                print("Login exitoso")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear') 
                intentos = 0
                usuario_actual = iniciarSesion
                bandera = False
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                # el abs unicamente me da el numero absuloto de intentos, el cual debe ser siempre positivo
                print(f"Contraseña incorrecta. Tiene {abs(intentos-3)} intentos para poder logearse. \n")
                intentos += 1

                if intentos == 4:
                    intentos = 1
                    bandera = False

    return intentos, usuario_actual


def sacar_tildes(texto):
    """Funcion que se encarga de reemplazar la variable q entra por la palabra sin tilde"""
    tildes = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N'
    }
    for acento, sin_acento in tildes.items():
        texto = texto.replace(acento, sin_acento)

    return texto


def mostrar_filtro_vuelos(vuelos):
    pais_origen, pais_llegada = obtener_paises()
    os.system('cls' if os.name == 'nt' else 'clear')
    # Buscar vuelos
    resultados = buscar_vuelos(vuelos, pais_origen, pais_llegada)

    print(f"\nVuelos encontrados para ir desde {pais_origen} hasta {pais_llegada}")
    if resultados:
        for index, vuelo in resultados:
            # Imprimir índice seguido de los detalles del vuelo
            print(f"{index}) {vuelo[0]} --> {vuelo[2]} - {vuelo[3]} == {vuelo[4]}\t{vuelo[5]}")
            print('-' * 130)
        print("\n\n")
    else:
        print("No se encontraron vuelos que coincidan.")



def buscar_vuelos(vuelos, pais_origen, pais_llegada):
    # Filtrar la matriz según el país de origen y país de llegada
    resultados = []
    
    pais_origen_sin_tildes = sacar_tildes(pais_origen)
    pais_llegada_sin_tildes = sacar_tildes(pais_llegada)

    # Se usa filter para seleccionar vuelos con el origen y destino deseado
    vuelos_filtrados = filter(
        lambda vuelo: sacar_tildes(vuelo[0]) == pais_origen_sin_tildes and sacar_tildes(vuelo[2]) == pais_llegada_sin_tildes,
        vuelos
    )

    resultados = [(index + 1, vuelo) for index, vuelo in enumerate(vuelos_filtrados)]

    return resultados


def obtener_paises():
    pais_origen = input("Ingrese el país de origen: ").title()
    pais_llegada = input("Ingrese el país de llegada: ").title()
    return pais_origen, pais_llegada


def cancelarReserva(reservas, usuario_actual):
    """Función que permite al usuario cancelar una reserva existente, gestionando el reembolso o cambios según las políticas del sistema. Recibe lista de usuarios y lista de reservas existentes."""
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\nReservas del usuario:")
    reservas_usuario = list(filter(lambda reserva: reserva[0] == usuario_actual, reservas))

    if not reservas_usuario:
        print("No tiene reservas para cancelar.\n")
        return

    for i, reserva in enumerate(reservas_usuario):
        vuelo = reserva[1]
        print(f"{i + 1}. Origen: {vuelo[0]}, {vuelo[1]} -> Destino: {vuelo[2]}, {vuelo[3]} == {vuelo[4]}\t{vuelo[5]}")

    # Función lambda para validar la selección de reserva
    validar_seleccion = lambda seleccion: 1 <= seleccion <= len(reservas_usuario)

    seleccion = int(input("\nSeleccione el número de la reserva que desea cancelar: \n"))
    while not validar_seleccion(seleccion):
        print("Selección de reserva inválida\n")
        seleccion = int(input("Seleccione el número de la reserva que desea cancelar: \n"))

    reserva_seleccionada = reservas_usuario[seleccion - 1]
    reservas.remove(reserva_seleccionada)

    print(f"\nReserva cancelada con éxito. Vuelo cancelado: Origen: {reserva_seleccionada[1][0]}, {reserva_seleccionada[1][1]} -> Destino: {reserva_seleccionada[1][2]}, {reserva_seleccionada[1][3]} == {reserva_seleccionada[1][4]}\t{reserva_seleccionada[1][5]}\n")


# Consultas Vuelos
def consultarStatusDeVuelo(vuelo_seleccionado):
    """Consulta y muestra el estado actual del vuelo seleccionado, proporcionando razones aleatorias si está cancelado."""

    origen_pais, origen_capital, destino_pais, destino_capital, fecha, hora, estado_vuelo = vuelo_seleccionado
    razones_cancelacion = ["Tormenta", "Vientos fuertes", "Problemas técnicos", "Falta de personal"]
    
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"Estado del vuelo seleccionado: Origen: {origen_pais}, {origen_capital} -> Destino: {destino_pais}, {destino_capital}")
    print(f"Fecha: {fecha} Hora: {hora}")
    
    if estado_vuelo == "Retrasado":
        razon = random.choice(razones_cancelacion)
        print(f"Estado actual del vuelo: {estado_vuelo}. Razón: {razon}.\n")
    elif estado_vuelo == "Cancelado":
        razon = random.choice(razones_cancelacion)
        print(f"Estado actual del vuelo: {estado_vuelo}. Razón: {razon}.\n")
    else:
        print(f"Estado actual del vuelo: {estado_vuelo}\n")
    
    return estado_vuelo


def pagarReserva():
    """Esta funcion gestiona el proceso de pago para completar una reserva, incluyendo la elección del método de pago y la confirmación de la transacción."""
    # Creo diccionario que contenga las opciones de pago
    metodos_pago = {
        1: "Tarjeta de crédito",
        2: "Tarjeta de débito",
        3: "QR Mercado Pago"
    }
    print("\nProceso de pago iniciado.")
    print("Opciones de método de pago:")
    for clave, valor in metodos_pago.items():
        print(f"{clave}. {valor}")
    
    metodo_pago = int(input("\nSelecciona un método de pago: "))

    if metodo_pago in metodos_pago:
        print(f"Método de pago seleccionado: {metodos_pago[metodo_pago]}.")
    else:
        print("Método de pago inválido. Intenta de nuevo.")
        #Vuelvo a la funcion cuando el usuario ponga cualquier otro metodo de pago no existente
        return pagarReserva()

    #Utilizacion de procesamiento de pago aleatoreo
    print("Espere un momento, su pago se esta procesando...")
    transaccion_exitosa = random.choice([True, False, True, True])
    
    if transaccion_exitosa:
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear') 
        print("\nPago completado con éxito.")
        return True
    else:
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear') 
        print("\nError en la transacción. Vuelve a intentarlo.")
        return False


def historialReservas(reservas, usuario_actual):
    # """Esta funcion muestra un historial de reservas realizadas por el usuario, incluyendo reservas anteriores y pagos.(antiguas y actuales) Recibe reservas actuales"""
    # os.system('cls' if os.name=='nt' else 'clear')
    # bandera = True

    # print("\nHistorial de reservas del usuario:")
    # reservas_usuario = list(filter(lambda reserva: reserva[0] == usuario_actual, reservas))

    # if not reservas_usuario:
    #     print("No tiene reservas registradas.\n")
    #     return

    # for i, reserva in enumerate(reservas_usuario):
    #     vuelo = reserva[1]
    #     print('-' * 80)
    #     print(f"{i+1}. | Origen: {vuelo[0]}, {vuelo[1]} -> Destino: {vuelo[2]}, {vuelo[3]}  == {vuelo[4]}\t{vuelo[5]}")
    # print('-' * 80) 

    """Esta función muestra un historial de reservas realizadas por el usuario, incluyendo reservas anteriores y pagos.(antiguas y actuales) Recibe reservas actuales."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\nHistorial de reservas del usuario:")
    reservas_usuario = list(filter(lambda reserva: reserva[0] == usuario_actual, reservas))

    if not reservas_usuario:
        print("No tiene reservas registradas.\n")
        return

    # Verificar si la carpeta 'historiales' existe, si no, crearla
    carpeta_historiales = "historiales"
    if not os.path.exists(carpeta_historiales):
        os.makedirs(carpeta_historiales)

    # Crear o sobrescribir el archivo del historial en la carpeta
    nombre_archivo = os.path.join(carpeta_historiales, f"historial_reservas_{usuario_actual}.txt")
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(f"Historial de reservas del usuario: {usuario_actual}\n")
        archivo.write('-' * 80 + '\n')

        for i, reserva in enumerate(reservas_usuario):
            vuelo = reserva[1]
            linea = f"{i+1}. | Origen: {vuelo[0]}, {vuelo[1]} -> Destino: {vuelo[2]}, {vuelo[3]}  == {vuelo[4]}\t{vuelo[5]}"
            print('-' * 80)
            print(linea)
            archivo.write(linea + '\n')
            archivo.write('-' * 80 + '\n')

    print(f"\nEl historial se ha guardado en el archivo: {nombre_archivo}")


def hacerReservaDeVuelos(vuelos, reservas, usuario_actual):
    """Esta funcion Facilita la reserva de un vuelo seleccionado, solicitando la información del usuario y confirmando la reserva. Recibe la matriz de Vuelos, la lista de usuarios existentes y las reservas actuales"""
    os.system('cls' if os.name=='nt' else 'clear')

    bandera = True
    ancho_pais = 20
    ancho_capital = 20
    
    print("\nLista de vuelos disponibles:\n")
    print('-'*130)
    for i,vuelo in enumerate(vuelos):
        origen_pais, origen_capital, destino_pais, destino_capital, fecha, hora, estado = vuelo
        print(f"{i+1}. | {origen_pais:<{ancho_pais}},{origen_capital:<{ancho_capital}}-->   {destino_pais:<{ancho_pais}},{destino_capital:<{ancho_capital}}\t{fecha}\t{hora}")
        print('-' * (ancho_pais + ancho_capital + ancho_pais + ancho_capital + 50))

    seleccion = int(input("\nSeleccione el número del vuelo que desea reservar: \n"))
    bandera = True

    while bandera:
        if seleccion < 1 or seleccion > len(vuelos):
            print("Selección de vuelo inválida\n")
            seleccion = int(input("Seleccione el número del vuelo que desea reservar: \n"))
        else:
            vuelo_seleccionado = vuelos[seleccion-1]
            bandera = False


    cantidad_pasajes=int(input("Ingrese la cantidad de pasajes que desee reservar, siendo 8 el máximo permitido: \n"))

    while bandera:
        if cantidad_pasajes<1 or cantidad_pasajes>8:
            print("Selección inválida\n")
            cantidad_pasajes=int(input("Ingrese la cantidad de pasajes que desee reservar, siendo 8 el máximo permitido: \n"))
        else:
            bandera = False
            

    estado = consultarStatusDeVuelo(vuelo_seleccionado)

    if estado == "Cancelado":
        print("No puedes reservar este vuelo porque está cancelado. Selecciona otro vuelo.\n")
        return

    if pagarReserva():
        os.system('cls' if os.name=='nt' else 'clear')
        reservas.append((usuario_actual, vuelo_seleccionado))
        print("\nReserva realizada con ÉXITO\n")
        print(f"Vuelo reservado: Origen: {vuelo_seleccionado[0]}, {vuelo_seleccionado[1]} -> Destino: {vuelo_seleccionado[2]}, {vuelo_seleccionado[3]}  ==  {vuelo_seleccionado[4]}\t{vuelo_seleccionado[5]}\n")
        imprimirTicket(usuario_actual, vuelo_seleccionado)
    else:
        print("ERROR. La reserva no se pudo completar debido a un problema con el pago.")


def imprimirTicket(usuario_actual, vuelo):
    origen_pais, origen_capital, destino_pais, destino_capital, fecha, hora, estado = vuelo
    
    numero_vuelo=random.randint(1000,9999)
    numero_asiento=str(random.randint(1,20)).zfill(2)+random.choice(['A', 'B', 'C', 'D', 'E', 'F'])

    ticket = f"""
    ****************************************************************************************
                                           BOARDING PASS                                                                          
    ****************************************************************************************
    
        N° Usuario: {usuario_actual}                    Fecha: {fecha}
    
    Desde/From: {origen_pais}, {origen_capital}         Vuelo n°/Flight nr:{numero_vuelo}
    A/To: {destino_pais}, {destino_capital}             Asiento/Seat: {numero_asiento}
    
        Puerta/Gate: E01                                Hora: {hora}

    ****************************************************************************************
                                  ¡Gracias por viajar con nosotros!
    ****************************************************************************************
    """
    
    os.system('cls' if os.name=='nt' else 'clear')
    time.sleep(1)
    print(ticket)
    time.sleep(3)
    os.system('cls' if os.name=='nt' else 'clear')


def main():
    reservas = []
    diccionario_usuarios = {0000:
                            {"nombre y apellido":"Administrador",
                            "contrasena":"admin"}
                            }

    salir = True
    salir2 = True

    vuelos = generarVuelos(matrizPaisesCapitales)
    while salir:
        seleccion = menuInicial()

        if seleccion == 1:
            registrarUsuario(diccionario_usuarios)

        elif seleccion == 2:
            intentos=0
            os.system('cls' if os.name == 'nt' else 'clear')
            intentos, usuario_actual = iniciarSesion(diccionario_usuarios, intentos)

            # Pruba de usuarios activos diccionarios
            print("Prueba Diccionario Usuarios existentes: ",diccionario_usuarios)


            salir2 = True

            while salir2:
                
                if intentos==1:
                    intentos=0
                    seleccion=5
                else:
                    seleccion = menuVuelos()

                if seleccion == 1:
                    # Buscar vuelos               
                    imprimirMatrizOrdenada(vuelos)
                    # Seleccionar segun pais de origen y llegada
                    mostrar_filtro_vuelos(vuelos)
                elif seleccion == 2:
                    # Hacer reserva y pagar
                    hacerReservaDeVuelos(vuelos, reservas, usuario_actual)
                elif seleccion == 3:
                    # Historial de reservas
                    historialReservas(reservas, usuario_actual)  
                elif seleccion == 4:
                    # Cancelar reservas
                    cancelarReserva(reservas, usuario_actual)
                elif seleccion==5:
                    # Cerrar sesion
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Sesión cerrada.")
                    time.sleep(2)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    

                    salir2 = False
        else:
            print("\n   ¡¡¡¡Gracias por utilizar nuestro Sistema de Vuelos!!!!")
            print("\n\t\t***** ADIOS *****\n")
            salir = False

# Programa Principal

# Paises unicamente de america del norte y sur
matrizPaisesCapitales = [
    ["Canadá", "Ottawa"],
    ["Estados Unidos", "Washington, D.C."],
    ["México", "Ciudad de México"],
    ["Guatemala", "Ciudad de Guatemala"],
    ["Belice", "Belmopán"],
    ["Honduras", "Tegucigalpa"],
    ["El Salvador", "San Salvador"],
    ["Nicaragua", "Managua"],
    ["Costa Rica", "San José"],
    ["Panamá", "Ciudad de Panamá"],
    ["Argentina", "Buenos Aires"],
    ["Bolivia", "La Paz"],
    ["Brasil", "Brasília"],
    ["Chile", "Santiago"],
    ["Colombia", "Bogotá"],
    ["Ecuador", "Quito"],
    ["Paraguay", "Asunción"],
    ["Perú", "Lima"],
    ["Uruguay", "Montevideo"],
    ["Venezuela", "Caracas"]
]

# Menu de interaccion
main()

