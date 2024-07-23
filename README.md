# personSearchRut
Consulta de datos por Rut de personas chilenas.  

## Consulta por rut
Para consultar por el rut de una persona basta con consultar a la API de la siguiente forma:

    <url-api>/consulta?rut=12345678-9

con el rut en formato sin puntos y con guion **(ejemplo: 12345678-9)**.

## Respuesta de API
#### Respuesta exitósa
En caso de que se agregue un rut en los parámetros y este sea un rut válido la respuesta será de la siguiente forma: 

```
{
  "status": 200,
  "error": null,
  "nombre": "Perez Martinez Juan Carlos",
  "rut": "12.345.678-9",
  "sexo": "VAR",
  "direccion": "La Moneda 123",
  "ciudad/comuna": "Santiago Centro",
  "actividades": [
    {
      "nombre": "OTRAS ACTIVIDADES DE SERVICIOS PERSONALES N.C.P.",
      "codigo": 96025,
      "categoria": "Segunda",
      "afecta IVA": false,
      "fecha": "19-12-1998"
    }
  ]
}
