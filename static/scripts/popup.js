function openPopup(button) {
  document.getElementById("popup").style.display = "block";
  const rewardName = button.getAttribute("data-reward-name");
  document.querySelector("#popup h3").textContent = rewardName;
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
}
