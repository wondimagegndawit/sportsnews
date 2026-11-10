  var rawData = [{},{},{},{},{},{}];
  var rawData2 = [{},{},{},{},{},{}];
  var dictData = {};
  var dictData2 = {};
  var teams = [];
  var teams2 = [];
  var padding = 75;
  var paddingTop = 75;
  var offset = 500;
  var school = "";
  var colors = {"Ticket Sales": "#B6E053", 
                "Direct Institutional Support": "#5A88B8", 
                "Donations": "#FF6564", 
                "Media Rights": "#C67194", 
                "NCAA Distributions": "#7CC4CC",
                "Conference Distributions":"#24B086",
                "Licensing & Ads": "#FFAC6F", 
                "Miscellaneous": "#ddd",
                "Coaching Compensation":"#FFDE50",
                "Admin Compensation":"#BB998C",
                "Athletic Facilities":"#ff7d5c",
                "Equipment":"#789e4a",
                "Team Travel":"pink",
                "Game Expenses":"#9e7ec2",
                "Athletic Student Aid":"#7ec2ac"
              }

  var colors2 = ["#B6E053", "#5A88B8", "#FF6564", "#C67194", "#7CC4CC", "#24B086", "#FFAC6F", "#473C6C", "#FFDE50","#BB998C",];
  var barColor = '#bbbbbb';
  var revCategories = ["Ticket Sales",
                       "Direct Institutional Support",
                       "Donations",
                       "Media Rights",
                       "NCAA Distributions",
                       "Licensing & Ads", 
                       "Conference Distributions",
                       "Miscellaneous"]
  var expCategories = ["Miscellaneous",
                       "Coaching Compensation",
                       "Admin Compensation",
                       "Athletic Facilities",
                       "Equipment",
                       "Team Travel",
                       "Game Expenses",
                       "Athletic Student Aid"]
  var boxes = {};
  var svg3 = d3.select("#boxes")
  var leftWidth = 530
  var rightWidth = 630


  function searchBoxes(){
      var boxWidth = 150;
      var boxHeight = 180;
      var boxSpacing = 12;
      var boxesPerRow = Math.floor(width / (boxWidth + boxSpacing))
      var sortedSchools = Object.keys(allData).sort(function(a, b){
          if (schoolNames[a] > schoolNames[b]){
            return 1;
          }
          return -1;
      });


      sortedSchools.forEach(function(school,i){
          positionX = i % boxesPerRow;
          positionY = Math.floor(i / boxesPerRow)

          var g3 = svg3.append('g')
            .attr("transform", "translate(" + (positionX * (boxWidth + boxSpacing)) + "," + (positionY * (boxHeight + boxSpacing)) + ")");

          boxes[school] = g3;

          var box = g3.append('rect')
            .data(school)
            .attr('x',0)
            .attr('y',0)
            .attr("width", boxWidth)
            .attr("height", boxHeight)
            .attr('rx',5)
            .attr("class","box")
            .attr('fill','white')
            .attr('strike-width',.5)
            .attr('stroke','#bbb')
            .on("mouseover",function(){
              d3.select(this).attr('fill','#ddd')
              d3.select(this).style("cursor", "pointer"); 
            })
            .on("mouseout",function(){
              d3.select(this).attr('fill','white')
              d3.select(this).style("cursor", "default"); 
            })
            .on("click",function(){
              schoolView(school);
            })

          console.log(school)
          
          g3.append('text')
            .attr("x", (boxWidth / 2))
            .attr("y", boxHeight - 20)
            .attr('text-anchor','middle')
            .attr('font-size',schoolNames[school].length > 15 ? "12px" : "14px")
            .attr('stroke','black')
            .style('stroke-width',.5)
            .attr("class","boxLabel")
            .text(schoolNames[school].toUpperCase())
            .style("pointer-events", "none")

          g3.append('svg:image')
            .attr("x", (boxWidth / 4))
            .attr("y", (boxHeight / 6))
            .attr('width',boxWidth / 2)
            .attr('height',boxHeight / 2)
            .attr("xlink:href", "Logos/" + schoolNames[school] + ".png")
            .attr("class","boxLogo")
            .style("pointer-events", "none")
    })
  }

  function keyup(){
    var boxWidth = 150;
    var boxHeight = 180;
    var boxSpacing = 12;
    var boxesPerRow = Math.floor(width / (boxWidth + boxSpacing))
    var search = document.getElementById("schoolsearch").value.toLowerCase()
    var counter = 0;

    Object.keys(boxes).forEach(function(school,i){
      if (school.toLowerCase().includes(search) || schoolNames[school].toLowerCase().includes(search)){
          positionX = counter % boxesPerRow;
          positionY = Math.floor(counter / boxesPerRow)
          counter += 1;
          boxes[school]
             .attr("transform", "translate(" + (positionX * (boxWidth + boxSpacing)) + "," + (positionY * (boxHeight + boxSpacing)) + ")")
             .attr('opacity',1)

      } else {
        boxes[school].attr('opacity',0);
      }      
    })
  }
  

  // Clears the svg, calls in the data, and calls the individual functions for each graph
  function graphIt(){
    var schoolYear = document.getElementById("schoolYear").value;

    document.getElementById("schoolName").innerHTML = schoolNames[school].toUpperCase()
    document.getElementById("schoolLogo").src = "Logos/" + schoolNames[school] + ".png"

    svg.selectAll("*").remove();
    svgr.selectAll("*").remove();
    rawData[0] = {"Team":"Football"}
    rawData[1] = {"Team":"Men's Basketball"}
    rawData[2] = {"Team": "Women's Basketball"}
    rawData[3] = {"Team": "Other Sports"}
    rawData[4] = {"Team": "Non Sport Specfic"}
    rawData[5] = {"Team": "Overall"}
    // make sure there's actually data
    if (!allData[school][schoolYear] || (schoolNames[school] == "Navy" && schoolYear == "2018")){
      document.getElementById("error").style.display = "block"
      document.getElementById("svgContainer").style.visibility = "hidden"
      document.getElementById("svgContainer2").style.visibility = "hidden"
      document.getElementById("errorMessage").innerHTML = "Sportico's database does not yet contain budget reports from " + schoolNames[school] + " for this fiscal year. It will be updated when we obtain those documents." 
      if (school == "Pittsburgh" || school == "Troy" || school == "Temple"){
        document.getElementById("errorMessage").innerHTML = "Sportico's database does not contain budget reports from " + schoolNames[school] + "."
      }
    } else {
      document.getElementById("error").style.display = "none"
      document.getElementById("svgContainer").style.visibility = "visible"
      document.getElementById("svgContainer2").style.visibility = "visible"
      Object.keys(allData[school][schoolYear]["Totals"]).forEach(function(cat){
        for (i = 0; i <= 5; i++){
          console.log(school,schoolYear)
          console.log(cat)
          rawData[i][cat] = numberify(allData[school][schoolYear]["Totals"][cat][i]);
          if (cat == "Royalties, Licensing, Advertisement and"){
            rawData[i]["Royalties, Licensing, Advertisement and Sponsorships"] = rawData[i][cat]
          }
        }
      })
      for (i = 0; i <= 5; i++){        
        rawData[i]["Miscellaneous"] = rawData[i]["Total Operating Revenues"] 
                                      - rawData[i]["Ticket Sales"] 
                                      - rawData[i]["Direct Institutional Support"] 
                                      - rawData[i]["Contributions"] 
                                      - rawData[i]["Media Rights"] 
                                      - rawData[i]["NCAA Distributions"]
                                      - rawData[i]["Conference Distributions (Non Media and Non Bowl)"] 
                                      - (rawData[i]["Conference Distributions of Bowl Generated Revenue"] ? rawData[i]["Conference Distributions of Bowl Generated Revenue"] : 0)
                                      - rawData[i]["Royalties, Licensing, Advertisement and Sponsorships"] 
        rawData[i]["Conference Distributions"] = rawData[i]["Conference Distributions (Non Media and Non Bowl)"] 
                                                + (rawData[i]["Conference Distributions of Bowl Generated Revenue"] ? rawData[i]["Conference Distributions of Bowl Generated Revenue"] : 0)
        rawData[i]["Licensing & Ads"] = rawData[i]["Royalties, Licensing, Advertisement and Sponsorships"]
        rawData[i]["Donations"] = rawData[i]["Contributions"]
        dictData[rawData[i]["Team"]] = rawData[i]
      }
      teams = Object.keys(dictData);
      rawData = rawData.slice(0,5)

      dashboard(svg, svgr, rawData, dictData, revCategories, "R ");

      ////////////////////////////

      svg2.selectAll("*").remove();
      svg2r.selectAll("*").remove();
      rawData2[0] = {"Team":"Football"}
      rawData2[1] = {"Team":"Men's Basketball"}
      rawData2[2] = {"Team": "Women's Basketball"}
      rawData2[3] = {"Team": "Other Sports"}
      rawData2[4] = {"Team": "Non Sport Specfic"}
      rawData2[5] = {"Team": "Overall"}
      Object.keys(allData[school][schoolYear]["Totals"]).forEach(function(cat){
        for (i = 0; i <= 5; i++){
          rawData2[i][cat] = numberify(allData[school][schoolYear]["Totals"][cat][i]);
          if (cat == "Royalties, Licensing, Advertisement and"){
            rawData2[i]["Royalties, Licensing, Advertisement and Sponsorships"] = rawData2[i][cat]
          } else if (cat == "Athletic Facilities Debt Service, Leases and Rental Fee Direct Overhead and"){
            rawData2[i]["Athletic Facilities Debt Service, Leases and Rental Fee"] = rawData2[i][cat]
          } else if (cat == " Sports Equipment,"){
            rawData2[i]["Sports Equipment, Uniforms and Supplies"] = rawData2[i][cat]
          }
        }
      })
      for (i = 0; i <= 5; i++){        
        rawData2[i]["Miscellaneous"] = rawData2[i]["Total Operating Expenses"] 
                                      - rawData2[i]["Coaching Salaries, Benefits and Bonuses paid by the University and Related Entities"] 
                                      - rawData2[i]["Coaching Salaries, Benefits and Bonuses paid by a Third Party"]
                                      - rawData2[i]["Support Staff/ Administrative Compensation, Benefits and Bonuses paid by the University and Related Entities"] 
                                      - rawData2[i]["Support Staff/ Administrative Compensation, Benefits and Bonuses paid by Third Party"]
                                      - rawData2[i]["Athletic Student Aid"] 
                                      - rawData2[i]["Athletic Facilities Debt Service, Leases and Rental Fee"] 
                                      - rawData2[i]["Team Travel"]
                                      - rawData2[i]["Sports Equipment, Uniforms and Supplies"] 
                                      - rawData2[i]["Game Expenses"] 
        rawData2[i]["Coaching Compensation"] = rawData2[i]["Coaching Salaries, Benefits and Bonuses paid by the University and Related Entities"] 
                                                + rawData2[i]["Coaching Salaries, Benefits and Bonuses paid by a Third Party"]
        rawData2[i]["Admin Compensation"] = rawData2[i]["Support Staff/ Administrative Compensation, Benefits and Bonuses paid by the University and Related Entities"] 
                                                + rawData2[i]["Support Staff/ Administrative Compensation, Benefits and Bonuses paid by Third Party"]
        rawData2[i]["Athletic Facilities"] = rawData2[i]["Athletic Facilities Debt Service, Leases and Rental Fee"]
        rawData2[i]["Equipment"] = rawData2[i]["Sports Equipment, Uniforms and Supplies"] 
        dictData2[rawData2[i]["Team"]] = rawData2[i]
      }
      teams2 = Object.keys(dictData2);
      rawData2 = rawData2.slice(0,5)

      dashboard(svg2, svg2r, rawData2, dictData2, expCategories, "E ");
    }
  }

  function schoolSearchView(){
    document.getElementById("schoolsearch").value = ""
    document.getElementById("results").style.display = "none"
    document.getElementById("teams").style.display = "block"
    document.getElementById("boxes").style.display = "block"
    document.getElementById("svgContainer").style.display = "none"
    document.getElementById("svgContainer2").style.display = "none"
    document.getElementById("alignment").style.display = "block"
    document.getElementById("alignment2").style.display = "none"
    document.getElementById("schoolHeader").style.display = "none"
    document.getElementById("error").style.display = "none"
    svg3.selectAll("*").remove()
    searchBoxes();
  }

  function schoolView(skool){
    school = skool
    document.getElementById("results").style.display = "none"
    document.getElementById("teams").style.display = "block"
    document.getElementById("boxes").style.display = "none"
    document.getElementById("svgContainer").style.display = "inline-block"
    document.getElementById("svgContainer2").style.display = "inline-block"
    document.getElementById("alignment").style.display = "none"
    document.getElementById("alignment2").style.display = "block"
    document.getElementById("schoolHeader").style.display = "block"
    graphIt();
    changeteam(skool);
  }

  function dashboard(svg, svgr, fData, dData, categories, suffix){
    
    // function to handle histogram.
    function histoGram(data,column,blank){
        var fD = getTopBlank(fData, column, blank);

        var hG ={}
        var m = d3.max(fD, function(d) { return d[column]; })
        var theseTeams = fD.map(function(item){
            return item["Team"];
        })

        // create function for x-axis mapping.
        var x = d3.scaleBand()
                .domain(theseTeams)
                .range([0, 450])
                .padding(0.1)

        // Add x-axis to the histogram svg.
        svg.append("g").attr("class", "xaxis")
            .attr("transform", "translate(" + padding + "," + (300 + paddingTop) + ")")
            .call(d3.axisBottom(x).tickSize(5).tickSizeOuter(0));

        // Create function for y-axis map.
        var y = d3.scaleLinear()
                .domain([0, m])
                .range([300,0])

        // Add y-axis to the histogram svg.
        var yCall = svg.append("g").attr("class", "yaxis")
            .attr("transform", "translate(" + padding + ", " + paddingTop + ")")
            .call(d3.axisLeft(y).tickSizeOuter(0).tickFormat(d3.format("$,")));

        // Create bars for histogram to contain rectangles and freq labels.
        var bars = svg.selectAll(".bar").data(fD).enter()
                .append("g").attr("class", "bar");
        
        //create the rectangles.
        bars.append("rect")
            .attr("x", function(d) { return x(d["Team"]) + padding; })
            .attr("y", function(d) { return y(d[column]) + paddingTop; })
            .attr("width", x.bandwidth())
            .attr("height", function(d) { return 300 - y(d[column]); })
            .attr("class","rect")
            .attr('fill',barColor)
            .on("mouseover",mouseover)// mouseover is defined below.
            .on("mouseout",mouseout);// mouseout is defined below.

        //Create the frequency labels above the rectangles.
        bars.append("text").text(function(d){ return d[column] == 0 ? "" : "$" + formatNumber(d[column])})
            .attr("x", function(d) { return x(d["Team"])+x.bandwidth()/2 + padding; })
            .attr("y", function(d) { return y(d[column]) + paddingTop -5; })
            .style("font-size", "8pt")
            .attr("text-anchor", "middle");

        svg.append("text")
            .attr("class","histHead")
            .text(column)
            .attr("x", padding + 190)
            .attr("y", paddingTop - 30)
            .style("font-size", "12pt")
            .attr("text-anchor", "middle");
        
        function mouseover(d){  // utility function to be called on mouseover.
                           
            // call update functions of pie-chart and legend.    
            pC.update(d["Team"],suffix);
            //leg.update(nD);
        }
        
        function mouseout(d){    // utility function to be called on mouseout.
            // reset the pie-chart and legend.    
            pC.update("Overall",suffix);
        }
        
        // create function to update the bars. This will be used by pie-chart.
        hG.update = function(vari, color){
            // update the domain of the y-axis map to reflect change in frequencies.
            y.domain([0, d3.max(fData, function(d) { return d[vari]; })]);
            
            // transition the height and color of rectangles.
            bars.select("rect").transition().duration(500)
                .attr("y", function(d) {return y(d[vari]) + paddingTop; })
                .attr("height", function(d) { return 300 - y(d[vari]); })
                .attr("fill", color);

            // transition the frequency labels location and change value.
            bars.select("text").transition().duration(500)
                .text(function(d){ return d[vari] == 0 ? "" : "$" + formatNumber(d[vari])})
                .attr("y", function(d) {return y(d[vari]) + paddingTop - 5; });    

            var t = d3.transition().duration(500);
            yCall.transition(t).call(d3.axisLeft(y).tickFormat(d3.format("$,")).bind(this));

            svg.select(".histHead").text(vari);
        }        
        return hG;
    }
    
    // function to handle pieChart.
    function pieChart(dData,row,revenue){

        var pD = getPies(dData,row,revenue);

        //console.log(dData)
        //console.log(row)
        //console.log(revenue)

        var pC ={};    
        
        var pieG = svgr.append("g")
          .attr("transform", "translate(" + (70 + padding) + "," + (150 + paddingTop) + ")");

        // create function to draw the arcs of the pie slices.
        var arc = d3.arc().outerRadius(130).innerRadius(0);

        // create a function to compute the pie slice angles.
        var pie = d3.pie().value(function(d) { return d.value; })
                    .sort(null)//.sort(function(a, b) { return d3.ascending(a.key, b.key);} );

        // Draw the pie slices.
        pieG.selectAll("path").data(pie(pD)).enter().append("path")
            .attr("d", arc)
            .each(function(d) { this._current = d; })
            .style("fill", function(d,i) {return colors[d.data.key]; })
            .attr("stroke", "white")
            .style("stroke-width", "1px")
            .style("opacity", 1)
            .on("mouseover",mouseover).on("mouseout",mouseout);

        pieG.selectAll("legendBox").data(pD).enter().append("rect")
          .attr('class',"legendBox")
          .attr('x',155)
          .attr('y',function(d,i){ return - 75 + 20 * i})
          .attr('height',10)
          .attr('width',10)
          .attr("fill",function(d,i) { return colors[d.key];})

        pieG.selectAll("legendText").data(pD).enter().append("text")
          .attr("class",'legendText')
          .attr('x',175)
          .attr('y',function(d,i){ return - 75 + 20 * i + 10})
          .attr('fill','black')
          .attr('font-size','12px')
          .text(function(d,i){ return "$" + formatNumber(d.value)})

        pieG.selectAll("legendText2").data(pD).enter().append("text")
          .attr("class",'legendText2')
          .attr('x',270)
          .attr('y',function(d,i){ return - 75 + 20 * i + 10})
          .attr('fill','black')
          .attr('font-size','12px')
          .text(function(d,i){ return d.key})

        pieG.append("text")
          .attr("class","legendTotal")
          .attr('fill','black')
          .attr('x',165)
          .attr("y", -180)
          .style("font-size", "12pt")
          .attr("text-anchor", "middle")
          .text("Total " + (revenue == "R " ? 
                            "Revenue" + ": $" + formatNumber(dData[row]["Total Operating Revenues"]) :
                            "Expenses" + ": $" + formatNumber(dData[row]["Total Operating Expenses"])
          ))


        // create function to update pie-chart. This will be used by histogram.
        pC.update = function(newRow,newR){
            var newData = getPies(dData,newRow,newR);

            pieG.selectAll("path").data(pie(newData)).transition().duration(500).attrTween("d", arcTween);

            var u = pieG.selectAll('.legendText').remove()

            pieG.selectAll("legendText").data(newData).enter()
              .append("text")
              .attr("class",'legendText')
              .attr('x',175)
              .attr('y',function(d,i){ return - 75 + 20 * i + 10})
              .attr('font-size','12px')
              .attr('fill','black')
              .text(function(d,i){ return "$" + formatNumber(d.value)})

            pieG.select(".legendTotal").text(newRow + " " + 
                                            (newR == "R " ? "Revenue" : "Expenses") + ": $" + 
                                            (newR == "R " ? formatNumber(dData[newRow]["Total Operating Revenues"]) : formatNumber(dData[newRow]["Total Operating Expenses"])))
        }        
        
        // Utility function to be called on mouseover a pie slice.
        function mouseover(d,i){
            pieG.selectAll("path")
              .style('opacity',function(da){return da.data.key == d.data.key ? 1 : 0.3})
            pieG.selectAll(".legendBox")
              .style('opacity',function(da){return da.key == d.data.key ? 1 : 0.3})
            pieG.selectAll(".legendText")
              .style('opacity',function(da){return da.key == d.data.key ? 1 : 0.3})
            pieG.selectAll(".legendText2")
              .style('opacity',function(da){return da.key == d.data.key ? 1 : 0.3})

            // call the update function of histogram with new data.
            hG.update(d.data.key,colors[d.data.key])
        }
        //Utility function to be called on mouseout a pie slice.
        function mouseout(d,i){
              pieG.selectAll("path")
              .style('opacity',1)
              pieG.selectAll(".legendBox")
              .style('opacity',1)
              pieG.selectAll(".legendText")
              .style('opacity',1)
              pieG.selectAll(".legendText2")
              .style('opacity',1)
            // call the update function of histogram with all data.
            hG.update((suffix == "R " ? "Total Operating Revenues" : "Total Operating Expenses"),barColor);
        }
        // Animating the pie-slice requiring a custom function which specifies
        // how the intermediate paths should be drawn.
        function arcTween(a) {
            var i = d3.interpolate(this._current, a);
            this._current = i(0);
            return function(t) { return arc(i(t)); };
        }    

        return pC;
    }

    function getTopBlank(data, sortable, blank){
      /*data.sort(function(a,b){ 
        return b[sortable] - a[sortable];
      })*/
      return data.slice(0,blank)
    }

    function getPies(data,index,which){
      return d3.entries(data[index]).filter(function(item,index){
        return categories.includes(item.key);
      }).sort(function(a,b){
        return data["Overall"][b.key] - data["Overall"][a.key];
      })
    }

    var hG = histoGram(fData, (suffix == "R " ? "Total Operating Revenues" : "Total Operating Expenses"), 8), // create the histogram.
        pC = pieChart(dData,"Overall", suffix); // create the pie-chart.
  }


