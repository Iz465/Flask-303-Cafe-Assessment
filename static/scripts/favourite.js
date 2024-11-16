

function open_favourite() {
const open_check = document.getElementById('favourite-popup-id');

if (open_check.style.visibility == 'visible') {
  open_check.style.visibility = 'hidden';
}
else {
  open_check.style.visibility= 'visible';
}
}