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
