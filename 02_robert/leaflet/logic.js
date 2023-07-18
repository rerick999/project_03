function init(){
	let myMap = L.map("map", {
	  center: [37.09,-95.71],
	  zoom: 5
	});
	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(myMap);
	add_markers(myMap);
	//add_legend(myMap);
}
  
function normalize(val, max, min) { 
    if(max - min === 0) return 0; // or 0, it's up to you
	let res=Math.abs((val-1500)/3000);
	res=Math.trunc(res*16777215);
	res=res.toString(16);
	return res;
}

function theradius(r){
	r=r**0.25;
	if(r<1.00) r=1.00;
	return r;
}

function color_info(depth){
	depth=(depth*50);
	if(depth<10)
		return ["red","<10"];
	else if(depth<30)
		return ["orangered","10-30"];
	else if(depth<50)
		return ["orange","30-50"];
	else if(depth<70)
		return ["gold","50-70"];
	else if(depth<90)
		return ["yellow","70-90"];
	else {
		return ["green",">90"];
	}
}

function color_info_old(depth){
	depth=(depth*50);
	if(depth<10)
		return ["lawngreen","<10"];
	else if(depth<30)
		return ["greenyellow","10-30"];
	else if(depth<50)
		return ["gold","30-50"];
	else if(depth<70)
		return ["orange","50-70"];
	else if(depth<90)
		return ["orangered","70-90"];
	else {
		return ["red",">90"];
	}
}

function add_markers(myMap){
	console.log('adding markers...');
	let fpth="./data.geojson";
	d3.json(fpth).then(function(data) {
		for (let i=0;i<data.length;i++){
			console.log(data[i]);
			let lon=data[i]['lon'];
			let lat=data[i]['lat'];
			let qr=data[i]['quick_ratio'];
			let color=color_info(qr);
			let radius=theradius(data[i]['market_cap']);
			let name=data[i]['name'];
			tooltip="name: "+name;
			let address=data[i]['address'];
			tooltip=tooltip+" location: "+address;
			tooltip=tooltip+" quick ratio: "+qr;
			let circle = L.circle([lat,lon], {
				color: color[0],
				stroke: true,
				fillOpacity: 0.3,
				radius: radius,
			}).bindTooltip(tooltip).addTo(myMap);
		}
		//createFeatures(data);
	});	
}

function add_legend(myMap){
	var legend = L.control({position: 'topright'});
	legend.onAdd = function (myMap) {
		var div = L.DomUtil.create('div', 'info legend');
		labels = ['<strong>DEPTH IN KILOMETERS</strong>'];
		labels.push('<ul style="display:inline-block; width: 40px;">');
		labels.push('<li style="background: lawngreen;"> &lt;10 </li>');
		labels.push('<li style="background: greenyellow;"> 10-30 </li>');
		labels.push('<li style="background: gold;"> 30-50 </li>');
		labels.push('<li style="background: orange;"> 50-70 </li>');
		labels.push('<li style="background: orangered;"> 70-90 </li>');
		labels.push('<li style="background: red;"> &gt;90 </li>');
		/*
		categories = [10,30,50,70,90,100];
		for (var i = 0; i < categories.length; i++) {
				let di=depth_info(categories[i]-1);
				labels.push('<li style="background:'+di[0]+';>'+di[1]+'</li>');
				//div.innerHTML +=
				//let newhtml='<i class="circle" style="background:' + di[1] + '"></i> ';
				//alert(newhtml);
				//labels.push(
				//	'<i class="circle" style="background:' + di[1] + '"></i> ');
				//labels.push(
				//	'<i class="circle" style="background:' + di[1] + '"></i> ' +
				//(categories[i] ? categories[i] : '+'));
			}
		*/
		labels.push('</ul>');
		div.innerHTML = labels.join('<br>');
		return div;
	};
	legend.addTo(myMap);
}

init();