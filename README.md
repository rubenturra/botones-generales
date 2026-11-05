# Botones generales

Complemento de FreeCAD con botones para fabricación que valen para **cualquier
tecnología de corte** (plasma, láser, oxicorte, agua…).

## Botones

| Botón | Dónde | Qué hace |
| --- | --- | --- |
| **Cantidad de piezas** | Barra *Fabricación* de Part Design y Part | Pide un número y lo guarda en cada pieza seleccionada como propiedad **Cantidad** (grupo *Fabricación*). Se guarda con el `.FCStd`. |

[1st Nesting (fork rubenturra, rama `mejoras-ruben`)](https://github.com/rubenturra/1st-Nesting/tree/mejoras-ruben)
lee esa cantidad al añadir la pieza y la actualiza si la cambias en su tabla.

## Instalación

1. *Herramientas → Addon Manager → ⚙ Configuración → Repositorios personalizados*:
   añade `https://github.com/rubenturra/botones-generales` con la rama `main`.
2. Instala **botones-generales** y reinicia FreeCAD.

La barra se crea una sola vez; si la quitas en *Herramientas → Personalizar*,
no vuelve a aparecer.

## Hacer todo

Botón en la barra **Fabricación** (Part Design y Part), al lado de *Ir a 1st Nesting*.
Hace el anidado con 1st Nesting y el mecanizado de plasma con la configuración de la
última vez, sin ventanas intermedias:

1. piezas: las seleccionadas; si no hay selección, la lista de la última vez;
2. chapas, espesores y ajustes: los guardados en 1st Nesting;
3. mecaniza solo los anidados nuevos con las opciones guardadas de *Mecanizar plasma*
   (carpeta, nombre, herramienta, entradas/salidas, retal, simulación);
4. al final, un único resumen con el anidado y el mecanizado.

Necesita 1st Nesting, el banco CAM y *Botones plasma*.
