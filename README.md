# ddd-python-rest-mysql
Proyecto que consiste en armar un servicio web que exponga un endpoint para leer un archivo, consultar una serie de APIs públicas y cargar una base de datos con los datos del archivo y las consultas a las APIs, construido con patrones de diseño, concurrencia y Domain Driven Design.

### Prerequisitos

**1:** Clonar el proyecto a través del cliente git o desde desde un navegador.
```
git clone https://github.com/egmartin1810/ddd-python-rest-mysql.git
```
**2:** Tener Docker instalado de la página oficial: https://docs.docker.com/get-docker/. (instalar la última versión de Docker en su sistema operativo).

### Instalación

**Paso 1:** Estar dentro del directorio del proyecto que fue clonado:

```
cd ddd-python-rest-mysql
```

**Paso 2:** Ejecutar los contenedores:

```
docker-compose up -d --build 
```
**Paso 3:** Verificar que los contenedores estén ejecutando.

```
docker-compose ps -a
```

**Paso 4:** Verificar que la aplicación subió correctamente.

```
docker logs ddd-python-rest-mysql_app_1

```

**Paso 5:** Verificar que la Base de Datos mysql subió correctamente.

```
docker exec -it ddd-python-rest-mysql_db_1 mysql -uroot -p

```
le solicita el password el cual es: root

y revisar que la tabla meli.item se encuentre, en la consola de mysql:

```
 select * from meli.item;

```

**Paso 6:** Ejecutar el servicio rest expuesto por la aplicación creada.

```
curl -X POST http://127.0.0.1:5000/api/v1/almacenardatositems

```

**Paso 7:** Una vez de tener la respuesta del servicio rest, Validar que los 2000 registros estén en la tabla meli.item.

```
comando: docker exec -it ddd-python-rest-mysql_db_1 mysql -uroot -p
password: root
select * from meli.item; 

```

## Documentación y Desafío Técnico:

Por último dentro de la carpera documetnación de directorio del proyecto, podemos encontrar el documento con el detalle de la instalación de la aplicación, un documento técnico con unos diagramas muy explicativos de la solución y la respuesta del Desafío Teórico.

[Link-Documentación] (https://github.com/egmartin1810/ddd-python-rest-mysql/tree/master/documentaci%C3%B3n) - Documentación y Desafío Técnico.
