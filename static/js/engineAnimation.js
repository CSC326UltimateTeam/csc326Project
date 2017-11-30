console.log("run animation");
var animation = bodymovin.loadAnimation({
  container: document.getElementById('engineLogo'), // Required
  path: 'static/js/logoAnimation.json', // Required
  renderer: 'svg', // Required
  loop: true, // Optional
  autoplay: true, // Optional
  name: "Engine Logo", // Name for future reference. Optional.
})
