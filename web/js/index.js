var slider = document.getElementById("slider");
var output = document.getElementById("slider-value");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
}

eel.expose(sendalert); // Expose this function to Python
function sendalert(x) {
    alert(x);
}

async function previous() {
    let n = await eel.previous()();
    console.log(n);
    $("#Title").html(n.Title);
    $("#Image").attr("src",n.Image);
    slider.value = n.Score;
    output.innerHTML = slider.value;
    $("#MeanScore").html(n.MeanScore/10);
    $("#Current").html(n.Count+"/"+n.Total);
}
async function next() {
    let n = await eel.next()();
    console.log(n);
    $("#Title").html(n.Title);
    $("#Image").attr("src",n.Image);
    slider.value = n.Score;
    output.innerHTML = slider.value;
    $("#MeanScore").html(n.MeanScore/10);
    $("#Current").html(n.Count+"/"+n.Total);
}
async function save() {
    let n = await eel.save(slider.value)();
}
next();