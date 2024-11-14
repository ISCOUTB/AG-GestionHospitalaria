
const grande = document.querySelector('.grande');
const punto  = document.querySelectorAll('.punto');

// Cuando se clickee un punto:
    // identificar la posición del punto translate X al grande
    // Quitar la case activo de todos los puntos
    // Añadir clase activo al punto seleccionado

punto.forEach(( cadaPunto, i ) => {
    punto[i].addEventListener('click', () => {

        let position = i
        let operation = position * -50

        grande.style.transform = `translateX(${operation}%)`
        punto.forEach((cadaPunto, i) =>{
            punto[i].classList.remove('activo')
        })
        punto[i].classList.add('activo')
    })

})
