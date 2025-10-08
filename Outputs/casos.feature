Feature: Validación de transferencia interbancaria nacional

  Scenario: Acceso al flujo de transferencias
    Given el feature flag LD_TRANSFER_INTERBANCARIA está activado
    When el cliente accede al menú
    Then el menú “Transferencias” es visible

  Scenario: Acceso al flujo de transferencias sin feature flag
    Given el feature flag LD_TRANSFER_INTERBANCARIA está desactivado
    When el cliente accede al menú
    Then el menú “Transferencias” no es visible

  Scenario: Mostrar cuentas destino registradas
    Given el cliente tiene cuentas destino registradas
    When el cliente accede al flujo de transferencias
    Then se muestran las cuentas destino registradas

  Scenario: Mensaje si no hay cuentas registradas
    Given el cliente no tiene cuentas destino registradas
    When el cliente accede al flujo de transferencias
    Then se muestra el mensaje “No tienes cuentas guardadas. Agrega una nueva cuenta destino.”

  Scenario: Transferencia con monto válido
    Given el cliente ingresa un monto de $500.000
    When el cliente revisa el resumen de la transferencia
    Then se muestra el resumen de la transferencia

  Scenario: Transferencia con monto que excede el límite
    Given el cliente ingresa un monto de $1.500.000
    When el cliente intenta revisar el resumen de la transferencia
    Then se muestra el mensaje “El monto supera el límite permitido.”

  Scenario: Confirmar transferencia exitosa
    Given el cliente tiene datos de transferencia válidos
    When el cliente confirma la transferencia
    Then se muestra el mensaje “Tu transferencia fue realizada con éxito.”

  Scenario: Confirmar transferencia con error técnico
    Given el cliente tiene datos de transferencia válidos
    And ocurre un error en el backend
    When el cliente confirma la transferencia
    Then se muestra el mensaje “No pudimos completar tu transferencia. Intenta más tarde.”

  Scenario: Respuesta del backend con estado SUCCESS
    Given el cliente realiza una transferencia exitosa
    When el backend responde
    Then el estado de la respuesta es SUCCESS

  Scenario: Respuesta del backend con estado ERROR
    Given el cliente realiza una transferencia fallida
    When el backend responde
    Then el estado de la respuesta es ERROR
```

Esta matriz de pruebas y los casos Gherkin cubren los criterios de aceptación y aseguran que se validen todos los aspectos del flujo de transferencia interbancaria nacional desde la App Móvil.