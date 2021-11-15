function loadingAnimation() {
    document.getElementById('iframe').addEventListener('load', function () {
        // Hide the loading indicator
        document.getElementById('loadingAnimation').style.visibility = 'hidden';
        setTimeout(overlay_off(), 1000);

        // Bring the iframe back
        document.getElementById('iframe').style.visibility = 'visible';
    });
    document.getElementById('iframe').style.visibility = 'hidden';
    overlay_on("<iframe src='loadingAnimation.html' id='loadingAnimation' width='100%' height='100%' style='visibility:hidden; transition:visibility 1s ease;'>");
    document.getElementById("loadingAnimation").style.visibility = 'visible';

};