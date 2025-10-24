Feature: Registro de usuario

  Scenario: Registro exitoso
    Given el correo "usuario@ejemplo.com"
    And el nombre "Juan"
    And la contraseña "Contraseña123"
    When el usuario intenta registrarse
    Then muestra "Usuario registrado correctamente"

  Scenario: Registro fallido - correo ya existe
    Given el correo "usuario@ejemplo.com"
    And el nombre "Juan"
    And la contraseña "Contraseña123"
    When el usuario intenta registrarse
    Then muestra "El correo ya está en uso"

  Scenario: Registro fallido - contraseña débil
    Given el correo "nuevo@ejemplo.com"
    And el nombre "Ana"
    And la contraseña "123"
    When el usuario intenta registrarse
    Then muestra "La contraseña es demasiado débil"

  Scenario: Registro fallido - datos incompletos
    Given el correo ""
    And el nombre "Juan"
    And la contraseña "Contraseña123"
    When el usuario intenta registrarse
    Then muestra "Todos los campos son obligatorios"

  Scenario: Registro fallido - formato de correo inválido
    Given el correo "usuario@ejemplo"
    And el nombre "Juan"
    And la contraseña "Contraseña123"
    When el usuario intenta registrarse
    Then muestra "Formato de correo inválido"
```

Estos casos de prueba y escenarios Gherkin cubren las funcionalidades básicas y las validaciones necesarias para el registro de un nuevo usuario en la aplicación.