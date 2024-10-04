
let carouselbackgrounds = document.querySelectorAll(".carousel-images")

let imageIndex = 0;

function changeImage() {

  carouselbackgrounds[imageIndex].classList.remove("showing")

  imageIndex++;

  if (imageIndex >= carouselbackgrounds.length) {
    imageIndex = 0;
  }

  carouselbackgrounds[imageIndex].classList.add("showing");

}

setInterval(changeImage, 4000);