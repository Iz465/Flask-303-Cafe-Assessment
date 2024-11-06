

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



  else if (checkout_length.length == 2 && answer.id == "card_expiry"  && answer.value[2] != '/') {
    answer.value += '/';
  }
  else if (checkout_length.length == 4 && answer.id == 'card_number') {
    answer.value += ' ';
  }
  else if (checkout_length.length == 9 && answer.id == 'card_number') {
    answer.value += ' ';
  }
  else if (checkout_length.length == 14 && answer.id == 'card_number') {
    answer.value += ' ';
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


function product_quantity(div, change) {

  const quantityElement = div.querySelector(".specific_item_quantity");
  const div_price = div.querySelector(".specific_item_price");
  const original_price = div.querySelector(".original_price");
  const total_price = document.querySelector('.total_price_class')
  const total_amount = document.querySelector('.total_amount_class')

  if (div == ".specific_item_div") {
    
  }

  let currentQuantity = parseInt(quantityElement.textContent) || 0;

  let currentPrice = parseFloat(div_price.textContent.replace(/[^0-9.-]+/g, "")); // Removes the dollar sign as that is not a number
  let new_sum_price = parseFloat(total_price.textContent.replace(/[^0-9.-]+/g, ""));
  let final_amount = parseInt(total_amount.textContent.replace(/[^0-9.-]+/g, ""));
  let first_price = parseFloat(original_price.textContent);
  
 

  currentQuantity += change;


  if (currentQuantity < 0) { // This will make it so the quantity can't go below zero.
      currentQuantity = 0; 
  }

 
  quantityElement.textContent = currentQuantity;

  if  (change == 1) {
    currentPrice += first_price;
    new_sum_price += first_price;
    final_amount += 1;
  }
  else if (change == -1) {
    currentPrice -= first_price;
    new_sum_price -= first_price;
    final_amount -= 1;
  }

  if (currentPrice < 0) {
    currentPrice = 0;
    new_sum_price = 0;
    final_amount = 0;
  }
  
  div_price.textContent = `$${currentPrice.toFixed(2)}`; // Brings back the dollar sign i removed earlier
  total_price.textContent = `Total Price: $${new_sum_price.toFixed(2)}`;
  total_amount.textContent = `Amount of items in cart: ${final_amount}`;

}


function delete_item(div) {
  const total_amount = document.querySelector('.total_amount_class')
  const total_price = document.querySelector('.total_price_class')
  const quantityElement = div.querySelector(".specific_item_quantity");
  const div_price = div.querySelector(".specific_item_price");
  let currentQuantity = parseInt(quantityElement.textContent) || 0;
  let specific_price = parseFloat(div_price.textContent.replace(/[^0-9.-]+/g, ""));
  let amount = parseInt(total_amount.textContent.replace(/[^0-9.-]+/g, ""));
  let price = parseFloat(total_price.textContent.replace(/[^0-9.-]+/g, ""));
  amount -= currentQuantity;
  price -= specific_price;
  total_amount.textContent = amount;
  total_price.textContent = price.toFixed(2);
  remove = div.querySelector(".specific_item_div");
  remove.remove();
  product_quantity(remove);
}



