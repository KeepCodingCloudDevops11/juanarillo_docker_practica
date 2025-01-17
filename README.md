# PRÁCTICA CONTENEDORES: MÁS QUE VMS DOCKER - JUAN ARILLO
Práctica de Juan Arillo para el módulo de **Contenedores: Más que VMs Docker** a la nube.

## TABLA DE CONTENIDOS
[Descripción](#descripción)  
[Funcionamiento](#funcionamiento)  
[Puesta en marcha](#puesta-en-marcha)

## DESCRIPCIÓN
Este proyecto despliega una aplicación *Flask* que trabaja sobre una base de datos *Redis*.  

La aplicación *Flask* muestra un texto con los datos del *Host* y del *Puerto* donde se despliega el servicio de la
base de datos *Redis*, más un texto que muestra las veces que se ha cargado la página principal de la aplicación.

El servicio de la base de datos *Redis*, sirve como persistencia del número de veces que se visita la página principal
de la aplicación.

Adicionalmente, se han añadido logs a la aplicación para que salga por STDOUT / STDERR, así como el guardado
de estos logs en un servicio *ElasticSearch*, a los cuales se pueden acceder a través de una ruta añadida a la aplicación
*Flask*.

Por último, también se despliega un servicio *Kibana* para trabajar con la información de los logs guardados en el
servicio *ElasticSearch*.

## FUNCIONAMIENTO

## PUESTA EN MARCHA
