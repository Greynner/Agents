DOCUMENTACIÓN DE CASOS DE PRUEBA Y MATRICES DE TESTING
========================================================

1. CASOS DE PRUEBA EN GHERKIN
==============================

Feature: Sistema de autenticación de usuarios
  Como usuario del sistema
  Quiero poder iniciar sesión con mis credenciales
  Para acceder a mi cuenta personal

  Scenario: Login exitoso con credenciales válidas
    Given que estoy en la página de login
    And tengo un usuario registrado con email "usuario@test.com" y password "Pass123!"
    When ingreso el email "usuario@test.com"
    And ingreso el password "Pass123!"
    And hago clic en el botón "Iniciar Sesión"
    Then debo ser redirigido al dashboard principal
    And debo ver el mensaje "Bienvenido, Usuario"
    And la sesión debe estar activa

  Scenario: Login fallido con credenciales inválidas
    Given que estoy en la página de login
    When ingreso el email "usuario@test.com"
    And ingreso el password "PasswordIncorrecto"
    And hago clic en el botón "Iniciar Sesión"
    Then debo permanecer en la página de login
    And debo ver el mensaje de error "Credenciales incorrectas"
    And no debo tener sesión activa

  Scenario: Login con campo email vacío
    Given que estoy en la página de login
    When dejo el campo email vacío
    And ingreso el password "Pass123!"
    And hago clic en el botón "Iniciar Sesión"
    Then debo ver el mensaje de error "El email es requerido"
    And el botón "Iniciar Sesión" debe estar deshabilitado


Feature: Carrito de compras
  Como cliente de la tienda online
  Quiero gestionar productos en mi carrito
  Para realizar una compra

  Scenario: Agregar producto al carrito
    Given que estoy en la página de productos
    And veo el producto "Laptop HP" con precio "$999"
    When hago clic en el botón "Agregar al carrito"
    Then debo ver el mensaje "Producto agregado al carrito"
    And el contador del carrito debe mostrar "1"
    And el total del carrito debe ser "$999"

  Scenario: Eliminar producto del carrito
    Given que tengo 2 productos en mi carrito
    And el total del carrito es "$1500"
    When hago clic en "Eliminar" en el producto "Mouse Logitech"
    Then el producto debe ser removido del carrito
    And el contador del carrito debe mostrar "1"
    And el total debe actualizarse correctamente

  Scenario: Aplicar cupón de descuento válido
    Given que tengo productos en el carrito por un total de "$1000"
    When ingreso el cupón "DESCUENTO20"
    And hago clic en "Aplicar"
    Then debo ver el mensaje "Cupón aplicado exitosamente"
    And el descuento debe ser "$200"
    And el total final debe ser "$800"


Feature: Registro de nuevos usuarios
  Como visitante del sitio
  Quiero registrarme como usuario
  Para acceder a las funcionalidades del sistema

  Scenario: Registro exitoso con datos válidos
    Given que estoy en la página de registro
    When ingreso el nombre "Juan Pérez"
    And ingreso el email "juan.perez@test.com"
    And ingreso el password "Seguro123!"
    And confirmo el password "Seguro123!"
    And acepto los términos y condiciones
    And hago clic en "Registrarse"
    Then debo ver el mensaje "Registro exitoso"
    And debo recibir un email de confirmación
    And debo ser redirigido a la página de bienvenida

  Scenario: Registro con email duplicado
    Given que existe un usuario con email "usuario@test.com"
    When intento registrarme con el mismo email "usuario@test.com"
    Then debo ver el mensaje de error "Este email ya está registrado"
    And no se debe crear una nueva cuenta

  Scenario: Registro con contraseña débil
    Given que estoy en la página de registro
    When ingreso el password "123"
    Then debo ver el mensaje "La contraseña debe tener al menos 8 caracteres"
    And el botón "Registrarse" debe estar deshabilitado


2. MATRICES DE PRUEBAS
=======================

MATRIZ 1: PRUEBAS DE AUTENTICACIÓN
-----------------------------------
ID    | Caso de Prueba              | Prioridad | Estado    | Resultado Esperado
------|----------------------------|-----------|-----------|---------------------
TC001 | Login válido               | Alta      | Pasado    | Usuario autenticado
TC002 | Login con email inválido   | Alta      | Pasado    | Error mostrado
TC003 | Login con password inválido| Alta      | Pasado    | Error mostrado
TC004 | Login con campos vacíos    | Media     | Pasado    | Validación frontend
TC005 | Logout de usuario          | Alta      | Pasado    | Sesión cerrada
TC006 | Login con SQL injection    | Alta      | Pasado    | Input sanitizado
TC007 | Login con sesión expirada  | Media     | Fallado   | Redirigir a login
TC008 | Recuperar contraseña       | Media     | Pendiente | Email enviado

MATRIZ 2: PRUEBAS DE CARRITO DE COMPRAS
---------------------------------------
ID    | Caso de Prueba              | Prioridad | Estado    | Resultado Esperado
------|----------------------------|-----------|-----------|---------------------
TC101 | Agregar producto           | Alta      | Pasado    | Producto en carrito
TC102 | Eliminar producto          | Alta      | Pasado    | Producto removido
TC103 | Actualizar cantidad        | Alta      | Pasado    | Cantidad actualizada
TC104 | Aplicar cupón válido       | Media     | Pasado    | Descuento aplicado
TC105 | Aplicar cupón inválido     | Media     | Pasado    | Error mostrado
TC106 | Carrito con stock agotado  | Alta      | Fallado   | Notificar usuario
TC107 | Calcular total con IVA     | Alta      | Pasado    | Total correcto
TC108 | Persistir carrito          | Baja      | Pendiente | Carrito guardado

MATRIZ 3: PRUEBAS DE REGISTRO
------------------------------
ID    | Caso de Prueba              | Prioridad | Estado    | Resultado Esperado
------|----------------------------|-----------|-----------|---------------------
TC201 | Registro con datos válidos | Alta      | Pasado    | Usuario creado
TC202 | Registro email duplicado   | Alta      | Pasado    | Error mostrado
TC203 | Validar formato email      | Media     | Pasado    | Validación ok
TC204 | Password seguro            | Alta      | Pasado    | Cumple requisitos
TC205 | Confirmar password         | Alta      | Pasado    | Passwords coinciden
TC206 | Aceptar términos           | Media     | Pasado    | Checkbox requerido
TC207 | Email de verificación      | Alta      | Fallado   | Email no enviado
TC208 | Activar cuenta             | Media     | Pendiente | Cuenta activada


3. CRITERIOS DE ACEPTACIÓN
===========================

Para el sistema de login:
- El tiempo de respuesta debe ser menor a 2 segundos
- Debe soportar al menos 100 usuarios concurrentes
- Los passwords deben estar encriptados en la base de datos
- Debe implementar rate limiting (máximo 5 intentos por minuto)
- Debe registrar todos los intentos de login en logs de auditoría

Para el carrito de compras:
- Debe sincronizarse en tiempo real con el inventario
- Debe mantener el carrito por 7 días para usuarios no autenticados
- Los cálculos de precios deben ser precisos hasta 2 decimales
- Debe soportar múltiples monedas
- Debe permitir guardar el carrito para usuarios autenticados

Para el registro de usuarios:
- El email de verificación debe enviarse en menos de 1 minuto
- La contraseña debe tener: mínimo 8 caracteres, 1 mayúscula, 1 número, 1 carácter especial
- Debe cumplir con GDPR y protección de datos personales
- Debe implementar CAPTCHA para prevenir bots
- Debe permitir registro social (Google, Facebook)


4. ESCENARIOS DE PRUEBA ADICIONALES
====================================

Feature: Búsqueda de productos
  Scenario: Búsqueda con resultados
    Given que estoy en la página principal
    When ingreso "laptop" en el campo de búsqueda
    And presiono Enter
    Then debo ver una lista de productos relacionados con "laptop"
    And cada resultado debe contener la palabra "laptop"
    And los resultados deben estar ordenados por relevancia

  Scenario: Búsqueda sin resultados
    Given que estoy en la página principal
    When ingreso "xyzabc123" en el campo de búsqueda
    Then debo ver el mensaje "No se encontraron resultados"
    And debo ver sugerencias de productos populares

Feature: Proceso de pago
  Scenario: Checkout exitoso con tarjeta
    Given que tengo productos en mi carrito
    And estoy en la página de checkout
    When ingreso los datos de envío válidos
    And selecciono el método de pago "Tarjeta de Crédito"
    And ingreso los datos de la tarjeta válida
    And hago clic en "Confirmar Compra"
    Then debo ver el mensaje "Compra realizada exitosamente"
    And debo recibir un email con el número de orden
    And el carrito debe quedar vacío
    And mi pedido debe aparecer en "Mis Órdenes"

