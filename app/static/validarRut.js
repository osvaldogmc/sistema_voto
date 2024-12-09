const $formRut = document.getElementById('formRut');
const $txtRut = document.getElementById('txtRut');

(function () {
    $formRut.addEventListener('submit', function (e) {
        let rut = String($txtRut.value).trim();
        if (rut.length === 0) {
            alert("El rut no puede ir vacio");
            e.preventDefault();
        }
    });
})();


function validarRut() {
    const rut = document.getElementById("txtRut").value;

    // Verificar si el RUT tiene el formato correcto: XX.XXX.XXX-X
    const rutPattern = /^\d{1,2}(\.\d{3}){2}-[0-9Kk]{1}$/;

    if (!rutPattern.test(rut)) {
        alert("RUT inválido. El formato debe ser XX.XXX.XXX-X");
        return false;
    }

    const rutLimpio = rut.replace(/[.-]/g, ''); // Elimina puntos y guion
    const cuerpo = rutLimpio.slice(0, -1);
    const dv = rutLimpio.slice(-1).toUpperCase();

    if (!/^\d{7,8}[0-9k]$/.test(rutLimpio)) {
        alert("RUT inválido.");
        return false;
    }

    let suma = 0;
    let multiplicador = 2;
    for (let i = cuerpo.length - 1; i >= 0; i--) {
        suma += cuerpo[i] * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }

    const dvCalculado = 11 - (suma % 11);
    const dvCorrecto = dvCalculado === 11 ? '0' : dvCalculado === 10 ? 'K' : dvCalculado.toString();

    if (dv !== dvCorrecto) {
        alert("RUT inválido.");
        return false;
    }

    return true;

}
