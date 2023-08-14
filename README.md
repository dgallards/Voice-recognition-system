# SECUREMAILING.VOICE

¿No estás cansado de que te roben la cuenta de correo o de robar correos tan fácilmente?

Te presentamos Securemailing.voice, tu deficiente app encargada de reconocerte a ti y solo a ti para enviar correos de una forma más segura.

Con, no solo uno, si no dos mecanismos de seguridad para garantizarte los estándares más elevados de seguridad de un país del tercer mundo, por el modico precio de 3 copilots.

--------------------------------------------------------------------------------

El objetivo de este proyecto es crear un pequeño programa capaz de identificar usuarios a partir de una voz y una contraseña únicas utilizando Machine Learning.
Para ello ofrece una interfaz gráfica con varias funciones básicas implementadas, tales como la creación de usuario y su inicio de sesión, gestión de credenciales y envío de correos.

Se utiliza una gran cantidad de tecnologías en el proyecto tales como MongoDB, PyQt, Cloud Speech o Machine Learning entre otras.

Si bien el Jupyter Notebook vale como una pequeña demo limitada para mostrar el proceso técnico que el programa usa, la versión en Python ofrece la interfaz gráfica y más libertad en las acciones a escoger.

--------------------------------------------------------------------------------
TODO PLAUSIBLE:
 - Añadir excepciones a varios métodos, como:
       - Que el usuario deba añadir algo en los campos de las credenciales al crear su cuenta, como se hace al modificar las credenciales de uno existente.
       - Añadir una excepción cuando el modelo tenga menos de dos voces.
 - Comprobar si sería demasiado restrictivo que la similitud de las contraseñas fuese de un 100%, en vez de un 80%.
 - Mejorar el modelo actual para lograr mayor precisión, aunque en pruebas locales ha mejorado enormemente, el dataset es muy pequeño.

TODO NO PLAUSIBLE:
 - Mejorar la interfaz de usuario.
 - Pasar a Android con una app.
 - Migrar los servicios a un servidor de microservicios.
