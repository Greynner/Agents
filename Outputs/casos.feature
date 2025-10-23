Feature: Registro de usuario

  Scenario: Registro exitoso
    Given el correo "usuario@ejemplo.com"
    And el nombre "Juan"
    And la contraseña "Contraseña123"
    When el usuario intenta registrarse
    Then muestra "Usuario registrado correctamente"

  Scenario: Registro fallido - Correo existente
    Given el correo "usuario@ejemplo.com"
    And el nombre "Pedro"
    And la contraseña "Contraseña456"
    When el usuario intenta registrarse
    Then muestra "El correo ya está registrado"

  Scenario: Registro fallido - Contraseña débil
    Given el correo "nuevo@ejemplo.com"
    And el nombre "Ana"
    And la contraseña "123"
    When el usuario intenta registrarse
    Then muestra "La contraseña debe tener al menos 8 caracteres"

  Scenario: Registro fallido - Campos vacíos
    Given el correo ""
    And el nombre ""
    And la contraseña ""
    When el usuario intenta registrarse
    Then muestra "Todos los campos son obligatorios"

  Scenario: Registro fallido - Formato de correo inválido
    Given el correo "usuarioejemplo.com"
    And el nombre "Luis"
    And la contraseña "Contraseña789"
    When el usuario intenta registrarse
    Then muestra "Formato de correo inválido"
```

Estos casos de prueba y escenarios Gherkin cubren las principales funcionalidades y validaciones requeridas para el registro de un nuevo usuario en el sistema.