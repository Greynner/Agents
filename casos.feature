Feature: Validar login en aplicación móvil

  Scenario: Usuario válido accede con credenciales correctas
    Given un usuario registrado con credenciales válidas
    When introduce usuario y contraseña válidos
    Then debe acceder exitosamente a la aplicación

  Scenario: Usuario inválido intenta acceder
    Given un usuario no registrado
    When introduce credenciales inválidas
    Then debe mostrarse un mensaje de error "Credenciales inválidas"

  Scenario: Usuario bloqueado después de 3 intentos fallidos
    Given un usuario registrado
    When introduce contraseña incorrecta tres veces
    Then el usuario debe ser bloqueado
    And debe mostrarse un mensaje "Acceso bloqueado"

  Scenario: Intento de acceso después de ser bloqueado
    Given un usuario bloqueado
    When intenta acceder con credenciales válidas
    Then debe mostrarse un mensaje "Acceso bloqueado"