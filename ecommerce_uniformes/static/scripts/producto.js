
document.addEventListener('DOMContentLoaded', function () {
    const colorButtons = document.querySelectorAll('.color-button');
    const tallaButtons = document.querySelectorAll('.talla-button');
    const thumbnailSwitcher = document.querySelectorAll('.thumbnail-switcher');
    const precioElemento = document.getElementById('precio-producto');
    const imagenElemento = document.getElementById('imagen-producto');
    const stockElemento = document.getElementById('estado-stock');
    const btnAnadir = document.getElementById('btn-anadir');
    const descripcionColor = document.getElementById('descripcion-color');
    const descripcionTalla = document.getElementById('descripcion-talla');
    const skuPlaceholder = document.getElementById('sku-placeholder');
    console.log(variantes)

    let selectedColorId = null;
    let selectedTallaId = null;

    function actualizarProducto() {
        const variante = variantes.find(v =>
            v.color_id == selectedColorId && v.talla_id == selectedTallaId
        );

        if (variante) {
            precioElemento.innerText = `$${variante.precio} MXN`;
            imagenElemento.src = variante.imagen;
            stockElemento.innerText = (
                variante.stock > 10 ? "En stock" :
                    variante.stock > 0 ? "Pocas unidades" :
                        "Agotado"
            );
            stockElemento.classList.remove("text-success", "text-warning", "text-danger");
            stockElemento.classList.add(variante.stock > 10 ? "text-success" :
                variante.stock > 0 ? "text-warning" : "text-danger")
            btnAnadir.disabled = variante.stock === 0;
            descripcionColor.innerText = `Color: ${variante.color_nombre}`;
            descripcionTalla.innerText = `Talla: ${variante.talla_nombre}`;
            skuPlaceholder.innerText = variante.sku;
        } else {
            // Si aún no se ha seleccionado una talla válida
            precioElemento.innerText = "$ Precio MXN";
            stockElemento.innerText = "";
            btnAnadir.disabled = true;
        }
    }

    colorButtons.forEach(button => {
        button.addEventListener('click', function () {
            selectedColorId = this.getAttribute('data-color');

            // Mostrar solo las tallas del color seleccionado
            document.querySelectorAll('.tallas-color').forEach(div => {
                div.style.display = 'none';
            });

            const target = document.querySelector(`.tallas-color[data-color="${selectedColorId}"]`);
            if (target) {
                target.style.display = 'block';

                // Simular clic en la primera talla disponible del color
                const firstTalla = target.querySelector('.talla-button');
                if (firstTalla) {
                    firstTalla.click();
                }
            }
        });
    });

    tallaButtons.forEach(button => {
        button.addEventListener('click', function () {
            selectedTallaId = this.getAttribute('data-talla');
            actualizarProducto();
        });
    });

    thumbnailSwitcher.forEach(button => {
        button.addEventListener('click', function () {
            selectedColorId = this.getAttribute('data-color');
            selectedColorButton = document.querySelector(`.color-button[data-color="${selectedColorId}"]`);
            selectedColorButton.click();
        });
    });

    // Disparo automático del primer color al cargar
    if (colorButtons.length > 0) {
        colorButtons[0].click();
    }

});