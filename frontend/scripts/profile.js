
function cambiarContenido(contenido){
    const contenedor = document.getElementById('contenedor');

    if (contenido==="act_history"){
        contenedor.innerHTML = "<div class = \"act_history\">\n" +
            "                <h1>Actualizar historia clínica</h1>\n" +
            "                <p class=\"parrafo\">Por favor, ingrese el número de documento del paciente y seleccione el archivo de actualización\n" +
            "                    de la historia clínica.</p>\n" +
            "                <div class=\"inputBox\" id=\"user\">\n" +
            "                    <input type=\"text\" placeholder=\"Número de identificación\" required>\n" +
            "                </div>\n" +
            "                <label for=\"archivo\" class=\"boton-archivo\">Seleccionar archivo</label>\n" +
            "                <input type=\"file\" id=\"archivo\" style=\"display: none;\" onchange=\"mostrarNombreArchivo()\">\n" +
            "                <div id=\"nombre-archivo\">Ningún archivo seleccionado</div>\n" +
            "                <button class=\"act\">Actualizar</button>\n" +
            "            </div>"
    }
    else if(contenido==="get_history"){
        contenedor.innerHTML="     <div class = \"act_history\">\n" +
            "                <h1>Obtener historia clínica</h1>\n" +
            "                <p class=\"parrafo\">Por favor, ingrese el número de documento del paciente y seleccione ingresar para descargar\n" +
            "                    automáticamente la última versión de la historia clínica.</p>\n" +
            "                <div class=\"inputBox\" id=\"user\">\n" +
            "                    <input type=\"text\" placeholder=\"Número de identificación\" required>\n" +
            "                </div>\n" +
            "                <button class=\"get\">Última versión</button>\n" +
            "                <button class=\"get\">Histórico de actualizaciones</button>\n" +
            "\n" +
            "\n" +
            "            </div>"
    }
}

function mostrarNombreArchivo() {
    const inputArchivo = document.getElementById("archivo");
    const nombreArchivo = document.getElementById("nombre-archivo");

    // Verifica si hay un archivo seleccionado
    if (inputArchivo.files.length > 0) {
        nombreArchivo.textContent = `Archivo seleccionado: ${inputArchivo.files[0].name}`;
    } else {
        nombreArchivo.textContent = "Ningún archivo seleccionado";
    }
}