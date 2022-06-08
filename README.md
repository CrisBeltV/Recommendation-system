# Sistema de recomendación

Este proyecto consta de un sistema de recomendación que sugiere al usuario un platillo a partir de los ingredientes de los platillos pedidos por el usuario en el pasado, el sistema también permite ingresar nuevos platillos y nuevos usuarios **El método de recomendación se denomina basado en contenido con esta técnica buscamos identificar los ingredientes favoritos de usuario** (arroz, carne, pollo, aguacate, etc) **para algún platillo que haya pedido el usuario para luego recomendar dichos platos que contienen esos ingredientes hayan sido pedidos con anterioridad o no por dicho usuario.**, es decir que el sistema hará la recomendación de platillos de comida en base a la frecuencia en la que un usuario particular pide los ingredientes de dichos platos.

La recomendación se hace a partir de una “base de datos” (realmente es solo dos hojas de un archivo Excel) que consta de dos tablas una llamada “ranking” que contiene los registros de cada pedido que han hechos los usuarios y de una llamada “platos” contiene los registros de los platillos de comida de la base de datos, esto fácilmente podria ser los platillos del menú de un restaurante, etc. Las tablas se relacionan entre el ID de la tabla "platos" y el ID_PLATO de la tabla “ranking”.

### Capturas de la base de datos

<img src="https://github.com/CrisBeltV/Recommendation-system/blob/main/img/Captura1.JPG?raw=true"  width="500" />

<img src="https://github.com/CrisBeltV/Recommendation-system/blob/main/img/Captura2.JPG?raw=true"  width="500" />

La interface grafica permite consultar el plato mas recomendado de un usuario particular al igual que permite cambiar a una pantalla diferente que deja ingresar nuevos registros en nuestra base de usuarios y platos (el Excel), con estos nuevos registros ya se podrá pedir una recomendación del usuario nuevo o bien actualizará la lista de recomendación de platos de un usuario existente al ingresar un nuevo conjunto de ingredientes, es decir un nuevo plato, acompañado de una valoración del plato. Esto es algo similar a cuando se da una calificación en estrellas o puntos a un producto este valor tendrá un peso en las valoraciones de los platos que ayudara a ponderar la clasificación de la recomendación de los platos de comida.

Proyectos de los que me apoye.
https://github.com/MariyaSha/BinarytoDecimal
https://www.statdeveloper.com/recomendaciones-basado-en-contenido-en-python/

