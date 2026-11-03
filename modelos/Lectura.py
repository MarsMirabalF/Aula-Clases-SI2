from pathlib import Path
from shutil import copy2
from uuid import uuid4

import pymupdf
from firebase_admin import db


class Lectura:
    def __init__(self, carpetaProyecto=None):
        self.carpetaProyecto = Path(carpetaProyecto or Path(__file__).resolve().parent.parent).resolve()
        self.carpetaLecturas = self.carpetaProyecto / "Archivos" / "Lecturas"

    def agregarLectura(self, titulo, rutaPdf):
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("Escribe el título de la lectura.")
        archivoOriginal = Path(rutaPdf)
        if not archivoOriginal.is_file():
            raise FileNotFoundError("No se encuentra el archivo PDF seleccionado.")
        if archivoOriginal.suffix.lower() != ".pdf":
            raise ValueError("Selecciona un archivo con extensión .pdf.")
        try:
            with pymupdf.open(archivoOriginal) as documento:
                if not documento.is_pdf or documento.needs_pass or documento.page_count == 0:
                    raise ValueError("Selecciona un PDF válido, con páginas y sin contraseña.")
        except RuntimeError as error:
            raise ValueError("No se puede leer el PDF. Comprueba que el archivo no esté dañado.") from error

        if not self.carpetaLecturas.resolve().is_relative_to(self.carpetaProyecto):
            raise ValueError("La carpeta de lecturas debe estar dentro del proyecto.")
        self.carpetaLecturas.mkdir(parents=True, exist_ok=True)
        idLectura = uuid4().hex
        rutaRelativa = Path("Archivos") / "Lecturas" / (idLectura + ".pdf")
        archivoCopia = self.carpetaProyecto / rutaRelativa
        registro = {"titulo": titulo.strip(), "rutaArchivo": rutaRelativa.as_posix()}
        archivoCopia.touch(exist_ok=False)
        try:
            copy2(archivoOriginal, archivoCopia)
            db.reference("lecturas/" + idLectura).set(registro)
        except Exception:
            # Si falla el guardado, se retira solo la copia de esta importación.
            try:
                archivoCopia.unlink(missing_ok=True)
            except OSError:
                pass
            raise
        return {"id": idLectura, **registro}

    def listarLecturas(self):
        registros = db.reference("lecturas").get() or {}
        lecturas = [{**registro, "id": idLectura}
                    for idLectura, registro in registros.items()]
        return sorted(lecturas, key=lambda lectura: (lectura["titulo"].casefold(),
                                                     lectura["titulo"], lectura["id"]))

    def obtenerRutaPdf(self, idLectura):
        lectura = (db.reference("lecturas").get() or {}).get(idLectura)
        if lectura is None:
            raise ValueError("La lectura seleccionada no existe.")
        archivoPdf = (self.carpetaProyecto / lectura["rutaArchivo"]).resolve()
        if not archivoPdf.is_relative_to(self.carpetaLecturas) or archivoPdf.suffix.lower() != ".pdf":
            raise ValueError("El PDF debe estar dentro de Archivos/Lecturas.")
        if not archivoPdf.is_file():
            raise FileNotFoundError("No se encuentra el PDF guardado de esta lectura.")
        return archivoPdf
