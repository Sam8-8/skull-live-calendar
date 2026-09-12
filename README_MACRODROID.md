# Fondo Live Calendar + calavera para MacroDroid

## Qué hace

Genera `wallpaper.png` en formato vertical 1080×2400. El mes actual aparece grande y tenue detrás de la calavera; los días anteriores usan blanco hueso, el día actual terracota apagado y los días futuros gris verdoso.

## Opción recomendada: GitHub Actions + MacroDroid

### 1. Crear el repositorio

1. En GitHub, crea un repositorio nuevo, por ejemplo `skull-live-calendar`.
2. Si quieres que MacroDroid descargue el archivo sin iniciar sesión, el repositorio y el archivo deben ser públicos.
3. Sube al repositorio estos archivos y la imagen original de la calavera:
   - `generate_skull_calendar.py`
   - `a73878054e629d404eff3240bf3483d1.jpg`
   - `.github/workflows/update-wallpaper.yml`

### 2. Activar la actualización diaria

En GitHub entra en **Actions**, abre el flujo **Update wallpaper** y pulsa **Enable workflow** si GitHub lo solicita. El flujo se ejecuta a las 03:00 UTC, que corresponde a las 00:00:05 aproximadamente en la zona horaria de Punta Arenas durante el horario UTC−3.

También puedes pulsar **Run workflow** una vez para crear inmediatamente la primera imagen.

### 3. URL que debe usar MacroDroid

Después de la primera ejecución, cambia la URL de la acción HTTP de tu macro por:

```text
https://raw.githubusercontent.com/TU_USUARIO/skull-live-calendar/main/wallpaper.png?t={timestamp}
```

Sustituye `TU_USUARIO` por tu usuario real de GitHub. Si MacroDroid no acepta `{timestamp}`, utiliza una variable de MacroDroid que cambie cada día o deja la URL sin el parámetro `?t=...`.

La URL sin caché queda así:

```text
https://raw.githubusercontent.com/TU_USUARIO/skull-live-calendar/main/wallpaper.png
```

### 4. Mantener las acciones actuales

No cambies el disparador de las 00:00:05 ni la acción **Establecer fondo de pantalla**. Solo sustituye la URL de descarga. Conserva el mismo nombre de archivo `life.png` si el macro ya lo usa.

## Estructura final del repositorio

```text
skull-live-calendar/
├── .github/
│   └── workflows/
│       └── update-wallpaper.yml
├── a73878054e629d404eff3240bf3483d1.jpg
├── generate_skull_calendar.py
└── wallpaper.png
```

## Nota sobre la hora

El flujo de GitHub actualiza la imagen alrededor de medianoche. MacroDroid vuelve a descargarla a las 00:00:05. Si el teléfono descarga la versión anterior por caché, añade el parámetro `?t=` con una variable cambiante de MacroDroid.

## Alternativa

Si no quieres hacer público un repositorio, necesitarás un servidor propio o un almacenamiento público con una URL de descarga directa. Google Drive normalmente no es ideal para este macro porque sus enlaces suelen abrir una página intermedia en lugar de entregar directamente el PNG.
