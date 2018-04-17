function isNumeric(obj){
    return !isNaN(parseFloat(obj)) && isFinite(obj)
}

function validate1() {
  var fname = document.getElementById('1').value;
  var surname = document.getElementById('2').value;
  var phone = document.getElementById('3').value;

  var demo1 = document.getElementById('demo1');
  var demo2 = document.getElementById('demo2');
  var demo3 = document.getElementById('demo3');

  var valid = true;

  if (fname == "") {
    demo1.innerHTML = "Zadajte svoje prvé meno!";
    valid = false;
  } else {
    demo1.innerHTML = "";
  }

  if (surname == "") {
    demo2.innerHTML = "Zadajte svoje priezvisko!";
    valid = false;
  } else {
    demo2.innerHTML = "";
  }

  if (phone == "") {
    demo3.innerHTML = "Zadajte svoje číslo!";
    valid = false;
  } else {
    var num = phone.substring(1, phone.length);

    var i;
    for (i = 0; i < num.length; i++) {
      if (num.substring(i, i+1) == " ") {
        num = num.substring(0, i) + num.substring(i+1, num.length);
        i = i - 1;
      }
    }

    if ((phone.substring(0,1) != "+") || (isNumeric(num) == false) || (num.length < 12)) {
      demo3.innerHTML = "Číslo musí byť v tvare '+421 123 456 789'!";
      valid = false;
    } else {
      demo3.innerHTML = "";
    }
  }

  if (valid == true) {
    return (true);
  } else {
    return (false);
  }
}

function d1() {
  if (validate1() == true) {
    var hide = document.getElementById('info');
    var show = document.getElementById('get');

    hide.style.display = "none";
    show.style.display = "block";
  }
}

function p2() {
  var hide = document.getElementById('get');
  var show = document.getElementById('info');

  hide.style.display = "none";
  show.style.display = "block";
}

function d2() {
  var manner = document.getElementById('manner').value;

  if (manner == "Personal purchase") {
    var hide = document.getElementById('get');
    var show = document.getElementById('send');

  } else {
    var hide = document.getElementById('get');
    var show = document.getElementById('address');
  }

  hide.style.display = "none";
  show.style.display = "block";
}

function p3() {
  var hide = document.getElementById('address');
  var show = document.getElementById('get');

  hide.style.display = "none";
  show.style.display = "block";
}

function validate3() {
  var street = document.getElementById('4').value;
  var house = document.getElementById('5').value;
  var town = document.getElementById('6').value;
  var pdn = document.getElementById('7').value;

  var demo4 = document.getElementById('demo4');
  var demo5 = document.getElementById('demo5');
  var demo6 = document.getElementById('demo6');
  var demo7 = document.getElementById('demo7');

  var valid = true;

  if (street == "") {
    demo4.innerHTML = "Zadajte ulicu, na ktorej bývate!";
    valid = false;
  } else {
    demo4.innerHTML = "";
  }

  if ((house == "") || (isNumeric(house) == false)) {
    demo5.innerHTML = "Zadajte číslo domu, v ktorom bývate!";
    valid = false;

  } else {
    demo5.innerHTML = "";
  }

  if (town == "") {
    demo6.innerHTML = "Zadajte mesto, v ktorom bývate!";
    valid = false;
  } else {
    demo6.innerHTML = "";
  }

  if ((pdn == "") || (isNumeric(pdn) == false) || (pdn.length < 5)) {
    demo7.innerHTML = "Zadajte PSČ vašej adresy!";
    valid = false;
  } else {
    demo7.innerHTML = "";
  }

  if (valid == true) {
    return (true);
  } else {
    return (false);
  }
}

function d3() {
  if (validate3() == true) {
    var hide = document.getElementById('address');
    var show = document.getElementById('send');

    hide.style.display = "none";
    show.style.display = "block";
  }
}

function p4() {
  var manner = document.getElementById('manner').value;

  if (manner == "Personal purchase") {
    var hide = document.getElementById('send');
    var show = document.getElementById('get');

  } else {
    var hide = document.getElementById('send');
    var show = document.getElementById('address');
  }

  hide.style.display = "none";
  show.style.display = "block";
}
