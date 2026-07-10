
document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.flash').forEach(flash => {

        requestAnimationFrame(() => {
            flash.classList.add('flash-visible');
        });

        const timer = setTimeout(() => {
            removeFlash(flash);
        }, 4000);

        flash.addEventListener('click', () => {
            clearTimeout(timer);
            removeFlash(flash);
        });

    });

    function removeFlash(flash){

        flash.classList.remove('flash-visible');
        flash.classList.add('flash-hide');

        flash.addEventListener('transitionend', () => {

            flash.remove();

        }, { once:true });

    }

});
