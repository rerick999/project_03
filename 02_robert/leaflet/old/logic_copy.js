
function init(){
	// Creating our initial map object:
	// We set the longitude, latitude, and starting zoom level.
	// This gets inserted into the div with an id of "map".
	let myMap = L.map("map", {
	  center: [37.09,-95.71],
	  zoom: 5
	});

	// Adding a tile layer (the background map image) to our map:
	// We use the addTo() method to add objects to our map.
	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(myMap);
	
	add_markers(myMap);
	add_legend(myMap);
}

function normalize(val, max, min) { 
    if(max - min === 0) return 0; // or 0, it's up to you
	let res=Math.abs((val-1500)/3000);
	res=Math.trunc(res*16777215);
	res=res.toString(16);
	return res;
}

function depth_info(depth){
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
	//alert('adding markers');
	//let url="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson";
	let url="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.geojson";
	d3.json(url).then(function (data) {
		console.log(data);
		//alert(data.features.length);
		for (let i=0;i<data.features.length;i++){
			console.log(data.features[i]);
			let coords=data.features[i].geometry.coordinates;
			let lon=coords[0];
			let lat=coords[1];
			let depth=coords[2];
			//depth="#" + normalize(depth,16777215,0);
			let depth2=depth_info(depth)[0];
			let properties=data.features[i].properties;
			let mag=properties.mag;
			let mag2=mag**7;
			let place=properties.place;
			tooltip="location: "+place;
			tooltip=tooltip+"\nmagnitude: "+mag;
			tooltip=tooltip+"\ndepth: "+depth;
			tooltip=tooltip+"\nlongitude: "+lon+" latitude: "+lat;
			var circle = L.circle([lat,lon], {
				color: depth2,
				stroke: false,
				fillOpacity: 0.5,
				radius: mag2,
			}).bindTooltip(tooltip).addTo(myMap);
			
		}
		//createFeatures(data.features);
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