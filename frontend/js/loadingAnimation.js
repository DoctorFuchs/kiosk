function loadingAnimation() {
    document.getElementById('iframe').addEventListener('load',() => {
        // Hide the loading indicator
        setTimeout(overlay_off, 1000);
        // Bring the iframe back
        document.getElementById('iframe').style.opacity = '1';
    });
    document.getElementById('iframe').style.opacity = '0';
    var month = new Date().getMonth() + 1
    if(month === 12) {
        var loadingAnimation = "christmasLoadingAnimation.html"
    } else {
        var loadingAnimation = "loadingAnimation.html"
    }
    overlay_on(`<iframe src='${loadingAnimation}' id='loadingAnimation' width='100%' height='100%'>`);
};