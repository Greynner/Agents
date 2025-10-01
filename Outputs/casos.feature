Feature: Validar flujo de inicio de sesión en la banca digital

  Scenario: Usuario válido accede con credenciales correctas
    Given un usuario registrado con credenciales válidas
    When introduce usuario y contraseña correctos
    Then debe acceder exitosamente al sistema

  Scenario: Usuario inválido intenta acceder
    Given un usuario no registrado
    When introduce usuario y contraseña incorrectos
    Then debe mostrar un mensaje de error “Credenciales incorrectas”

  Scenario: Usuario válido bloqueado tras 3 intentos fallidos
    Given un usuario registrado
    When introduce usuario y contraseña incorrectos tres veces consecutivas
    Then la cuenta debe estar bloqueada
    And debe mostrar un mensaje de error

  Scenario: Registro de último intento de login
    Given un usuario registrado
    When introduce usuario y contraseña incorrectos
    Then el sistema debe registrar la fecha y hora del último intento de login