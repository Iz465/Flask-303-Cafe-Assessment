function openPopup(button) {
  document.getElementById("popup").style.display = "block";
  const rewardName = button.getAttribute("data-reward-name");
  document.querySelector("#popup h3").textContent = rewardName;
  
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
}

function tablePopup(table_div) {
  const admin_tables = document.querySelectorAll(".admin_table");
  const current_table =  document.getElementById(table_div)
  const changing_table = document.querySelectorAll('.changing_item');
  
  changing_table.forEach(div => {
    div.style.display = 'none';
  });

  admin_tables.forEach(table => { // This will check every table that has admin_table class and if they are open and not the current table that was clicked then they will be closed. this will make it so only one table is opened at once.
    if (table != current_table || table.style.display == '') {
      table.style.display = 'none';
    }

  });

  if ( current_table) 
    {
      current_table.style.display =  current_table.style.display === 'none' ? 'block' : "none"; // If hidden will open, if open will hide the table.
    }

}