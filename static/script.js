var selected_month = 1;


function closeFooter() {
    footer = document.getElementById('footer');
    footer.style.display = 'none';
}

function selectMonth(month_num) {
    for (let month = 1; month < 13; month ++) {
        elements = document.getElementsByName(month);
        for (let element_index = 0; element_index < elements.length; element_index ++) {
            var selected_element = elements[element_index];
            if (month != month_num) {
                selected_element.style.display = 'none';
            } else { // if it is equal then make it visible
                selected_element.style.display = 'inline';
                console.log(selected_element);
            };
        };
    };
    selected_month = month_num;
}

function selectNext() {
    selected_month = ((selected_month + 1) % 13);
    if (selected_month == 0) {
        selected_month += 1;
    };
    selectMonth(selected_month);
    console.log(selected_month);
}

function selectPrev() {
    selected_month = selected_month - 1;
    if (selected_month == 0) {
        selected_month = 12;
    };
    selectMonth(selected_month);
    console.log(selected_month);
}