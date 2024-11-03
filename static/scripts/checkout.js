

function validating_checkout(answer, checkout_marker) {
  const checkout_length = answer.value;  
  const length_required = answer.getAttribute('checkout_input_length'); 
  const length_checker = new RegExp(`^\\d{0,${length_required}}$`); 


  if (checkout_length.length == length_required && length_checker.test(length_required)) {
    checkout_marker.textContent = "✅";
  } 
  else if (checkout_length.length == 0) {
    checkout_marker.textContent = ""; 
  }
  else if (checkout_length.length == 2 && answer.id == "card_expiry") {
    answer.value += '/';
  }
  else {
    checkout_marker.textContent = "❌"; 
  }
}

const card_number_input = document.getElementById("card_number");
const card_number_answer = document.getElementById("card_number_validation");


card_number_input.addEventListener("input", function() {
  validating_checkout(card_number_input, card_number_answer );
});

const card_expiry_input = document.getElementById("card_expiry");
const card_expiry_answer = document.getElementById("card_expiry_validation");

card_expiry_input.addEventListener("input", function() {
  validating_checkout(card_expiry_input, card_expiry_answer)
});

const cvc_input = document.getElementById("cvc");
const cvc_answer = document.getElementById("cvc_validation");


cvc_input.addEventListener("input", function() {
  validating_checkout(cvc_input,  cvc_answer);
});