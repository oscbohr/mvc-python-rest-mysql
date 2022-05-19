# mvc-python-rest-mysql
Proyecto que expone un API Rest  para procesar un archivo y consultar una serie de APIs de MERCADO LIBRE y cargar el resultado del proceso una base de datos con los datos del archivo inicial y el resultado de las consultas a las APIs.

### Prerequisitos

**1:** Clonar el proyecto a través del cliente git o desde desde un navegador.
```
git clone https://github.com/oscbohr/mvc-python-rest-mysql.git
```
**2:** Tener Docker instalado docker o instalar la última versión en su sistema operativo  (url: https://docs.docker.com/get-docker/)

### Instalación

**Paso 1:** Localizarse dentro del directorio del proyecto que fue clonado:

```
cd mvc-python-rest-mysql-main
```

**Paso 2:** Ejecutar el comando para la construcción de los contenedores:

```
docker-compose up -d --build 
```
**Paso 3:** Verificar la correcta ejecución de los contenedores.

```
docker-compose ps -a
```

**Paso 4:** Verificar que la app haya iniciado satisfactoriamente.

```
docker logs -f meli-procesar-archivo-backend

```

**Paso 5:** Verificar que la Base de Datos mysql subió correctamente.

```
docker exec -it meli-procesar-archivo-mysql -uroot -p

```
le solicita el password el cual es: my-secret-pw

y revisar que la tabla tablas se encuentren:

```
 show tables;

```

**Paso 6:** Ejecutar el servicio rest expuesto por la aplicación creada.

```
PROCESAR: curl --header "Content-Type: application/json" --request POST \
		 --data '{}' http://localhost:5000/api/v1/procesararchivo


CONSULTAR: curl --header "Content-Type: application/json" --request GET \
		 --data '{}' http://localhost:5000/api/v1/procesararchivo?rows=300
 
ELIMINAR: curl --header "Content-Type: application/json" --request DELETE \
		 --data '{}' http://localhost:5000/api/v1/eliminarprocesoarchivo
			
```
Observacion: Para prueba inicial, se sugiere ejecutar en este orden:
	1- POST
	2- GET

**Paso 7:** Validar la respuesta del servicio REST ingresando a la Base de Datos y realizar consultas sobre
la tabla "ItemsProcesados" e "ItemsRechazados"

```
comando: docker exec -it meli-procesar-archivo-mysql mysql -uroot -p
password: my-secret-pw
select * from ItemsProcesados;
select * from ItemsRechazados;

```
Nota: Si es la primera vez que se ejecuta, el *count( * ) de ItemsRechazados mas la suma con el count( * ) de ItemsProcesados* debe ser igual al total de filas del archivo.


## Documentación y Desafío Técnico:

Por último dentro de la carpera documetnación de directorio del proyecto, podemos encontrar el documento con el detalle de la instalacióny la resolución del Desafío Teórico.

