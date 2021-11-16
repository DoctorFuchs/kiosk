function loadingAnimation() {
    document.getElementById('iframe').addEventListener('load', function () {
        // Hide the loading indicator
        document.getElementById('loadingAnimation').style.opacity = '0';
        setTimeout(overlay_off(), 1000);

        // Bring the iframe back
        document.getElementById('iframe').style.opacity = '1';
    });

    document.getElementById('iframe').style.opacity = '0';
    overlay_on("<iframe src='loadingAnimation.html' id='loadingAnimation' width='100%' height='100%'>");
    document.getElementById("loadingAnimation").style.opacity = '1';

};