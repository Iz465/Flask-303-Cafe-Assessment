let minefield = [];
let checkedsquares =[];
let totalflags = 0;
let totalbombs = 0;
let gamestate = true;



function isbomb(){
    let rand = Math.random();
    if(rand < 0.1){
        totalbombs = totalbombs + 1;
        return true;
    }
    return false;
}
function buildgridsquares(){
    const gridcontainer = document.getElementById("grid-cont");
    const grid_width = 10;
    const grid_height = 10;
    for(let y = 1; y <= grid_width; y++){
        for(let x = 1 ; x <= grid_height; x++){
            let cord = {X: x,Y:y};
            cord.bomb = isbomb();
            cord.guide = 0;
            cord.uncovered = false;
            cord.flagged = false;
            minefield.push(cord);
            const gridsquare = document.createElement('div');
            gridsquare.className = `grid-square covered`;
            gridsquare.addEventListener('click',function(){uncoversquare(cord)});

            gridsquare.addEventListener('contextmenu', function(ev) {
                ev.preventDefault();
                flag(cord);
                return false;
            }, false);


            gridsquare.id = `(${cord.X},${cord.Y})`
            gridcontainer.appendChild(gridsquare);
        }
    }
    let bombdisplay = document.getElementById('display-totalbombs')
    bombdisplay.textContent = `Total Bombs: ${totalbombs}`
}
function showbombs(){
    for(let i = 0; i < minefield.length; i++){
        if (minefield[i].bomb == true){
            showbomb(minefield[i]);
            
        }
    }
}
function setguides(){
    listofguides =[]
    for (let i = 0 ; i < minefield.length; i++){
        guide = countadjacent(minefield[i]);
        if(guide > 0){
            minefield[i].guide = guide;
        }
    }
    for (let i = 0 ; i < listofguides.length; i++){
        console.log(listofguides[i]);
    }

}
function showguides(){
    listofguides =[]
    for (let i = 0 ; i < minefield.length; i++){
        if(minefield[i].guide > 0){
            showguide(minefield[i])
        }
    }
    for (let i = 0 ; i < listofguides.length; i++){
        console.log(listofguides[i]);
    }

}
function showguide(c){
    idName = `(${c.X},${c.Y})`;
    square = document.getElementById(idName);
    square.textContent = c.guide;

    let guidecolors = ['blue','green','red','darkblue','darkred','cyan','black','darkgray'];
    square.style.color = guidecolors[c.guide-1];
}
function showbomb(c){
    idName = `(${c.X},${c.Y})`;
    square = document.getElementById(idName);
    square.textContent = "X";
}

function countadjacent(cord){
    if(cord.bomb == true){
        return 0
    }

    weather = getsurounding(cord)
    
    let counter = 0;
    for(let i = 0; i < weather.length; i++){
        if (finder(weather[i]).bomb == true){
            counter = counter +1;
        }
    }
    return counter

}
function finder(cord){
    let adjacent = minefield.find(o => o.X === cord[0] && o.Y === cord[1]);
    if(adjacent == undefined){
        return false;
    }
    return adjacent

}
function printfield(){
    for (let i = 0; i < minefield.length; i++){
        console.log(minefield[i]);
    }
}


function uncoversquare(cord){
    if(gamestate == false){
        console.log('game already ended')
        return 0
    }
    idName = `(${cord.X},${cord.Y})`;
    cord.uncovered = true

    square = document.getElementById(idName);
    square.className = `grid-square uncovered`;
    
    
    if(cord.guide == 0 && cord.bomb == false){
        console.log("clearempty", cord)
        clearempty(cord);
    }
    else if(cord.guide > 0){
        showguide(cord);

    }
    else if(cord.bomb == true){
        showbomb(cord)
        endgame();
    }

    if(checkgamestate()){
        endgame()
    }

}
function checkgamestate(){
    let temp_bombs = []
    let temp_unchecked = []

    for(let i = 0 ; i < minefield.length; i++){
        let cell = minefield[i];
        if (cell.bomb == true){
            temp_bombs.push(cell)
        }
        else if(cell.uncovered == false){
            temp_unchecked.push(cell)
        }

    }
    console.log(temp_bombs)
    console.log(temp_unchecked)

    if (temp_unchecked.length > 0){
        return false
    }
    for(let i =0; i< temp_bombs.length;i++){
        if(temp_bombs[i].flagged == false){
            return false
        }
    }
    return true
}
function flag(cord){
    idName = `(${cord.X},${cord.Y})`;
    square = document.getElementById(idName);

    if(gamestate == false){
        console.log('game already ended')
        return 0
    }

    if(cord.uncovered){
        return 0
    }

    if(cord.flagged){
        //remove flag
        totalflags = totalflags + 1
        square.textContent = "";
        cord.flagged = false
    }
    else{
        //add flag
        totalflags = totalflags - 1
        square.textContent = "🚩";
        cord.flagged = true
        if(checkgamestate()){
            endgame()
        }
    }
    updateflaginfo()
}

function getsurounding(cord){
    let n = [cord.X,cord.Y - 1];
    let s = [cord.X,cord.Y + 1];
    let e = [cord.X + 1,cord.Y];
    let w = [cord.X - 1,cord.Y];

    let ne = [cord.X +1,cord.Y - 1];
    let nw = [cord.X -1,cord.Y - 1];
    let se = [cord.X + 1,cord.Y + 1];
    let sw = [cord.X - 1,cord.Y + 1];

    weather = [n,s,e,w,ne,nw,se,sw];
    return weather;
}



function clearempty(cord){
    console.clear()
    //check 8 surounding cords
    uncheckedsquares =[];

    uncheckedsquares.push(cord);
    checkedsquares.push(cord)

    while(uncheckedsquares.length > 0){
        temp = getuncheckedempty(uncheckedsquares);
        uncheckedsquares = temp;

        for(let j =0; j< uncheckedsquares.length; j++){
            

            let foundcord = uncheckedsquares[j];
            checkedsquares.push(foundcord);
            idName = `(${foundcord.X},${foundcord.Y})`;
            square = document.getElementById(idName);
            square.className = `grid-square uncovered`;
            foundcord.uncovered = true

        }
    }

}
function getuncheckedempty(uncheckedsquares){
    filter = []

    for(let i = 0; i < uncheckedsquares.length; i++){
        temp = []
        
        uncheckcord = uncheckedsquares[i]
        weather = getsurounding(uncheckcord);

        for(let j = 0; j < weather.length; j++){
            f = finder(weather[j])
            if(f == false){} else{ temp.push(f)}
            
        }

        for(let j = 0; j < temp.length; j++){
            if(checkedsquares.includes(temp[j]) == true){

            } else{
                if(filter.includes(temp[j]) == false && temp[j].guide == 0){
                    filter.push(temp[j])
                }else if(temp[j].guide > 0){
                    uncoversquare(temp[j]);

                }
                
            }
        }

    }
    return filter

}

function updateflaginfo(){
    let flaginfo = document.getElementById('display-totalflags')
    flaginfo.textContent = `Total Flags: ${totalflags}`;
}

function endgame(){
    console.log("GAME ENDED")
    let overlay = document.getElementById('overlay')
    overlay.style.display = "block"
    gamestate = false
}

function restart(){
    const list = document.getElementsByClassName("grid-square");

    while(list.length > 0){
        for (let i = 0; i < list.length; i++){
            list[i].remove()
        }
    }


    let overlay = document.getElementById('overlay')
    overlay.style.display = "none"

    startgame();

}

function startgame(){
    minefield = [];
    checkedsquares =[];
    
    gamestate = true
    
    adminmode = false

    buildgridsquares();
    setguides();
    totalflags = totalbombs;
    updateflaginfo()

    if(adminmode == true){
        showguides();
        showbombs();    
    }
    
}
startgame()