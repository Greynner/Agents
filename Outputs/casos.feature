Feature: Validación de login

  Scenario: Login exitoso
    Given el usuario ingresa un correo electrónico "usuario@ejemplo.com"
    And el usuario ingresa una contraseña "contraseña123"
    When el usuario presiona el botón "Iniciar sesión"
    Then el usuario es redirigido a "/dashboard"
    And muestra "Bienvenido/a nuevamente."

  Scenario: Login fallido - campos vacíos
    Given el usuario no ingresa un correo electrónico
    And el usuario no ingresa una contraseña
    When el usuario presiona el botón "Iniciar sesión"
    Then muestra "Por favor, completa todos los campos."

  Scenario: Login fallido - correo inválido
    Given el usuario ingresa un correo electrónico "usuarioejemplo.com"
    And el usuario ingresa una contraseña "contraseña123"
    When el usuario presiona el botón "Iniciar sesión"
    Then muestra "Correo electrónico inválido."

  Scenario: Login fallido - credenciales incorrectas
    Given el usuario ingresa un correo electrónico "usuario@ejemplo.com"
    And el usuario ingresa una contraseña "incorrecta123"
    When el usuario presiona el botón "Iniciar sesión"
    Then muestra "Credenciales incorrectas."
```

### Notas
- Asegúrate de que el manejo de errores y la validación de campos se realicen sin recargar la página, utilizando JavaScript o React.
- Los mensajes de error deben ser claros y visibles para el usuario.