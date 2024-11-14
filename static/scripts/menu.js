
function initload(data_unparced){
    clear_data();

    data = parcedata(data_unparced);
    let ul = document.getElementById('data')
    for (let i = 0; i < data.length; i++){
        product_container = createMenuItem(data[i])

        ul.appendChild(product_container)

    }

}


function createMenuItem(dataitem){
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

    let item_content = ce('div');
    item_content.className = 'item-content';

    let item_text = ce('div');
    item_text.className = 'item-text inconsolata';

    let item_title = ce('p');
    item_title.className = 'item-title'
    let titlenode = document.createTextNode(dataitem.title)
    item_title.appendChild(titlenode)

    let item_price = ce('p');
    item_price.className = 'item-price'
    let pricenode = document.createTextNode(dataitem.price)
    item_price.appendChild(pricenode)

    let item_desc = ce('p');
    item_desc.className = 'item-desc'
    let descnode = document.createTextNode(dataitem.contains)
    item_desc.appendChild(descnode)

    item_text.appendChild(item_title)
    item_text.appendChild(item_price)
    item_text.appendChild(item_desc)

    item_content.appendChild(item_text)

    a.appendChild(product_img)
    a.appendChild(item_content)

    item_cont.appendChild(a)
    
    return item_cont
}


function ce(elementname){
    return document.createElement(elementname);
}

function clear_data(){
    document.getElementById('data').innerHTML = ""
}

function parcedata(data){
    let parcedlist =[];
    for(let i = 0 ; i< data.length; i++){
        let parced = JSON.parse(data[i]);
        parcedlist.push(parced);
    }
    return parcedlist

}