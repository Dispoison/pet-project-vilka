const popupLinks = document.querySelectorAll('.popup-link');
const body = document.querySelector('body');

let unlock = true;

const timeout = 250;

if (popupLinks.length > 0){
    for (let index = 0; index < popupLinks.length; index++) {
        const popupLink = popupLinks[index];
        popupLink.addEventListener('click', function (e){
           const popupName = popupLink.getAttribute('href').replace('#', '');
           const currentPopup = document.getElementById(popupName);
           popupOpen(currentPopup);
           e.preventDefault();
        });
    }
}

function popupOpen(currentPopup) {
    if (currentPopup && unlock){
        const popupActive = document.querySelector('.popup.open');
        if (popupActive){
            popupClose(popupActive, false);
        }
        else {
            unlock = false;
            setTimeout(function (){
                unlock = true;
            }, timeout);
        }
        currentPopup.classList.add('open');
        currentPopup.addEventListener('click', function (e) {
            if (!e.target.closest('.popup__content')) {
                popupClose(e.target.closest('.popup'));
            }
        });
    }
}

function popupClose(popupActive, doUnlock = true) {
    if (unlock){
        popupActive.classList.remove('open');
        if (doUnlock) {
            unlock = false;
            setTimeout(function (){
                unlock = true;
            }, timeout);
        }
    }
}
