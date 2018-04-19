function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

accepted = getCookie("accepted");

if (accepted != "true") {
  window.alert(
    "Používaním tejto stránky vyjadrujete súhlas s použitím súborov cookie. Tieto súbory nám pomáhajú zlepšiť kvalitu stránky."
  );
}

document.cookie = "accepted=true";
