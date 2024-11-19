

function open_favourite() {
const open_check = document.getElementById('favourite-popup-id');

if (open_check.style.visibility == 'visible') {
  open_check.style.visibility = 'hidden';
  open_check.style.marginLeft= '-45%';
}
else {
  open_check.style.visibility= 'visible';
  open_check.style.marginLeft= '0%';
}



}