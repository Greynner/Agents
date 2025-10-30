Feature: Validar que un usuario pueda iniciar sesión correctamente con credenciales válidas

  Scenario: Usuario válido accede con credenciales correctas
    Given un usuario registrado con correo "usuario@ejemplo.com" y contraseña "contraseñaSegura"
    When el usuario abre la aplicación web
    And selecciona la opción "Iniciar sesión"
    And introduce su correo electrónico "usuario@ejemplo.com" y contraseña "contraseñaSegura"
    And presiona el botón "Ingresar"
    Then debe acceder exitosamente al sistema y ser redirigido a la página principal

  Scenario: Usuario intenta iniciar sesión con correo incorrecto
    Given un usuario registrado con correo "usuario@ejemplo.com" y contraseña "contraseñaSegura"
    When el usuario abre la aplicación web
    And selecciona la opción "Iniciar sesión"
    And introduce su correo electrónico "correoIncorrecto@ejemplo.com" y contraseña "contraseñaSegura"
    And presiona el botón "Ingresar"
    Then debe ver un mensaje de error indicando que las credenciales son incorrectas

  Scenario: Usuario intenta iniciar sesión con contraseña incorrecta
    Given un usuario registrado con correo "usuario@ejemplo.com" y contraseña "contraseñaSegura"
    When el usuario abre la aplicación web
    And selecciona la opción "Iniciar sesión"
    And introduce su correo electrónico "usuario@ejemplo.com" y contraseña "contraseñaIncorrecta"
    And presiona el botón "Ingresar"
    Then debe ver un mensaje de error indicando que las credenciales son incorrectas

  Scenario: Usuario intenta iniciar sesión dejando campos vacíos
    Given un usuario registrado con correo "usuario@ejemplo.com" y contraseña "contraseñaSegura"
    When el usuario abre la aplicación web
    And selecciona la opción "Iniciar sesión"
    And introduce su correo electrónico vacío y contraseña vacía
    And presiona el botón "Ingresar"
    Then debe ver un mensaje de error indicando que los campos son obligatorios
```