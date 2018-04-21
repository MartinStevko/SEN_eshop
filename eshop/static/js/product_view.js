var ids = {1:"1", 2:"2", 3:"3"};

function still_same() {
	var seconds = new Date().getTime() / 1000;

	var time = localStorage.getItem("time");

  localStorage.setItem("time", String(seconds));

	if (time == null) {
		time = 0;
	}

	var diff = seconds - time;

	if (diff > 300) {
		return false;
	} else {
		return true;
	}
}

function previous_style() {
	var still = still_same();

	if (still == true) {
		var sec_styles = {1:null, 2:null, 3:null}
	  styles_in = true

		for (i = 1; i < 4; i++) {
	    sec_styles[i] = localStorage.getItem(ids[i]);

	    if (sec_styles[i] == null) {
	      styles_in = false;
	    }
	  }

	  if (styles_in == true) {
	    for (i = 1; i < 4; i++) {
	      var sec = document.getElementById(ids[i]);

	      if (sec.style.display !== sec_styles[i]) {
	        sec.style.display = sec_styles[i];
	      }
	    }
	  } else {
	    for (id in ids) {
	      var sec = document.getElementById(id);

	      if (sec.style.display !== "none") {
	        sec.style.display = "none";
	      }
	    }

	    var sec = document.getElementById("1");
	    sec.style.display = "block";
	  }
	} else {
		show_hide_section("1")
	}
}

function show_hide_section(i) {
	var seconds = new Date().getTime() / 1000;
  localStorage.setItem("time", String(seconds));

  for (id in ids) {
    var sec = document.getElementById(id);

    if (i === id) {
      var k = parseInt(i);
      localStorage.setItem(id, "block");

      if (sec.style.display !== "block") {
        sec.style.display = "block";
      }
    } else {
      localStorage.setItem(id, "none");

      if (sec.style.display !== "none") {
        sec.style.display = "none";
      }
    }
  }
}

function big_image(imgs) {
	var sw = document.getElementsByClassName("container")[0].offsetWidth;

	if (sw > 323) {
		var expandImg = document.getElementById("expandedImg");
    var imgText = document.getElementById("imgtext");

	   expandImg.src = imgs.src;
	   imgText.innerHTML = imgs.alt;
	   expandImg.parentElement.style.display = "block";
	}
}
