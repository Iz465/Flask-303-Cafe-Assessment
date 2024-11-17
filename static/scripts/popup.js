function openPopup(button) {
  document.getElementById("popup").style.visibility = "visible";
  const rewardName = button.getAttribute("data-reward-name");
  const points = button.getAttribute("data-points");
  const id = button.getAttribute("data-id");

  document.getElementById("reward_points_input").value = points;
  document.getElementById("reward_id_input").value = id;  
  document.querySelector("#popup h3").textContent = rewardName;
  document.getElementById("rewardTypeInput").value = rewardName;
 // document.querySelectorAll("#popup input").values = rewardName;
  
}
//<input type="submit" name="reward_points" id="reward_points_input" value="asdgag">
function closePopup() {
  document.getElementById("popup").style.visibility = "hidden";
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

const h3Elements = document.querySelectorAll("#popup h3");
h3Elements.forEach(h3 => {
    h3.textContent = rewardName;
});



//  const reward_types = document.querySelectorAll("#popup input");
 // reward_types.forEach(reward => {
  //  reward.value = rewardName;
 //   })