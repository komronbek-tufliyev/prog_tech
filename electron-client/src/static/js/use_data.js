
const base_endpoint = 'http://127.0.0.1:8000/api/';

async function postDataFetch(endpoint, data) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        console.log(response);
        if (!response.ok) {
            alert(`Xatolik yuz berdi ${response.statusText}`, response.status);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const responseData = await response.json();
        console.log('Success:', responseData);
        return responseData;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function getDataFetch(endpoint) {
    try {
        const response = await fetch(endpoint, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        // console.log(response);
        if (!response.ok) {
            alert(`Error ${response.statusText}`, response.status);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const responseData = await response.json();
        // console.log('Success:', responseData);
        return responseData;
    } catch (error) {
        console.error('Error:', error);
    }
}

function add_options() {
    var select1 = document.getElementById("select_attrs");
    var select2 = document.getElementById("select_values");

    var list1 = document.getElementsByClassName("list-group")[0];
    var list2 = document.getElementsByClassName("list-group")[1];

    var option1 = select1.options[select1.selectedIndex].text;
    var option2 = select2.options[select2.selectedIndex].text;

    var li1 = document.createElement("li");
    var li2 = document.createElement("li");

    li1.className = "list-group-item list-group-item-action";
    li2.className = "list-group-item list-group-item-action";

    li1.innerHTML = option1;
    li2.innerHTML = option2;

    list1.appendChild(li1);
    list2.appendChild(li2);
}

function show_result(){
    
}

window.onload = function () {
    const attr_and_values = document.getElementById('attr_and_values');

    const get_attrs = getDataFetch(base_endpoint + 'attributes/');
    const get_values = getDataFetch(base_endpoint + 'values/');

    const select_attrs = document.createElement('select');
    select_attrs.className = 'form-select my-3 mx-2';
    select_attrs.id = 'select_attrs';

    const select_values = document.createElement('select');
    select_values.className = 'form-select my-3 mx-2 ';
    select_values.id = 'select_values';

    get_attrs.then((data) => {
        data.forEach((attr) => {
            const option = document.createElement('option');
            option.value = attr.id;
            option.innerText = attr.name;
            select_attrs.appendChild(option);
        });
    });
    
    get_values.then((data) => {
        data.forEach((value) => {
            const option = document.createElement('option');
            option.value = value.id;
            option.innerText = value.name;
            select_values.appendChild(option);
        });
    });

    attr_and_values.appendChild(select_attrs);
    attr_and_values.appendChild(select_values);
    
}


function show_result(){
    const list1 = document.getElementsByClassName("list-group")[0];
    const list2 = document.getElementsByClassName("list-group")[1];
    const category = document.getElementById("category_value").innerText;

    // var attrs = [];
    // var values = [];
    var conditions = [];

    for (var i = 1; i < list1.children.length; i++) {
        // attrs.push(list1.children[i].innerHTML);
        // values.push(list2.children[i].innerHTML);

        var condition = {
            'attribute': list1.children[i].innerHTML,
            'value': list2.children[i].innerHTML,
            // 'category': category,
        }
        conditions.push(condition);

    }

    var data = {
        'conditions': conditions,
        'category': category,
    }

    console.log(data);

    if (conditions.length == 0) {
        alert('Iltimos, shartlarni kiriting!');
        return;
    }

    try {
        
        const result = postDataFetch(base_endpoint + 'check-answer/', data);
        result.then((data) => {
            console.log("Data", data);
            const result_data = document.getElementById('result_data');
            try {
                console.log(data[0]['answer']);
                console.log(data[0]['answer'][0]['attribute']);
                if (data[0]['answer']) {
                    result_data.innerHTML = 'Natija :=> ' + data[0]['answer'][0]['attribute'] + ' : ' + data[0]['answer'][0]['value'];
                }
                else {
                    result_data.innerHTML = 'Natija :=> ' + 'topilmadi :(';
                }
            } catch (error) {
                console.log('Error:', error);
            }
        });


    } catch (error) {
        console.error('Error:', error);
    }
}


