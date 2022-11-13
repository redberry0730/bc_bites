
function makeFoodTable(food){
    const newTable = document.getElementById("html-data-table");
    food.forEach(item => {
        let newRow = document.createElement("tr");
        let cell = document.createElement("img");
        cell.innerText = item[6]
        newRow.append(cell)
        for(let i = 3; i < 6; i++){
            let val = item[i];
            let cell = document.createElement("td");
            cell.innerText = val;
            newRow.appendChild(cell);
        }
        newTable.append(newRow);
    });
}