d0 = [];
d1 = [];
d2 = [];

d0s = [];
d1s = [];
d2s = [];

d0p = [];
d1p = [];
d2p = [];

myColors = [];
MAX_OCL = 6000;

var data = new Array();

ws = new WebSocket("ws://" + window.location.host + "/websocket");

ws.onmessage = function(evt) {
	var msg = evt.data;
	console.log(msg);
	obj = JSON.parse(msg);
	
	var temperature = document.getElementById("temperatureLBL");
	temperature.innerText=obj.d0;
	
	var humidity = document.getElementById("humidityLBL");
	humidity.innerText=obj.d1;
	
	var heatindex = document.getElementById("heatindexLBL");
	heatindex.innerText=obj.d2;
	
	d0.push([obj.x, obj.d0]);
	d1.push([obj.x, obj.d1]);
	d2.push([obj.x, obj.d2]);
	
	
	if(d0.length > MAX_OCL){
		d0.shift();
	}
	if(d1.length > MAX_OCL){
		d1.shift();
	}
	if(d2.length > MAX_OCL){
		d2.shift();
	}
	
	if (!(document.option.pause.checked)){
		d0s = d0.slice(0);
		d1s = d1.slice(0);
		d2s = d2.slice(0);
	
		d0p = d0;
		d1p = d1;
		d2p = d2;
	}
	else
	{
		d0p = d0s;
		d1p = d1s;
		d2p = d2s;
	}
	
	var maxstep = 100;
	
	var timelength = document.getElementById("ZoomRange").value;
	
	var fromindex = d0p.length-d0p.length*timelength/maxstep;
	
	if (d0p.length>timelength)
	{
	  d0p = slice(d0p, fromindex, null, timelength);
	  d1p = slice(d1p, fromindex, null, timelength);
	  d2p = slice(d2p, fromindex, null, timelength);
	}

	var n;
	n = 0
	data = new Array();
	myColors = [];
	if (document.chk.pin[0].checked){
		data[n] = {
			data: d0p,
			label: 'Temperature'
		};
		myColors.push('red');
		n=n+1;
	}
	
	if (document.chk.pin[1].checked){
		data[n] = {
			data: d1p,
			label: 'Humidity'
		};
		myColors.push('green');
		n=n+1;
	}
	
	if (document.chk.pin[2].checked){
		data[n] = {
			data: d2p,
			label: 'Heat index'
		};
		myColors.push('blue');
	}
	
}

// Draw Graph
function drawGraph(){
		var graph;
		var container = document.getElementById("graphDiv");
		
		graph = Flotr.draw(container, data, {
			colors: myColors,
			xaxis: {
				minorTickFreq: 4
			}, 
			yaxis: {
				max: 60,
				min: 0
			},
			grid: {
				minorVerticalLines: true
			}
		});

		// Reload
		setTimeout(function(){
			drawGraph();
		}, 500);
}

function slice(array, from, to, step) {
	if (from===null) from=0;
	if (to===null) to=array.length;
	if (!step) return array.slice(from, to);
	var result = Array.prototype.slice.call(array, from, to);
	if (step < 0) result.reverse();
	step = Math.abs(step);
	if (step > 1) {
		var final = [];
		for (var i = result.length - 1; i >= 0; i--) {
		(i % step === 0) && final.push(result[i]);
		};
		final.reverse();
		result = final;
	}
	return result;
}

function updateZoomRange(){
	//get elements
	var myRange = document.getElementById("ZoomRange");
	var myNumber = document.getElementById("ZoomNumber");
	//copy the value over
	myNumber.value = myRange.value;
} // end function

function updateZoomNumber(){
	//get elements
	var myRange = document.getElementById("ZoomRange");
	var myNumber = document.getElementById("ZoomNumber");
	//copy the value over
	myRange.value = myNumber.value;
} // end function

