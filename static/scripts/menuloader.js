
function runPyScript(input){
    console.log(input)
    var jqXHR = $.ajax({
        type: "POST",
        url: "Cafe-UX-Project/menu/views.py",
        data: { param: input }
    }).done(function(){
        console.log("CHECK")
    }).fail(function(){
        console.log("FAIL")
    })

    

    return jqXHR.responseText;
}

class Item{
    constructor(obj){
        this.name = obj.name;
        this.price = obj.price;
        this.contains = obj.cont;
        
    }
    showDetails() {
        console.log(`Name: ${this.name}, Price: ${this.price},
                     Contains: ${this.contains}`);
    }
}

class SortingManager{
    constructor(){
        this.mode = ['name','price'];
        this.Sortby = this.mode[0];
        this.Search = "";
    }
    update(){
        document.getElementById("data").innerHTML = ""
        getJsonData();
    }
    find(menulist){
        let filteredlist = []
        if(this.Search == ""){
            return menulist;
        }
        for(let x in menulist){
            let itemname = menulist[x].name.toLowerCase()
            if(itemname.includes(this.Search)){
                filteredlist.push(menulist[x])
            }
        }

        return filteredlist;
    }
    
    sortitems(menulist){
        let sortedlist = [];
        if(this.Sortby == 'name'){
            sortedlist = sortAlpha(menulist);
        }
        if(this.Sortby == 'price'){
            sortedlist = sortNum(menulist);
        }
        return sortedlist;
    }
}
let sortingmanager = new SortingManager();
function search(){
    var e = document.getElementById("search");
    console.log(""+e.value);
    sortingmanager.Search = e.value.toLowerCase();
    sortingmanager.update();
}

function combochange(){
    var e = document.getElementById("combobox");
    var value = e.value;
    sortingmanager.Sortby = value;
    sortingmanager.update();
}
function sortAlpha(list){
    let sortedlist = [];
    sortedlist = list.sort(function(a,b){
        let x = a.name.toLowerCase();
        let y = b.name.toLowerCase();
        if (x < y) {return -1;}
        if (x > y) {return 1;}
        return 0;
    })
    console.log(sortedlist)
    return sortedlist;
}
function sortNum(list){
    let sortedlist = [];
    sortedlist = list.sort(function(a,b){return a.price - b.price})
    return sortedlist;
}
function getData(){
    response= runPyScript("listMenuPage");
    console.log(response);
    // itemlist = new Array();
    // for(let i = 0; i < obj.item.length; ++i){
    //     itemlist.push(new Item(obj.item[i]));
    // }
    // console.log("Menuitems count: " + itemlist.length)
    // build(itemlist)
}


function build(obj){
    let list = document.getElementById("data");
    let sortedlist = sortingmanager.sortitems(obj);
    let filteredlist = sortingmanager.find(sortedlist)
    for(let i = 0; i < filteredlist.length; ++i){
        menuitem = construct_item(filteredlist[i]);
        list.appendChild(menuitem);
    }

}


function construct_item(obj){
    let itemcontainer = document.createElement('div');
    itemcontainer.classList.add("item-cont");
    let image = document.createElement("img");
    image.classList.add("item-image");
    image.src = "Assets/Images/placeholder.jpg";
    let content = document.createElement("div");
    content.classList.add("item-content");
    let lable = document.createElement("p");
    lable.innerText = obj.name;
    lable.classList.add("item-lable");

    let price = document.createElement("p");
    price.innerText = obj.price
    price.classList.add("item-price");

    let description = document.createElement("p");
    let newstring = "";
    for (let x in obj.contains) {
        newstring += obj.contains[x] + " ";         
    }

    description.innerText = newstring;
    description.classList.add("item-desc");


    content.appendChild(lable);
    content.appendChild(price)
    content.appendChild(description);
    itemcontainer.appendChild(image);
    itemcontainer.appendChild(content);
    return itemcontainer;
}
/////
// Need to add sorting by: name, price


// do something with the response
