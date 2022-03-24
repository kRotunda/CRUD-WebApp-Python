function getRan(){
    var make = ["BMW","Chevrolet","Jeep", "Porsche", "Subaru", "Tesla"];
    var bmw = ["M3", "M4", "i8", "3 Series", "X4"];
    var chevrolet = ["Camaro", "Tahoe", "Corvette", "Blazer", "Colorado"];
    var jeep = ["Wrangler", "Gladiator", "Compass", "Cherokee", "Wagoneer"];
    var porsche = ["911", "Macan", "Cayenne", "Boxster", "Taycan"];
    var subaru = ["WRX", "Forester", "Outback", "BRZ", "Legacy"];
    var tesla = ["Model S", "Model 3", "Model X", "Model Y", "Cybertruck"];
    var color = ["Red","Blue","Green","Yellow","Orange","Purple", "Black", "White", "Gray"];
    var ranMake = Math.round(Math.random()* 5);
    var ranModel = Math.round(Math.random()* 4);
    var ranYear = Math.round(Math.random()* 22+2000);
    var ranColor = Math.round(Math.random()* 8);
    make=document.getElementById("make").value = make[ranMake];
    if (ranMake == 0){
        model=document.getElementById("model").value = bmw[ranModel];
    }
    if (ranMake == 1){
        model=document.getElementById("model").value = chevrolet[ranModel];
    }
    if (ranMake == 2){
        model=document.getElementById("model").value = jeep[ranModel];
    }
    if (ranMake == 3){
        model=document.getElementById("model").value = porsche[ranModel];
    }
    if (ranMake == 4){
        model=document.getElementById("model").value = subaru[ranModel];
    }
    if (ranMake == 5){
        model=document.getElementById("model").value = tesla[ranModel];
    }
    year=document.getElementById("year").value = ranYear;
    color=document.getElementById("color").value = color[ranColor];
}