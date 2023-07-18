
function init(){
d3.json("./employees.json").then(function(data) {
  console.log(data[0]);
});
}

init();