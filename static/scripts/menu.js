let global
let reward_global =[]
let employee_status = false

//parce reward data from json
function reward(data_reward){
    data = parcedata(data_reward)
    reward_global = data
    for(let i = 0; i < reward_global.length; i++){
        console.log("REWARD",reward_global[i])
    }
}

//check if user is an employee
function isemployee(check){
    console.log("isempl",check)
    employee_status = check
}

//returns reward ammount as percentage
function applyreward(){
    let reward_amount = null //counted in percentage, here is 0% reward; default
    if(reward_global.includes(1)){
        reward_amount = ["One Free Item",100]
        console.log(`discount = ${reward_amount[0]}: ${reward_amount[1]}%`)
    }else if(reward_global.includes(3)){
        reward_amount = ["10% off",10]
        console.log(`discount = ${reward_amount[0]}: ${reward_amount[1]}%`)
    }else if(reward_global.includes(3)){
        reward_amount = ["One Free Coffe",100]
        console.log(`discount = ${reward_amount[0]}: ${reward_amount[1]}%`)
    }
    if(employee_status){
        reward_amount = ["Employee discount",50]
        console.log(`discount = ${reward_amount[0]}: ${reward_amount[1]}%`)
    }
    return reward_amount
}

// assigns data to global variable, then populates menu
function initload(data_unparced){
    console.log(reward_global)
    
    data = parcedata(data_unparced);
    global = data
    populatemenu(global)
}

//deletes then re-populates all menuitems in html
function reload(){
    populatemenu(global)
}

//apply sorting to data then populates all data to html
function populatemenu(data){
    clear_data();
    

    sorteddata = sortdata(data)
    console.log(sorteddata)
    let ul = document.getElementById('data')
    for (let i = 0; i < sorteddata.length; i++){
        product_container = createMenuItem(sorteddata[i])

        ul.appendChild(product_container)

    }
}

//gets input from search bar then reloads data passed though filter
function search(){
    var searchfield = document.getElementById("search");
    let search_str = searchfield.value;
    console.log(search_str);

    filtered_data = filter(search_str,global)
    console.log(filtered_data)

    populatemenu(filtered_data)
}

//compares data from search with each dataitem; returning only items which passed through the filter
function filter(str,data){
    filtered = []
    for(let i = 0; i < data.length; i++ ){
        input = str.toUpperCase()
        title = data[i].title.toUpperCase()
        if(title.includes(input)){
            filtered.push(data[i])
        }
    }
    return filtered
}


//gets imput from sortdropdownselector then sorts it based on its numerical value; sorts by popular, name, and price
function sortdata(data){
    var selector = document.getElementById("sortdropdownselector");
    let sort_id = selector.selectedIndex
    console.log(global)
    if(sort_id == 0){
        return data.sort(sortbypopular);
    }
    else if(sort_id == 1){
        return data.sort(sortbyname);
    }
    else if(sort_id == 2){
        return data.sort(sortbyprice);
    }
}

//sorting by popular
function sortbypopular(a,b){
    console.log("SORTING BY POPULARITY");
    const popularA = a.id;
    const popularB = b.id;

    let comparison = 0;
    if (popularA > popularB){
        comparison = 1;
    } else if (popularA < popularB){
        comparison = -1;
    }
    return comparison;
}

//sorting by name
function sortbyname(a,b){
    console.log("SORTING BY NAME");

    const nameA = a.title.toUpperCase();
    const nameB = b.title.toUpperCase();

    let comparison = 0;
    if (nameA > nameB){
        comparison = 1;
    } else if (nameA < nameB){
        comparison = -1;
    }
    return comparison;
}

//sorting by price
function sortbyprice(a,b){
    console.log("SORTING BY PRICE");

    const priceA = a.price;
    const priceB = b.price;

    let comparison = 0;
    if (priceA > priceB){
        comparison = 1;
    } else if (priceA < priceB){
        comparison = -1;
    }
    return comparison;


}

//given item from database constructs an html object then returns it
function createMenuItem(dataitem){
    active_reward = applyreward()

    let item_cont = ce('div');
    item_cont.className = "item-cont";
    

    

    let a = ce('a');
    a.href = 'http://127.0.0.1:5000/' + dataitem.id;
    a.method = 'POST'

    let product_img = ce('img');
    product_img.title = 'product-img';
    product_img.className = 'item-image';
    product_img.alt = 'Image-alt';
    product_img.src = dataitem.img_url;
    
    let rewardbanner = ce("div");
    if(active_reward != null){
        
        rewardbanner.className = "reward-banner";
        let reward_text = ce('p');
        reward_text.className = 'item-reward'
        let textnode = document.createTextNode(`- ${active_reward[1]}%`)
        reward_text.appendChild(textnode)
        rewardbanner.appendChild(reward_text)
    }else{
        rewardbanner.display = "none"
    }
    


    let item_content = ce('div');
    item_content.className = 'item-content';

    let item_text = ce('div');
    item_text.className = 'item-text inconsolata';

    let item_title = ce('p');
    item_title.className = 'item-title'
    let titlenode = document.createTextNode(dataitem.title)
    item_title.appendChild(titlenode)

    let pricecontainer = ce('div');
    pricecontainer.className = "price-container"
    if(active_reward != null){
        let diff = active_reward[1]/100 * dataitem.price
        let result = dataitem.price - diff

        let item_price = ce('p');
        item_price.className = 'item-price lineover'
        let pricenode = document.createTextNode(dataitem.price)
        item_price.appendChild(pricenode)
        let reward_price = ce('p');
        reward_price.className = 'item-price reward'
        let rewardpricenode = document.createTextNode(result.toFixed(2))
        reward_price.appendChild(rewardpricenode)
        pricecontainer.appendChild(item_price)
        pricecontainer.appendChild(reward_price)
        
    }
    else{
        let item_price = ce('p');
        item_price.className = 'item-price'
        let pricenode = document.createTextNode(dataitem.price)
        item_price.appendChild(pricenode)
        pricecontainer.appendChild(item_price)
    }
    


    let item_desc = ce('p');
    item_desc.className = 'item-desc'
    let descnode = document.createTextNode(dataitem.contains)
    item_desc.appendChild(descnode)

    item_text.appendChild(item_title)
    item_text.appendChild(pricecontainer)
    item_text.appendChild(item_desc)

    item_content.appendChild(item_text)

    a.appendChild(product_img)
    a.appendChild(item_content)
    if(active_reward != null){
        a.appendChild(rewardbanner)
    }
    

    item_cont.appendChild(a)
    
    return item_cont
}

//shorthand for create element
function ce(elementname){
    return document.createElement(elementname);
}

//clear all data in html
function clear_data(){
    document.getElementById('data').innerHTML = ""
}

//parce jsondata
function parcedata(data){
    let parcedlist =[];
    for(let i = 0 ; i< data.length; i++){
        let parced = JSON.parse(data[i]);
        parcedlist.push(parced);
    }
    return parcedlist

}

