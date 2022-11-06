var pathname = window.location.pathname;
var nav = document.querySelector('.navbar-nav');
var anchors = nav.getElementsByTagName('a');

for (var i = 0; i < anchors.length; i += 1) {
    var href = anchors[i].getAttribute('href');
    if (href == pathname) {
        anchors[i].setAttribute('class', 'nav-item nav-link active');
        var sr_only = anchors[i].getElementsByTagName('span');
        sr_only[0].innerHTML = "(Current)";
    }
    else{
        anchors[i].setAttribute('class', 'nav-item nav-link');
    }
}
