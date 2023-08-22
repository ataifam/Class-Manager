function toggleEditSection(id) {
    let category;
    if ((category = document.getElementById(id)) != null) {
      if (category.style.display == "none") {
        category.style.display = "block";
        document.querySelector("#start_" + id).style.display = "none";
      } else {
        category.style.display = "none";
        document.querySelector("#start_" + id).style.display = "block";
      }
    }
}

  function showPrice(value) {
    if(value == 1){
      document.querySelector("#price").innerHTML = "$30,000"
    } else if (value == 2){
      document.querySelector("#price").innerHTML = "$40,000"
    } else if (value == 3){
      document.querySelector("#price").innerHTML = "$60,000"
    } else if (value == 4){
      document.querySelector("#price").innerHTML = "$80,000"
    } else if (value == 5){
      document.querySelector("#price").innerHTML = "$100,000"
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".skill_toggler").forEach((el) => {
        el.onchange = (el) => {
          showPrice(el.target.value);
        };
      });

    document.querySelectorAll(".toggler").forEach((el) => {
      el.onclick = (el) => {
        toggleEditSection("create_" + el.target.id);
      };
      });

      var prev = document.querySelector("#all");
    document.getElementById("filter").onchange = (el) => {
      prev.style.display = "none";
      prev = document.getElementById(el.target.value);
      prev.style.display = "block";
    };
    

    document.querySelector("#filter1").onchange = (el) => {
      document.querySelector("#filter1").submit();
    };
  });

  