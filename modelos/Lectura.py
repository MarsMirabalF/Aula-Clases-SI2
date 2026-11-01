from pathlib import Path
from shutil import copy2
from uuid import uuid4

from firebase_admin import db


def validarId(identificador, nombre):
    if (not isinstance(identificador, str) or not identificador.strip()
            or any(caracter in identificador for caracter in ".#$[]/\\")
            or any(ord(caracter) < 32 or ord(caracter) == 127 for caracter in identificador)):
        raise ValueError("El identificador no es válido. Selecciona " + nombre + ".")
    return identificador


class Lectura:
    def __init__(self, carpetaProyecto=None):
        self.carpetaProyecto = (Path(carpetaProyecto).resolve() if carpetaProyecto is not None
                                else Path(__file__).resolve().parent.parent)
        self.carpetaLecturas = self.carpetaProyecto / "Archivos" / "Lecturas"

    def agregarLectura(self, titulo, rutaPdf):
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("Escribe el título de la lectura.")
        try:
            archivoOriginal = Path(rutaPdf).resolve()
        except (TypeError, ValueError) as error:
            raise ValueError("Selecciona un archivo PDF válido.") from error
        if not archivoOriginal.is_file():
            raise FileNotFoundError("No se encuentra el archivo PDF seleccionado.")
        if archivoOriginal.suffix.lower() != ".pdf":
            raise ValueError("Selecciona un archivo con extensión .pdf.")
        self.validarPdf(archivoOriginal)

        carpetaDestino = self.carpetaLecturas.resolve()
        if not carpetaDestino.is_relative_to(self.carpetaProyecto):
            raise ValueError("La carpeta de lecturas debe estar dentro del proyecto.")
        carpetaDestino.mkdir(parents=True, exist_ok=True)
        idLectura = uuid4().hex
        rutaRelativa = Path("Archivos") / "Lecturas" / (idLectura + ".pdf")
        archivoCopia = carpetaDestino / (idLectura + ".pdf")
        registro = {"titulo": titulo.strip(), "rutaArchivo": rutaRelativa.as_posix()}
        try:
            copy2(archivoOriginal, archivoCopia)
            db.reference("lecturas/" + idLectura).set(registro)
        except Exception:
            # Solo se retira la copia de esta importación; el original se conserva.
            try:
                archivoCopia.unlink(missing_ok=True)
            except OSError:
                pass
            raise
        return {"id": idLectura, **registro}

    def validarPdf(self, rutaPdf):
        try:
            import pymupdf
        except ImportError as error:
            raise ValueError("Falta instalar PyMuPDF. Ejecuta: python -m pip install PyMuPDF") from error
        try:
            with pymupdf.open(str(rutaPdf)) as documento:
                if not documento.is_pdf:
                    raise ValueError("El archivo seleccionado no es un PDF válido.")
                if documento.needs_pass or documento.is_encrypted:
                    raise ValueError("El PDF está protegido con contraseña. Usa una copia sin protección.")
                if documento.page_count == 0:
                    raise ValueError("El PDF debe contener al menos una página.")
        except ValueError:
            raise
        except Exception as error:
            raise ValueError("No se puede leer el PDF. Comprueba que el archivo no esté dañado.") from error

    def listarLecturas(self):
        registros = db.reference("lecturas").get() or {}
        lecturas = [{**registro, "id": idLectura}
                    for idLectura, registro in registros.items()]
        return sorted(lecturas, key=lambda lectura: (lectura["titulo"].casefold(),
                                                     lectura["titulo"], lectura["id"]))

    def obtenerLectura(self, idLectura):
        validarId(idLectura, "una lectura")
        registro = db.reference("lecturas/" + idLectura).get()
        return {**registro, "id": idLectura} if registro is not None else None

    def obtenerRutaPdf(self, idLectura):
        lectura = self.obtenerLectura(idLectura)
        if lectura is None:
            raise ValueError("La lectura seleccionada no existe.")
        rutaGuardada = lectura.get("rutaArchivo")
        if not isinstance(rutaGuardada, str) or not rutaGuardada.strip():
            raise ValueError("La lectura no tiene una ruta PDF válida.")
        rutaRelativa = Path(rutaGuardada)
        if rutaRelativa.is_absolute() or rutaRelativa.drive or rutaRelativa.root:
            raise ValueError("La ruta del PDF debe ser relativa al proyecto.")
        archivoPdf = (self.carpetaProyecto / rutaRelativa).resolve()
        carpetaPermitida = self.carpetaLecturas.resolve()
        if (not carpetaPermitida.is_relative_to(self.carpetaProyecto)
                or not archivoPdf.is_relative_to(carpetaPermitida)
                or archivoPdf.suffix.lower() != ".pdf"):
            raise ValueError("El PDF debe estar dentro de Archivos/Lecturas.")
        if not archivoPdf.is_file():
            raise FileNotFoundError("No se encuentra el PDF guardado de esta lectura.")
        return archivoPdf
