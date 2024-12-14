(function () {

    const btnEditar = document.querySelectorAll(".btnEditar");
    
    btnEditar.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('No se puede editar candidato ya que tiene votos asociados');
            if (!confirmacion) {
                e.preventDefault();
            }
            
            return true;
        });
    });
})();