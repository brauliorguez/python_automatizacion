import modelo.mod_equipos as modelo
import napalm
import yaml
from jinja2 import FileSystemLoader, Environment
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style

class equipo(object):
    # Metodos set y get de los datos de la clase equipo
    def set_id(self, id):
        """Asigna un id al equipo"""
        self.id = id
    def get_id(self):
        """Retorna el id del equipo"""
        return self.id
    def set_nombre(self, nombre):
        """Asigna un nombre al equipo"""
        self.nombre = nombre
    def get_nombre(self):
        """Retorna el nombre del equipo"""
        return self.nombre  
    def set_modelo(self, modelo):
        """Asigna un modelo al equipo"""
        self.modelo = modelo
    def get_modelo(self):
        """Retorna el modelo del equipo"""
        return self.modelo    
    def set_serie(self, serie):
        """Asigna una serie al equipo"""
        self.serie = serie
    def get_serie(self):
        """Retorna la serie del equipo"""
        return self.serie
    def set_ip(self, ip):
        """Asigna una ip al equipo"""
        self.ip = ip
    def get_ip(self):
        """Retorna la ip del equipo"""
        return self.ip
    def set_usuario(self, usuario):
        """Asigna un usuario al equipo"""
        self.usuario = usuario
    def get_usuario(self):
        """Retorna el usuario del equipo"""
        return self.usuario
    def set_password(self, password):
        """Asigna un password al equipo"""
        self.password = password
    def get_password(self):
        """Retorna el password del equipo"""
        return self.password
    def set_secret(self, secret):
        """Asigna un secret al equipo"""
        self.secret = secret
    def get_secret(self):
        """Retorna el secret del equipo"""
        return self.secret
#funcion que establece la conexion con el equipo en gns3 esto por medio de napalm
    def conexion(self):
        CONFIG = {
            'hostname': self.ip,
            'username': self.usuario,
            'password': self.password,
            'optional_args': {'port':22,'secret': self.secret}
            }
        self.device = napalm.get_network_driver('ios')
        self.device = self.device(**CONFIG)
        print(self.device)
        self.device.open()
#funcion que permite obtener el nomnre del equipo y retorna el hostname 
    def hostname(self):
        return self.device.hostname
#funcion que permite obtener la contraseña del equipo y retorna el password
    def clave(self):
        return self.device.password
#funcion que permite obtener el usuario y retorna el usuario
    def user(self):
        return self.device.username
#funcion que permite obtener los usuarios del equipo y retorna una lista con los usuarios
    def get_usuarios(self):
        usuarios = self.device.get_users()
        for key,valores in usuarios.items():
            print('usuario: ' + str(key))
            for k,v in valores.items():
                print('  ' + str(k) + ": "+str(v))
#funcion que permite obtener las interfaces del equipo y retorna una lista con las interfaces       
    def get_interfaces(self):
        interfaces = self.device.get_interfaces()
        for key,valores in interfaces.items():
            print('interface: ' + str(key))
            for k,v in valores.items():
                print('  ' + str(k) +": "+ str(v))
#funcion que permite configurar el equipo, por medio de una plantilla y su archivo de configuracion
    def set_configuracion(self):
        config_data = yaml.load(open('plantillas/'+'{}_template.yml'.format(self.serie)), Loader=yaml.FullLoader)
        env = Environment(loader = FileSystemLoader('plantillas'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('cisco_template.j2')
        print(template.render(config_data))
        renderizado = template.render(config_data)
        self.device.load_merge_candidate(filename=None, config=renderizado)
        self.device.commit_config()


#funciones que se crearon con el fin de hacer los distintos menus dentro de la aplicacion
#menu principal
def menu_principal():
    """Funcion que muestra el menu principal"""
    menu_prin=PrettyTable()
    menu_principal={1:"Administrar equipos",2: "Configurar Equipos",3 :"Salir"}
    menu_prin.field_names=["Tecla","Opciones"]
    for x in menu_principal:
        menu_prin.add_row([x,menu_principal[x]])
    menu_prin.header_style = 'upper'
    menu_prin.align["Tecla,Opciones"] = "c"
    menu_prin.horizontal_char = '_'
    menu_prin.vertical_char = '|'
    menu_prin.junction_char = '+'
    print(Fore.LIGHTBLUE_EX,menu_prin,Fore.RESET)
#menu de administracion de equipos
def menu():
    """Funcion que muestra el menu"""
    menu=PrettyTable()
    menu_opciones={1:"Agregar Un Registro",2:"Buscar Un Registro",3:"Modificar Un Registro",4:"Eliminar Un Registro",5:"Mostrar Todos  los registros",6:"Eliminar Todos los registros",7:"Menu anterior"}
    menu.field_names = ["Teclea","Opciones"]
    for x in menu_opciones:
        menu.add_row([x,menu_opciones[x]])
    menu.header_style = 'upper'
    menu.align["Teclea"] = "c"
    menu.horizontal_char = '_'
    menu.vertical_char = '|'
    menu.junction_char = '+'
    print(Fore.YELLOW,menu,Fore.RESET)
#menu de configuracion de equipos
def menu_secundario():
    """Funcion que muestra el menu secundario"""
    menu_secundario=PrettyTable()
    #crea un diccionario donde se muestra las opciones de la tabla
    menu_secu={1:"Hostaname",2:"Usuario",3:"contraseña",4:"Usuarios",5:"Interfaces",6:"Aplicar configuracion",7:"Regresar al menu anterior"}
    menu_secundario.field_names=["Tecla","Opciones"]
    for x in menu_secu:
        menu_secundario.add_row([x,menu_secu[x]])
    menu_secundario.header_style = 'upper'
    menu_secundario.align["Tecla,Opciones"] = "c"
    menu_secundario.horizontal_char = '_'
    menu_secundario.vertical_char = '|'
    menu_secundario.junction_char = '+'
    print(Fore.MAGENTA,menu_secundario,Fore.RESET)
#funcion que permite validar el dato ingresado por el usuario, esta dividido en distintos menus ya que verifica el que lo ingresado 
#es un numero entero y este dentro del rango de la lista de opciones correspondientes a cada menu.
def valida_opcion(menu):
    """Funcion que valida la opcion de ingreso el usuario"""
    # Funcion que valida si la opcion que ingreso el usuario es un numero entero
    correcto=False
    num=0
    if menu ==1:            
        while(not correcto):
            try:
                opcion = int(input(Fore.YELLOW+"Ingresa la opcion (La opcion en número entero): "+Fore.RESET))
                correcto=True
            except ValueError:
                print (Fore.WHITE,Back.RED+"  Introduce un número entero     ",Fore.RESET,Back.RESET)
            if correcto:
                if opcion>0 and opcion<4:
                    return opcion
                else:
                    print(Fore.WHITE,Back.RED+"  La opcion debe ser de 1 a 3    ",Fore.RESET,Back.RESET)
    elif menu == 2:
        while(not correcto):
            try:
                opcion = int(input(Fore.YELLOW+"Ingresa la opcion (La opcion en número entero): "+Fore.RESET))
                correcto=True
            except ValueError:
                print (Fore.WHITE,Back.RED+"  Introduce un número entero     ",Fore.RESET,Back.RESET)
            if correcto:
                if opcion>0 and opcion<8:
                    return opcion
                else:
                    print(Fore.WHITE,Back.RED+"  La opcion debe ser de 1 a 7    ",Fore.RESET,Back.RESET)
    elif menu == 3:
        while(not correcto):
            try:
                opcion = int(input(Fore.YELLOW+"Ingresa la opcion (La opcion en número entero): "+Fore.RESET))
                correcto=True
            except ValueError:
                print (Fore.WHITE,Back.RED+"  Introduce un número entero     ",Fore.RESET,Back.RESET)
            if correcto:
                if opcion>0 and opcion<6:
                    return opcion
                else:
                    print(Fore.WHITE,Back.RED+"  La opcion debe ser de 1 a 8    ",Fore.RESET,Back.RESET)
#set y get de datos para cuando sea registrado unn equipo, regresara los datos que se capturaron
def set_get_datos(objeto_quipos,dic):
    """Funcion que setea los datos del equipo desde el diccionario creado"""
    if dic['NOMBRE']!='':
        objeto_quipos.set_nombre(dic['NOMBRE'])
        objeto_quipos.set_modelo(dic['MODELO'])
        objeto_quipos.set_serie(dic['SERIE'])
        objeto_quipos.set_ip(dic['IP'])
        objeto_quipos.set_usuario(dic['USUARIO'])
        objeto_quipos.set_password(dic['PASSWORD'])
        objeto_quipos.set_secret(dic['SECRET'])
        print(Fore.GREEN+"\n  Se capturaron los siguientes datos \n"+Fore.RESET)
        nombre=objeto_quipos.get_nombre()
        modelo=objeto_quipos.get_modelo()
        serie=objeto_quipos.get_serie()
        ip=objeto_quipos.get_ip()
        usuario=objeto_quipos.get_usuario()
        password=objeto_quipos.get_password()
        secret=objeto_quipos.get_secret()
        print(Fore.YELLOW+"  Nombre: "+nombre+"\n  Modelo: "+modelo+"\n  Serie: "+serie+"\n  IP: "+ip+"\n  Usuario: "+usuario+"\n  Password: "+password+"\n  Secret: "+secret+Fore.RESET)
    else:
        print(Fore.WHITE,Back.RED+"  La entrada no puede ser vacia ",Fore.RESET,Back.RESET)



#esta clase se creo con el fin de no saturar la funcion main, y asi poder a los metodos correspondientes dentro de las opciones
class manejo_db_crud(object):
#constructor crea un objeto de la clase equipos y una de mod_equipos esto para gestionar los datos de los equipos y solcitar las consultas
    def __init__(self):
        """crea una instancia del clase equipo"""
        self.obj_equipo=equipo()
        self.obj_conexion=modelo.conexion_equipos()
#funcion que llama a la funcion de la clase conexion_equipos para insertar un equipo
    def registra(self):
        """ Llama a las funciones correspondientes para registrar un equipo"""
        lista_de_datos=[]#esta lista ayuda a almacenar temporalmente los datos para posteriormente convertirlos en una tupla
        """Funcion que llama a las otras funciones"""
        dic=self.solicitar_datos()
        set_get_datos(self.obj_equipo, dic)
        #covierte los datos de diccionario en una tupla
        for valor in dic.values():
            lista_de_datos.append(valor)
            #convvertir la lista en una tupla
        tupla_de_datos=tuple(lista_de_datos)
        #llama a la funcion agregar_registro de la clase conexion_equipos
        estatus=self.obj_conexion.agregar_registro(tupla_de_datos)
        #si el estatus es true
        if estatus:
            print(Fore.GREEN+"  Registro agregado correctamente"+Fore.RESET)
        else:
            print(Fore.WHITE,Back.RED+"  Registro no agregado"+Fore.RESET,Back.RESET)
#funcion que llama a la funcion de la clase conexion_equipos para consultar un equipo
    def buscar(self):
        """Llama a las funciones correspondientes para buscar un equipo"""
        resgistros_estatus=self.obj_conexion.mostrar_registros()
        if resgistros_estatus:
            #pedirle l usuario que ingrese el nombre del equipo a buscar
            nombre=input(Fore.YELLOW+"Ingresa el nombre del equipo a buscar: "+Fore.RESET)
            #llama a la funcion buscar_registro de la clase conexion_equipos
            estatus=self.obj_conexion.buscar_registro(nombre)
            #si el estatus es true
            if estatus == False:
                print(Fore.WHITE,Back.RED+"  Registro no encontrado"+Fore.RESET,Back.RESET)
            else:
                print(Fore.GREEN+"  Registro encontrado correctamente"+Fore.RESET)
                print(Fore.GREEN+str(estatus)+Fore.RESET)
        else:
            print(Fore.WHITE,Back.RED+"  No hay registros en el base de datos, Debe agregar un registro primero"+Fore.RESET,Back.RESET)
            opcion_valida=input(Fore.YELLOW+"  Desea crear un nuevo registro? (S/N): "+Fore.RESET)
            if opcion_valida.upper() in ["S"]:
                self.registra()
            else:
                pass
#funcion que llama a la funcion de la clase conexion_equipos para modificar un equipo 
    def modificar(self):
        """Llama a las funciones correspondientes para modificar un equipo"""
        resgistros_estatus=self.obj_conexion.mostrar_registros()
        if resgistros_estatus:
            almacenar_datos=[]
            busqueda=input(Fore.YELLOW+"Ingresa el nombre del equipo a modificar: "+Fore.RESET)
            #llama a la funcion buscar_registro de la clase conexion_equipos
            registro=self.obj_conexion.validar_dato(busqueda)
            #si el estatus es true
            if registro == False:
                print(Fore.WHITE,Back.RED+"  Registro no encontrado"+Fore.RESET,Back.RESET)
            else:
                registro=list(registro[0])
                print(registro)
                print(type(registro))
                lista_de_preguntas=["NOMBRE","MODELO","SERIE","IP","USUARIO","PASSWORD","SECRET"]
                i=1
                print(Fore.GREEN+"  Registro encontrado correctamente"+Fore.RESET)
                for pregunta in lista_de_preguntas:
                    valor=input(pregunta+"(Valor predeterminado = "+registro[i]+"):" or {registro[i]})
                    if not valor:
                        valor=registro[i]
                    i+=1
                    almacenar_datos.append(valor)
                #llama a la funcion modificar_registro de la clase conexion_equipos
                estatus=self.obj_conexion.modificar_registro(almacenar_datos,registro[0])
                print(estatus)
                #si el estatus es true
                if estatus:
                    print(Fore.GREEN+"  Registro modificado correctamente"+Fore.RESET)
                else:
                    print(Fore.WHITE,Back.RED+"  Registro no modificado"+Fore.RESET,Back.RESET)
        else:
            print(Fore.WHITE,Back.RED+"  No hay registros en el base de datos, Debe agregar un registro primero"+Fore.RESET,Back.RESET)
            opcion_valida=input(Fore.YELLOW+"  Desea crear un nuevo registro? (S/N): "+Fore.RESET)
            if opcion_valida.upper() in ["S"]:
                self.registra()
            else:
                pass
#funcion que llama a la funcion de la clase conexion_equipos para eliminar un equipo
    def eliminar(self):
        """Llama a las funciones correspondientes para eliminar un equipo"""
         #muestra los reistros actuales
        resgistros_estatus=self.obj_conexion.mostrar_registros()
        if resgistros_estatus:
            print(Fore.GREEN+"  Lista de registros actuales"+Fore.RESET)
            print(Fore.LIGHTMAGENTA_EX+str(self.obj_conexion.mostrar_registros())+Fore.RESET)
            #pedirle al usuario que ingrese el nombre del equipo a eliminar
            nombre=input(Fore.YELLOW+"Ingresa el nombre del equipo a eliminar: "+Fore.RESET)
            #llama a la funcion eliminar_registro de la clase conexion_equipos
            estatus=self.obj_conexion.eliminar_registro(nombre)
            #si el estatus es true
            if estatus:
                print(Fore.GREEN+"  Registro eliminado correctamente\n"+Fore.RESET)
            else:
                    print(Fore.WHITE,Back.RED+"  Registro no eliminado, no se encontro coeincidencias con lo ingresado"+Fore.RESET,Back.RESET)
        else:
            print(Fore.WHITE,Back.RED+"  No hay registros en el base de datos, Debe agregar un registro primero"+Fore.RESET,Back.RESET)
            opcion_valida=input(Fore.YELLOW+"  Desea crear un nuevo registro? (S/N): "+Fore.RESET)
            if opcion_valida.upper() in ["S"]:
                self.registra()
            else:
                pass
#funcion que llama a la funcion de la clase conexion_equipos para mostrar los registros           
    def mostrar_todos(self):
        """Llama a las funciones correspondientes para mostrar todos los registros"""
        resgistros_estatus=self.obj_conexion.mostrar_registros()
        if resgistros_estatus:
            #llama a la funcion mostrar_registros de la clase conexion_equipos
            registros=self.obj_conexion.mostrar_registros()
            #si el estatus es true
            if registros:
                print(Fore.GREEN+str(registros)+Fore.RESET)
            else:
                print(Fore.WHITE,Back.RED+"  No hay registros en la base de datos"+Fore.RESET,Back.RESET)
        else:
            print(Fore.WHITE,Back.RED+"  No hay registros en el base de datos, Debe agregar un registro primero"+Fore.RESET,Back.RESET)
            opcion_valida=input(Fore.YELLOW+"  Desea crear un nuevo registro? (S/N): "+Fore.RESET)
            if opcion_valida.upper() in ["S"]:
                self.registra()
            else:
                pass
#funcion que llama a la funcion de la clase conexion_equipos para eliminar todos los registros
    def eliminar_todo(self):
        """Llama a las funciones correspondientes para eliminar todos los registros"""
        resgistros_estatus=self.obj_conexion.mostrar_registros()
        if resgistros_estatus:
            #llama a la funcion eliminar_registros de la clase conexion_equipos
            estatus=self.obj_conexion.eliminar_registros()
            #si el estatus es true
            if estatus:
                print(Fore.GREEN+"  Registros eliminados correctamente"+Fore.RESET)
            else:
                print(Fore.WHITE,Back.RED+"  Registros no eliminados"+Fore.RESET,Back.RESET)
        else:
            print(Fore.WHITE,Back.RED+"  No hay registros en el base de datos, Debe agregar un registro primero"+Fore.RESET,Back.RESET)
            opcion_valida=input(Fore.YELLOW+"  Desea crear un nuevo registro? (S/N): "+Fore.RESET)
            if opcion_valida.upper() in ["S"]:
                self.registra()
            else:
                pass
        # funcion que aolicitan los datos, muestran el menu y valida los datos
#funcion que solicita los datos del equipo y los guarda en un diccionario, valida tambien que la ip no este repetida
    def solicitar_datos(self):
        """Funcion que solicita los datos al usuario"""
        self.dic={'NOMBRE':'','MODELO':'','SERIE':'','IP':'','USUARIO':'','PASSWORD':'','SECRET':''}
        for clave in self.dic:
            while True:
                campo=input('Ingrese '+clave+': ')
                if len(campo)>0:
                    if clave=='IP':
                        while True:
                            estado=self.obj_conexion.buscar_ip(campo)
                            if estado:
                                campo=input(Fore.YELLOW+"  Ingrese otra "+clave+" diferente: "+Fore.RESET)
                            else:
                                self.dic[clave]=campo
                                break
                    else:
                        self.dic[clave]=campo
                    break;
                else:
                    print(Fore.WHITE,Back.RED+"  La entrada no puede ser vacia ",Fore.RESET,Back.RESET)
        return self.dic
#funcion que llama a la funcion de la clase conexion_equipos y clase equipos para consltar y gestionar los datos de un equipo
#ayuda a crear una conexion y obtener los datos del equipo que esta en gns3 y al final configura el equipo
    def busqueda_get_datos(self):
        """Llama a las funciones correspondientes para buscar un equipo"""
        obj_equipo=equipo()
        self.estado=True
        while self.estado:
            self.mostrar_todos()
            #pedirle al usuario que ingrese el nombre del equipo a buscar
            try:
                id=int(input(Fore.YELLOW+"Ingresa el ID del equipo: "+Fore.RESET))
                continua=True
            except ValueError:
                print(Fore.WHITE,Back.RED+"  Ingrese un valor numerico"+Fore.RESET,Back.RESET)
                continua=False
            if continua:
                #llama a la funcion buscar_registro de la clase conexion_equipos  
                estatus=self.obj_conexion.obtener_registro(id)
                #si el estatus es true
                if estatus:
                    #convierte estatus a una lista                        
                    obj_equipo.set_id(estatus[0][0])
                    obj_equipo.set_nombre(estatus[0][1])
                    obj_equipo.set_modelo(estatus[0][2])
                    obj_equipo.set_serie(estatus[0][3])
                    obj_equipo.set_ip(estatus[0][4])
                    obj_equipo.set_usuario(estatus[0][5])
                    obj_equipo.set_password(estatus[0][6])
                    obj_equipo.set_secret(estatus[0][7])
                    obj_equipo.conexion()
                    #llama a get y set de la clase conexion_equipos 
                    print(Fore.GREEN+"  Registro encontrado correctamente\n"+Fore.RESET)
                    tabla=PrettyTable()
                    tabla.field_names=["ID","NOMBRE","MODELO","SERIE","IP","USUARIO","PASSWORD","SECRET"]
                    for i in estatus:
                        tabla.add_row(i)
                    print(tabla)
                    while True:
                        #muestrae el menu secundario
                        menu_secundario()
                        opcion=input(Fore.YELLOW+"  Seleccione una opcion: "+Fore.RESET)
                        if opcion.upper() in ["1","2","3","4","5","6","7","8","9","10"]:
                            if opcion.upper()=="1":
                                print(Fore.YELLOW+"  Nombre: "+obj_equipo.hostname()+Fore.RESET)
                            elif opcion.upper()=="2":
                                print(Fore.YELLOW+"  Usuario: "+obj_equipo.user()+Fore.RESET)
                            elif opcion.upper()=="3":
                                print(Fore.YELLOW+"  Password: "+obj_equipo.clave()+Fore.RESET)
                            elif opcion.upper()=="4":
                                print(Fore.YELLOW+"  Usuarios: "+str(obj_equipo.get_usuarios())+Fore.RESET)
                            elif opcion.upper()=="5":
                                print(Fore.YELLOW+"  Interfaces: "+ str(obj_equipo.get_interfaces())+Fore.RESET)
                            elif opcion.upper()=="6":
                                print(Fore.YELLOW+"  Aplicar Configuracion: "+str(obj_equipo.set_configuracion())+Fore.RESET)
                            elif opcion.upper()=="7":
                                #rompe el ciclo
                                self.estado=False
                                break
                else:
                    print(Fore.WHITE,Back.RED+"  Registro no encontrado"+Fore.RESET,Back.RESET)
   

        
        
#Funcion principal que llama a los metodos de la clase crud_equipos
def main():
    #instancia del de un objeto de la clase manejo_db_crud
    objeto_crud=manejo_db_crud()
    #comienza el menu
    while True:
        menu_principal()
        opcion_menu=valida_opcion(menu=1)
        if opcion_menu==3:
            #si la opcion es 3 termina el programa
            break
        elif opcion_menu==1:
            menu()
            #solicita y valida la opcion del usuario
            opcion_valida=valida_opcion(menu=2)
            #si la opcion es 7 el progrma termina
            if opcion_valida == 7:
                #si la opcion es 7 termina este menu y regresa al menu principal
                pass
            #si la opcion es 1 agrega un registro al archivo
            elif opcion_valida == 1:
                objeto_crud.registra()
            #si la opcion es 2 busca un registro en el archivo
            elif opcion_valida == 2:
                objeto_crud.buscar()
            #si la opcion es 3 modifica un registro en el archivo
            elif opcion_valida == 3:
                objeto_crud.modificar()
            #si la opcion es 4 elimina un registro en el archivo
            elif opcion_valida == 4:
                objeto_crud.eliminar()
            #si la opcion es 5 muestra todos los registros en el archivo
            elif opcion_valida == 5:
                objeto_crud.mostrar_todos()
            #si la opcion es 6 elimina todos los registros en el archivo
            elif opcion_valida == 6:
                objeto_crud.eliminar_todo()
                pass
        elif opcion_menu==2:
#si la opcion es 2 muestra al usuario los registros existentes de equipos solicita el id del equipo 
# para crear una conexion con napal y mostrar los datos, incluso carge la configuracion
            objeto_crud.busqueda_get_datos()
            #tambien muestra el menu secundario y si teclea 7 regresa al menu principal
            
if __name__ == "__main__":
    main()