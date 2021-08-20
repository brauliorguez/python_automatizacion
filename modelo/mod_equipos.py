#importamos a nuestras bibliotecas
import sqlite3
from prettytable import PrettyTable,from_db_cursor
from colorama import init, Fore, Back, Style
#creamos la clase y sus atributos
class conexion_equipos():
    #Constructor
    def __init__(self):
        try:
            self.conexion = sqlite3.connect('modelo//equipos.db')
            self.cursor = self.conexion.cursor()
        except Exception as Error:
            print(Error)        
    #cierra la conexion
    def cerrar(self):
        self.conexion.close()
#busca un registro por medio del nombre del equipo y envia un objeto tipo prettytable
#y si no lo encuentra retorna un False
    def buscar_registro(self, nombre):
        try:
            sql = "SELECT * FROM configuracion WHERE nombre = :nombre"
            self.cursor.execute(sql, {'nombre': nombre})
            self.conexion.commit()
            resultado = self.cursor.fetchall()
            self.cursor.execute(sql, {'nombre': nombre})
            self.conexion.commit()
            tabla=from_db_cursor(self.cursor)
            if resultado:
                return (tabla)
            else:
                return (False)
        except Exception as Error:
            return Error
#busca un registro por medio del id del equipo y envia un objeto tipo tupla y si no lo encuentra retorna un False
    def obtener_registro(self, id):
        try:
            sql = "SELECT * FROM configuracion WHERE id = :id"
            self.cursor.execute(sql, {'id': id})
            self.conexion.commit()
            row = self.cursor.fetchall()
            if row:
                return (row)
            else:
                return (False)
        except Exception as Error:
            return Error
#busca todos los registros y envia un objeto tipo prettytable si no lo encuentra retorna un False
    def mostrar_registros(self):
        try:
            sql = 'SELECT * FROM configuracion'
            self.cursor.execute(sql)
            self.conexion.commit()
            tabla=from_db_cursor(self.cursor)

            #verificar si hay registros
            self.cursor.execute(sql)
            self.conexion.commit()
            consul=self.cursor.fetchall()
            if consul:
                return (tabla)
            else:
                return False
        except Exception as Error:
            return Error
#metodo para insertar un registro, espera una tupla con los datos a insertar
    def agregar_registro(self,tupla):
        try:
            sql = "INSERT INTO configuracion (nombre,modelo,serie,ip,usuario,password,secret) VALUES (?,?,?,?,?,?,?);"
            self.cursor.execute(sql,tupla)
            self.conexion.commit()
            return True
        except Exception as Error:
            return Error
#metodo para validar un dato en este caso con el nombre del equipo y retorna una tupla con los datos
    def validar_dato(self, dato):
        try:
            sql = "SELECT * FROM configuracion WHERE nombre = :nombre"
            self.cursor.execute(sql, {'nombre': dato})
            self.conexion.commit()
            row = self.cursor.fetchall()
            if row:
                return row
            else:
                return False
        except Exception as Error:
            return Error
#metodo para eliminar un registro, espera el nombre del equipo a eliminar
    def eliminar_registro (self, tupla):
        elemento=[]
        registros=self.validar_dato(tupla)
        if registros==False:
            return False
        elif len(registros)==1:
            try:
                sql = "DELETE FROM configuracion WHERE id = :id"
                self.cursor.execute(sql, {'id': registros[0][0]})
                self.conexion.commit()
                return True
            except Exception as Error:
                return Error
        else:
            print("Se encontraron %d registros" %(len(registros)-1))
            for i in range(0,len(registros)):
                print("Registro de equipo ",i, registros[i])
            ingrese=int(input("Ingrese el numero de registro a eliminar  ó el número -1 si quiere eleminiar todas las coeincidncias: "))
            #vaida de que sea un numero dentro del rango
            if ingrese>=0 and ingrese<len(registros):
                elemento.append(registros[ingrese])
            elif ingrese==-1:
                try:
                    sql= "DELETE FROM configuracion;"
                    self.cursor.execute(sql)
                    self.conexion.commit()
                    return True
                except Exception as Error:
                    return Error
            else:
                print("Error, ingrese un numero valido")  
            try:
                sql = "DELETE FROM configuracion WHERE id = :id"
                self.cursor.execute(sql,{'id': elemento[0][0]})
                self.conexion.commit()
                return True
            except Exception as Error:
                    return Error
#metodo para eliminar todos los registros pide una contraseña en este caso admin   
    def eliminar_registros(self):
        print(Fore.WHITE,Back.BLUE+" ESTAS A PUNTO DE ELLIMINAR TODO: "+Fore.RESET,Back.RESET)
        contra=input("Ingresa la contraseña para proceder: ")
        for i in range(0,3,1):
                if contra == "admin":
                    ejecutar=input(Fore.RED+"Estas realmente seguro que deseas eliminar  todos los usuarios [S/N]: ")
                    if ejecutar.upper() in ["S"]:
                        try:
                            sql= "DELETE FROM configuracion;"
                            self.cursor.execute(sql)
                            self.conexion.commit()
                            return True
                        except Exception as Error:
                            return Error
                    elif ejecutar.upper() in ["N"]:
                        break
                else:
                    contra=input("Contraseña erronea, ingresa la contraseña correcta (Intentos %s de 3): "%i)
#metodo para actualizar un registro, espera una tupla con los datos a actualizar y el id del registro       
    def modificar_registro(self,lista,id):
        #crea una lista con los campos que se desean modificar
        self.campos=["nombre","modelo","serie","ip","usuario","password","secret"]
        l=lista
        print(id)
        print(l)
        #descoposicion de a lista de actualizacion del dispositivo
        indice=0
        c="'"
        try:
            for valor in self.campos:
                sql = "UPDATE configuracion SET "+valor+"="+c+l[indice]+c+" WHERE id = :id"
                self.cursor.execute(sql,{'id': id})
                self.conexion.commit()
                indice+=1
            return True
        except Exception as Error:
            return Error
#metodo que valida si la ip esta y evitar ips duplicadas 
    def buscar_ip(self, ip):
        #verifica si ip ya esta registrado
        try:
            sql = "SELECT * FROM configuracion WHERE ip = :ip"
            self.cursor.execute(sql, {'ip': ip})
            self.conexion.commit()
            row = self.cursor.fetchall()
            if row:
                return True
            else:
                return False
        except Exception as Error:
            return Error
