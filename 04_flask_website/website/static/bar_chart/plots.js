let names=[]
let market_cap=[]
let colors=[]

for (let i = 0; i < searchResults.length; i++) {
  row = searchResults[i];
  names.push(row.name);
  market_cap.push(row.market_cap);
  colors.push(row.color);
}

let trace1 = {
  x: names,
  y: market_cap,
  marker:{color:colors},
  text: names,
  type: "bar"
};

// Create data array
let data = [trace1];

// Apply a title to the layout
let layout = {
  title: "Top 100 US Corporations by Market Capitalization",
  //barmode: "group",
  // Include margins in the layout so the x-tick labels display correctly
  margin: {
    l: 50,
    r: 50,
    b: 200,
    t: 50,
    pad: 4
  }
};

console.log(colors);

// Render the plot to the div tag with id "plot"
Plotly.newPlot("plot", data, layout);
