
function resultsView(){
    school = ""
    document.getElementById("teams").style.display = "none"
    document.getElementById("results").style.display = "block"
    results();
} 

function typeChange2(t){
  if (type != t){
    type = t;
    tabs = document.getElementsByClassName("tabb");
    Array.from(tabs).forEach(function(tab){
      if (tab.value == type){
        tab.classList.add('selectedtabb')
      } else {
        tab.classList.remove('selectedtabb')
      }
    });
    options()
    results()
  }
}

function typeChange(){
  type = document.getElementById("type").value;
  options()
}

function options(){
  var select = document.getElementById("category");
  var select2 = document.getElementById("sport");
  while (select.options.length > 0) {                
    select.remove(0);
  }    
  while (select2.options.length > 0) {                
    select2.remove(0);
  }  
  if (type == "Totals"){
    var keykeys = ["Total Operating Expenses", "Total Operating Revenues","Generated Revenue",'Subsidies']
    for (i = 0; i <= 3; i++){
        var option = document.createElement("option");
        option.text = Object.keys(categoryNames).includes(keykeys[i]) ? categoryNames[keykeys[i]] : keykeys[i];
        option.value = keykeys[i];
        select.add(option);
    }
    var sports = ["All Sports","Football", "Men's Basketball","Women's Basketball"]
    for (i = 0; i <= 3; i++){
        var option = document.createElement("option");
        option.text = sports[i];
        option.value = i == 0 ? 5 : i - 1
        select2.add(option);
    }
  } else if (type == "Expenses" || type == "Revenues"){
    var keyslist = Object.keys(allData['Oregon State University']['2020']['Totals'])
    var keynumber = 22
    keyslist.forEach(function(key,i) {
      if (key != 'Subsidies' && key != "Total Operating Expenses" && key != "Total Operating Revenues" && key != "Generated Revenue" && key){
        if (type == "Revenues" && i < keynumber){
          var option = document.createElement("option");
          option.text = Object.keys(categoryNames).includes(key) ? categoryNames[key] : key;
          option.value = key;
          select.add(option);
        }
        if (type == "Expenses" && i > keynumber && key != "Excess (Deficiencies) of Revenues Over (Under) Expenses"){
          var option = document.createElement("option");
          option.text = Object.keys(categoryNames).includes(key) ? categoryNames[key] : key;
          option.value = key;
          select.add(option);
        }
      }
    });
    var sports = ["All Sports","Football", "Men's Basketball","Women's Basketball"]
    for (i = 0; i <= 3; i++){
        var option = document.createElement("option");
        option.text = sports[i];
        option.value = i == 0 ? 5 : i - 1
        select2.add(option);
    }
  } else if (type == "Individual Sports"){
    var keykeys = ["Expenses", "Revenues"]
    for (i = 0; i <= 1; i++){
        var option = document.createElement("option");
        option.text = keykeys[i];
        option.value = keykeys[i];
        select.add(option);
    }
     allSports.forEach(function(sport, i){
        var option = document.createElement("option");
        option.text = sport;
        option.value = sport;
        select2.add(option);
    })
  } else {
    Object.keys(allData['Oregon State University']['2020']['Numbers']).forEach(function(key) {
      if (key != 'Name of Compliance Software Used' && key != "Compliance FTEs" && key){
        var option = document.createElement("option");
        option.text = Object.keys(categoryNames).includes(key) ? categoryNames[key] : key;
        option.value = key;
        select.add(option);
      }
    });
    var option = document.createElement("option");
    option.text = "All Sports";
    option.value = 5
    select2.add(option);
  }
}

function results(){

  output = []
  var table = document.getElementById("body");
  while(table.rows.length > 0) {
    table.deleteRow(0);
  }
  var c = document.getElementById("category");
  var category = c.value;
  var s = document.getElementById("sport");
  var sport = s.value;
  var y = document.getElementById("year");
  var year = y.value;
  var c2 = document.getElementById("conference")
  var conf = c2.value;


  var data = Object.keys(allData);
  if (conf != "all"){
    if (conf != "Power Five" && conf != "Group of Five"){
      data = data.filter(function(d){
        return conferences[d] == conf;
      })
    } else if (conf == "Power Five"){
      data = data.filter(function(d){
        return (conferences[d] == "Big Ten" || 
                conferences[d] == "Big 12" || 
                conferences[d] == "SEC" || 
                conferences[d] == "ACC" ||
                conferences[d] == "Pac-12");
      })
    } else if (conf == "Group of Five"){
      data = data.filter(function(d){
        return (conferences[d] != "Big Ten" && 
                conferences[d] != "Big 12" && 
                conferences[d] != "SEC" && 
                conferences[d] != "ACC" &&
                conferences[d] != "Pac-12");
      })
    }
  }
  if (year.substring(0,4) == 'diff'){
    year2 = year.substring(4,8)
    year1 = year.substring(8,12)

    data.forEach(function(key) {
      if (Object.keys(allData[key]).includes(year1) && Object.keys(allData[key]).includes(year2)){
          if (type == "Totals" || type == "Expenses" || type == "Revenues"){
            if (Object.keys(allData[key][year1]["Totals"]).includes(category) && Object.keys(allData[key][year2]["Totals"]).includes(category)){
              output.push([key,
                           numberify(allData[key][year1]["Totals"][category][Number(sport)]),
                           numberify(allData[key][year2]["Totals"][category][Number(sport)])])            
            }
          } else if (type == "Individual Sports"){
            if (Object.keys(allData[key][year1][category]).includes(sport) && Object.keys(allData[key][year2][category]).includes(sport)){
              output.push([key,
                           numberify("$" + allData[key][year1][category][sport]),
                           numberify("$" + allData[key][year2][category][sport])])            
            }
          } else {
            if (Object.keys(allData[key][year1]["Numbers"]).includes(category) && Object.keys(allData[key][year2]["Numbers"]).includes(category)) {
              if ((!notIncluded[year1][category] || !notIncluded[year1][category].includes(schoolNames[key])) && 
                (!notIncluded[year1][category] || !notIncluded[year1][category].includes(schoolNames[key]))){
                output.push([key,
                             numberify(allData[key][year1][type][category]),
                             numberify(allData[key][year2][type][category])])
              }
            }
          }
        }
    });
    sportOptions = ['Football ',"Men's Basketball ","Women's Basketball ",'','','']
    output.sort(function(a,b){
      return (b[2]-b[1]) - (a[2]-a[1])
    })
    var header = document.getElementById('header')
    if (header.rows.length > 0) {
      header.deleteRow(0);
    }
    var row = header.insertRow(0);     
    row.insertCell(0).innerHTML = 'School';
    row.insertCell(1).innerHTML = (type == "Individual Sports" ? (sport + ' ') : sportOptions[sport]) 
                                  + (Object.keys(categoryNames).includes(category) ? categoryNames[category] : category) 
                                  + ' ' + ('' + (Number(year2) - 1) + '-' + year2.substring(2,4));
    row.insertCell(1).innerHTML = (type == "Individual Sports" ? (sport + ' ') : sportOptions[sport]) 
                                  + (Object.keys(categoryNames).includes(category) ? categoryNames[category] : category) 
                                  + ' ' + ('' + (Number(year1) - 1) + '-' + year1.substring(2,4));
    row.insertCell(3).innerHTML = 'Difference';
    row.cells[0].addEventListener('click',function(){ sortTable(0); });
    row.cells[1].addEventListener('click',function(){ sortTable(1); });
    row.cells[2].addEventListener('click',function(){ sortTable(2); });
    row.cells[3].addEventListener('click',function(){ sortTable(3); });
    var total1 = 0
    var total2 = 0
    output.forEach( list => {
        let row2 = table.insertRow();
        let schoolCell = row2.insertCell(0)
        schoolCell.innerHTML = '<img id="miniLogo" src="' + ("Logos/" + schoolNames[list[0]] + ".png") + '"></img>' + schoolNames[list[0]];
        schoolCell.className = 'miniSchool';
        row2.cells[0].addEventListener('click',function(){ schoolView(list[0]); });
        row2.cells[0].addEventListener('hover',function(){ schoolView(list[0]); });
        row2.insertCell(1).innerHTML = '$' + formatNumber(list[1]);
        row2.insertCell(2).innerHTML = '$' + formatNumber(list[2]);
        row2.insertCell(3).innerHTML = '$' + formatNumber(list[2] - list[1]);
        //Math.round((list[2]-list[1])* 100/list[1] * 100)/100 + "%";
        total1 += list[1]
        total2 += list[2]
    });

    sortColumn = 3;
    sortDirection = 1;

    // TOTAL
    let rowFinal = table.insertRow();
    rowFinal.className = 'boldedRow'
    rowFinal.insertCell(0).innerHTML = 'Total'
    rowFinal.insertCell(1).innerHTML = '$' + formatNumber(total1);
    rowFinal.insertCell(2).innerHTML = '$' + formatNumber(total2);
    rowFinal.insertCell(3).innerHTML = '$' + formatNumber(total2 - total1);
    // AVERAGE
    let rowAverage = table.insertRow();
    rowAverage.className = 'boldedRow'
    rowAverage.insertCell(0).innerHTML = 'Average'
    rowAverage.insertCell(1).innerHTML = '$' + formatNumber(Math.floor(total1/output.length));
    rowAverage.insertCell(2).innerHTML = '$' + formatNumber(Math.floor(total2/output.length));
    rowAverage.insertCell(3).innerHTML = '$' + formatNumber(Math.floor((total2 - total1)/output.length));

  } else {
    data.forEach(function(key) {
      if (Object.keys(allData[key]).includes(year)){
          if (type == "Totals" || type == "Expenses" || type == "Revenues"){
            if (Object.keys(allData[key][year]["Totals"]).includes(category)){
              output.push([key,
                           numberify(allData[key][year]["Totals"][category][Number(sport)])])            
            }
          } else if (type == "Individual Sports"){
            if (Object.keys(allData[key][year][category]).includes(sport)){
              output.push([key,
                           numberify("$" + allData[key][year][category][sport])])            
            }
          } else {
            if (Object.keys(allData[key][year]["Numbers"]).includes(category)){
              //console.log(key,year,category)
              //console.log(allData[key][year]["Numbers"]['Excess Transfers to Institution'])
              if (!notIncluded[year][category] || !notIncluded[year][category].includes(schoolNames[key])){
                output.push([key,
                             numberify(allData[key][year][type][category])])
              }
            }
          }
      }
    });
    sportOptions = ['Football ',"Men's Basketball ","Women's Basketball ",'','','']
    output.sort(function(a,b){
      return (b[1]) - (a[1])
    })
    var header = document.getElementById('header')
    if (header.rows.length > 0) {
      header.deleteRow(0);
    }
    var row = header.insertRow(0);  
    var newcell = row.insertCell(0)
    newcell.innerHTML = 'Rank'
    newcell.className = 'rank rankHead'
    row.insertCell(1).innerHTML = 'School';
    row.insertCell(2).innerHTML = (type == "Individual Sports" ? (sport + ' ') : sportOptions[sport]) 
                                  + (Object.keys(categoryNames).includes(category) ? categoryNames[category] : category) 
                                  + ' ' + ('' + (Number(year) - 1) + '-' + year.substring(2,4));
    row.cells[1].addEventListener('click',function(){ sortTable(1); });
    row.cells[2].addEventListener('click',function(){ sortTable(2); });
    var total = 0;
    output.forEach( (list,i) => {
        let row2 = table.insertRow();
        var newcell2 = row2.insertCell(0)
        newcell2.innerHTML = i + 1
        newcell2.className = 'rank';
        let schoolCell = row2.insertCell(1)
        schoolCell.innerHTML = '<img id="miniLogo" src="' + ("Logos/" + schoolNames[list[0]] + ".png") + '"></img>' + schoolNames[list[0]];
        schoolCell.className = 'miniSchool';
        row2.cells[1].addEventListener('click',function(){ schoolView(list[0]); });
        row2.insertCell(2).innerHTML = '$' + formatNumber(list[1]);
        //Math.round((list[2]-list[1])* 100/list[1] * 100)/100 + "%";
        total += list[1]
    });

    sortColumn = 1;
    sortDirection = 1;

    // TOTAL
    let rowFinal = table.insertRow();
    rowFinal.className = 'boldedRow'
    var newcell3 = rowFinal.insertCell(0)
    newcell3.innerHTML = ""
    newcell3.className = 'rank';
    rowFinal.insertCell(1).innerHTML = 'Total'
    rowFinal.insertCell(2).innerHTML = '$' + formatNumber(total);
    // AVERAGE
    let rowAverage = table.insertRow();
    rowAverage.className = 'boldedRow'
    var newcell4 = rowAverage.insertCell(0)
    newcell4.innerHTML = ""
    newcell4.className = 'rank';
    rowAverage.insertCell(1).innerHTML = 'Average'
    rowAverage.insertCell(2).innerHTML = '$' + formatNumber(Math.floor(total/output.length));


    //populate not included footnote
    if (type == "Numbers" && notIncluded[year][category]){
      var string = "";
      notIncluded[year][category].forEach(function(school){
        string += school + ", "
      })
      document.getElementById("notIncluded").innerHTML = "The following schools did not report a number for this category: " + string.substring(0,string.length - 2)
    } else {
       document.getElementById("notIncluded").innerHTML = ""
    }
  }
  
}

function sortTable(column) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("body");
  switching = true;
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 0; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[column];
      y = rows[i + 1].getElementsByTagName("TD")[column];

      xInner = x.innerHTML
      yInner = y.innerHTML

      if (column != sortColumn || sortDirection == 0){
        // Check if the two rows should switch place:
        if ((xInner.substring(0,1) == "$" ? numberify(xInner) : xInner) < 
            (yInner.substring(0,1) == "$" ? numberify(yInner) : yInner)) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
        }
      } else {
        // Check if the two rows should switch place:
        if ((xInner.substring(0,1) == "$" ? numberify(xInner) : xInner) > 
            (yInner.substring(0,1) == "$" ? numberify(yInner) : yInner)) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }

  sortDirection = (sortColumn != column || sortDirection == 0) ? 1 : 0
  sortColumn = column;
}