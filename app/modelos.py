from abc import ABC, abstractmethod
import csv
import sqlite3

class Model(ABC):
    
    @classmethod
    @abstractmethod
    def create_from_dict(cls, diccionario):
        pass

class Director(Model):
    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(diccionario["nombre"], int(diccionario["id"]))


    def __init__(self, nombre: str, id: int = -1):
        self.nombre = nombre
        self.id = id

    def __repr__(self) -> str:
        return f"Director ({self.id}): {self.nombre}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id and self.nombre == other.nombre
        return False
    
    def __hash__(self):
        return hash((self.id, self.nombre))


class Pelicula(Model):

    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(diccionario["titulo"], 
                                      diccionario["sinopsis"], 
                                      int(diccionario["director_id"]), 
                                      int(diccionario["id"]))



    def __init__(self, titulo: str, sinopsis: str, director: object, id = -1):
        self.titulo = titulo
        self.sinopsis = sinopsis
        self.id = id
        self.director = director

    def __repr__(self) -> str:
        return f"Pelicula: ({self.titulo}), Sinopsis: {self.sinopsis}, Director: {self.director}, Id: {self.id}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.titulo == other.titulo and self.sinopsis == other.sinopsis and self.director == other.director and self.id == other.id
        return False
    
    def __hash__(self):
        return hash((self.titulo, self.sinopsis, self.director, self.id))
                
    @property
    def director(self):
        return self._director
    
    @director.setter
    def director(self, value):
        if isinstance(value, Director):
            self._director = value
            self._id_director = value.id
        elif isinstance(value, int):
            self._director = None
            self._id_director = value
        else:
            raise TypeError(f"{value} debe ser un entero o instancia de Director")


class Genero(Model):

    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(int(diccionario["id"]), diccionario["genero"])
    
    def __init__(self, genero: str , id: int = -1):
        self.id = id
        self.genero = genero

    def __repr__(self) -> str:
        return f"Genero: ({self.id}):{self.genero}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id and self.genero == other.genero
        return False
    
    def __hash__(self):
        return hash((self.id, self.genero))

class DAO(ABC):
    """
    @abstractmethod
    def guardar(self, instancia):
        pass
    
    @abstractmethod
    def actualizar(self, instancia):
        pass
    
    @abstractmethod
    def borrar(self, id: int):
        pass
    
    @abstractmethod
    def consultar(self, id: int):
        pass
    """

    @abstractmethod
    def todos(self):
        pass

class DAO_CSV(DAO):

    model = None

    def __init__(self, path, encoding="utf-8"):
        
        self.path = path
        self.encoding = encoding
    def todos(self):
        with open(self.path, "r", newline="", encoding=self.encoding) as fichero:
            lector_csv = csv.DictReader(fichero, delimiter=";", quotechar="'")
            lista = []
            for registro in lector_csv:
                lista.append(self.model.create_from_dict(registro))
        return lista   

class DAO_CSV_Director(DAO_CSV):
    

    model = Director
             

class DAO_CSV_Pelicula(DAO_CSV):
   

    model = Pelicula

class DAO_CSV_Genero(DAO_CSV):
    model = Genero


class DAO_SQLite(DAO):
    model = None
    tabla = None

    def __init__(self, path):
        self.path = path
        tabla = None
    
    def todos(self):
        """
        acceder a sqlite y traer todos los regustros de la tabla del modelo
        con la funcion rows_to_dictlist traerlos en forma de diuccionario
        devolverlos como instancias de Model
        """

        con = sqlite3.connect(self.path)
        cur = con.cursor()

        
        
        cur.execute(f"select * from {self.tabla}")
        nombres = list(map(lambda item: item[0], cur.description))

        lista = self.__rows_to_dictlist(cur.fetchall(), nombres)
        
        resultado = []

        # Evitar este segundo bucle( es segundo porque elprimero esta en la lunea  176) haciendo que
        # rows_to_dicc... devuelva una lista de Modelos y no una lista de diccionarios
        for registro in lista:
           resultado.append(self.model.create_from_dict(registro))

           con.close()
           
        return resultado

    def __rows_to_dictlist(self, filas, nombres):
        registros = []
        for fila in filas:
            registro = {}
            pos = 0
            for nombre in nombres:
                registro[nombre] = fila[pos]
                pos += 1

            """
            for pos, nombre in enumerate(nombres):
                registro[nombre] = fila[pos]
            """
            registros.append(registro)
        return registros


class DAO_SQLite_Director(DAO_SQLite):
    model = Director
    tabla = "directores"