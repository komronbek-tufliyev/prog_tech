
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
            alert(`Error ${response.statusText}`, response.status);
            // throw new Error(`HTTP error! status: ${response.status}`);
            return 
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
            alert(`Xatolik yuz berdi, ${response.statusText}`, response.status);
            return 
            // throw new Error(`HTTP error! status: ${response.status}`);
        }
        const responseData = await response.json();
        // console.log('Success:', responseData);
        return responseData;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function addAttrs() {
    const inputData = document.getElementById("attr");
    const list1 = document.getElementsByClassName("list-group")[0];

    const li1 = document.createElement("li");

    li1.className = "list-group-item list-group-item-action";

    li1.innerHTML = inputData.value;
    const categoryValue = document.getElementById("category_value").innerText;
    console.log(categoryValue);
    if (inputData.value !== "") {
        try {
            const endpoint = base_endpoint + 'attributes/';
            const data = {
                name: inputData.value,
                category: categoryValue,
            }
            console.log(data);
            const response = await postDataFetch(endpoint, data);
            console.log(response);
            if (response.status === 201) {
                console.log(response);
                list1.insertBefore(li1, inputData);
            }
        }
        catch (error) {
            console.log(error);
        }
    }

    inputData.value = "";
}

async function addValues() {
    const inputData = document.getElementById("value");
    const list1 = document.getElementsByClassName("list-group")[1];

    const li1 = document.createElement("li");

    li1.className = "list-group-item list-group-item-action";

    li1.innerHTML = inputData.value;

    if (inputData.value !== "") {
        try {
            const endpoint = base_endpoint + 'values/';
            const data = {
                name: inputData.value,
            }
            const response = await postDataFetch(endpoint, data);
            // console.log(response);
            if (response.status === 201) {
                list1.insertBefore(li1, inputData);
                // console.log(response);
            }
        }
        catch (error) {
            console.log(error);
        }
    }

    inputData.value = "";
}

window.onload = function () {
    const attrs_list = getDataFetch(base_endpoint + 'attributes/');
    const values_list = getDataFetch(base_endpoint + 'values/');
    const rules = getDataFetch(base_endpoint + 'answers/');

    const attrs_list_el = document.getElementById("attrs_list");
    const values_list_el = document.getElementById("values_list");

    const input_data_attr = document.getElementById("attr");
    const input_data_value = document.getElementById("value");

    const rules_list = document.getElementById("rules_list");
    rules.then(function (result) {
        console.log(result);
        console.log(result.length);
        new_div = document.createElement("div");
        new_div.className = "m-3";
        for (let i = 0; i < result.length; i++) {
            const p = document.createElement("p");
            p_text = "";
            for (let j = 0; j < result[i]['answer'].length; j++) {
                if(j == 0){
                    p_text += `Agar ${result[i]['answer'][j]['attribute']} = ${result[i]['answer'][j]['value']}`;
                }
                else if(j != result[i]['answer'].length - 1){
                    p_text += ` va ${result[i]['answer'][j]['attribute']} = ${result[i]['answer'][j]['value']}`;
                }
                else{
                    p_text += ` U holda ${result[i]['answer'][j]['attribute']} = ${result[i]['answer'][j]['value']}`;
                }
            }

            p.innerHTML = p_text;
            new_div.appendChild(p);
        }
        rules_list.appendChild(new_div);

    });


    const rules_box = document.getElementById("rules");
    var div1 = document.createElement("div");
    div1.className = "row text-center my-1";
    
    var box2 = document.createElement("div");
    box2.className = "row text-center my-1";

    var div2 = document.createElement("div");
    div2.className = "col";
    div2.innerHTML = "Agar";

    var box2_div2 = document.createElement("div");
    box2_div2.className = "col u-holda";
    box2_div2.innerHTML = "U holda";

    var div3 = document.createElement("div");
    div3.className = "col";
    var select1 = document.createElement("select");
    select1.className = "form-select";

    var box2_div3 = document.createElement("div");
    box2_div3.className = "col";
    var box2_select1 = document.createElement("select");
    box2_select1.className = "form-select";

    attrs_list.then(function (result) {
        for (let i = 0; i < result.length; i++) {
            const li1 = document.createElement("li");
            li1.className = "list-group-item list-group-item-action";
            li1.innerHTML = result[i].name;
            attrs_list_el.insertBefore(li1, input_data_attr);

            var option1 = document.createElement("option");
            option1.innerHTML = result[i].name;
            select1.appendChild(option1);

            var option3 = document.createElement("option");
            option3.innerHTML = result[i].name;
            box2_select1.appendChild(option3);
            
        }
    });

    var div4 = document.createElement("div");
    div4.className = "col";
    div4.innerHTML = "=";

    var div5 = document.createElement("div");
    div5.className = "col";
    var select2 = document.createElement("select");
    select2.className = "form-select";

    var box2_div4 = document.createElement("div");
    box2_div4.className = "col";
    box2_div4.innerHTML = "=";

    var box2_div5 = document.createElement("div");
    box2_div5.className = "col";
    var box2_select2 = document.createElement("select");
    box2_select2.className = "form-select";


    values_list.then(function (result) {
        for (let i = 0; i < result.length; i++) {
            const li1 = document.createElement("li");
            li1.className = "list-group-item list-group-item-action";
            values_list_el.insertBefore(li1, input_data_value);
            li1.innerHTML = result[i].name;

            var option2 = document.createElement("option");
            option2.innerHTML = result[i].name;
            select2.appendChild(option2);
            
            var option4 = document.createElement("option");
            option4.innerHTML = result[i].name;
            box2_select2.appendChild(option4);
        }
    });

    values_list.finally(function () {
        div3.appendChild(select1);
        div5.appendChild(select2);
        div1.appendChild(div2);
        div1.appendChild(div3);
        div1.appendChild(div4);
        div1.appendChild(div5);
        box2.appendChild(box2_div2);
        box2_div3.appendChild(box2_select1);
        box2.appendChild(box2_div3);
        box2_div3.appendChild(box2_select1);
        box2.appendChild(box2_div4);
        box2.appendChild(box2_div5);
        box2_div5.appendChild(box2_select2);
        
        rules_box.appendChild(div1);
        rules_box.appendChild(box2);
    });





}


function add_new_condition() {
    var rules = document.getElementById("rules");
    var u_holda = document.getElementsByClassName("u-holda")[0];
    u_holda.innerHTML = "Va";
    u_holda.className = "col";

    var div1 = document.createElement("div");
    div1.className = "row text-center my-1";

    var div2 = document.createElement("div");
    div2.className = "col u-holda";
    div2.innerHTML = "U holda";


    var div3 = document.createElement("div");
    div3.className = "col";
    var select1 = document.createElement("select");
    select1.className = "form-select";

    var attrs_list = getDataFetch(base_endpoint + 'attributes/');
    
    attrs_list.then(function (result) {
        for (let i = 0; i < result.length; i++) {
            var option1 = document.createElement("option");
            option1.innerHTML = result[i].name;
            select1.appendChild(option1);
        }
    });

    var div4 = document.createElement("div");
    div4.className = "col";
    div4.innerHTML = "=";

    var div5 = document.createElement("div");
    div5.className = "col";
    var select2 = document.createElement("select");
    select2.className = "form-select";

    var values_list = getDataFetch(base_endpoint + 'values/');
    values_list.then(function (result) {
        for (let i = 0; i < result.length; i++) {
            var option2 = document.createElement("option");
            option2.innerHTML = result[i].name;
            select2.appendChild(option2);
        }
    });

    console.log("save_condition");

    // var condition_btns = document.getElementById("condition-btns");
    values_list.finally(function () {
        rules.appendChild(div1);
        div1.appendChild(div2);
        div1.appendChild(div3);
        div3.appendChild(select1);
        div1.appendChild(div4);
        div1.appendChild(div5);
        div5.appendChild(select2);
    });

}



function save_condition() {
    var rules = document.getElementById("rules");
    const category_value = document.getElementById("category_value").innerText;
    var conditions = [];
    var conditions_list = document.getElementsByClassName("row text-center my-1");
    for (let i = 0; i < conditions_list.length-1; i++) {
        var condition = {};
        var condition_attrs = conditions_list[i].getElementsByClassName("form-select");
        condition["attribute"] = condition_attrs[0].options[condition_attrs[0].selectedIndex].text;
        condition["value"] = condition_attrs[1].options[condition_attrs[1].selectedIndex].text;
        condition["category"] = category_value;
        conditions.push(condition);
    }
    var url = base_endpoint + 'conditions/';
    postDataFetch(url, conditions).then(function (result) {
        console.log(result);
    });
}

