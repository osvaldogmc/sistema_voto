(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");
    
    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('No se puede eliminar candidato ya que tiene votos asociados');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
})();