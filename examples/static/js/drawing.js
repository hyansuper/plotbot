var lineWidth = 2;
var color = "black";
var canvas = document.getElementById("canv");
var context = canvas.getContext("2d");
context.lineJoin = 'round';
context.lineCap = 'round';
context.strokeStyle = color;
context.fillStyle = color;
context.lineWidth = lineWidth;

var user_id = 0;
var enabled = false;
var drawing = false;

var socket = io();

function canv2bot(p){
	return [p[1]*0.2+25, p[0]*0.2-50];
}

function bot2canv(p) {
	return [(p[1]+50)*5, (p[0]-25)*5];
}

function clear(){
	context.clearRect(0, 0, canvas.width, canvas.height);
}

function _press(p){
	var r = Math.ceil(lineWidth/2);
	context.beginPath();
	context.arc(p[0], p[1], r, 0, Math.PI*2);
	context.closePath();
	context.fill();
	context.beginPath();
	context.moveTo(p[0], p[1]);
}

function press(e) {
	if (enabled){
		_press([e.offsetX, e.offsetY])
		drawing = true;
		var p = canv2bot([e.offsetX, e.offsetY]);
		socket.emit('down', p);
	}
}

function _release(){
	context.closePath();
}

function release(e){
	if(enabled){
		_release();
		drawing = false;
		socket.emit('up');
	}
}

function _drag(p) {
	context.lineTo(p[0], p[1]);
	context.stroke();
}

function drag(e){
	if(drawing && enabled){
		_drag([e.offsetX, e.offsetY]);
	    
	    var p = canv2bot([e.offsetX, e.offsetY]);
	    socket.emit('lineto', p);
	}
}

canvas.addEventListener("mousedown", press);
canvas.addEventListener("mouseup", release);
canvas.addEventListener("mousemove", drag);
canvas.addEventListener("mouseout", release);

canvas.addEventListener("touchstart", press);
canvas.addEventListener("touchend", release);
canvas.addEventListener("touchmove", drag);
canvas.addEventListener("touchcancel", release);

function confirm_clear(){
	if(confirm("清除笔迹？")){
		clear();
	}
}

function start() {
	user_id = Date.now();
	socket.emit('occupy', user_id, true);
}

function end() {
	socket.emit('occupy',user_id, false);
	enabled = false;
}

socket.on('user', function(data){
	if(data.id == user_id){
		document.getElementById('start').disabled=true;
		document.getElementById('end').disabled=false;
		enabled = true;
		document.getElementById('msg').innerHTML = '<p style="color:green">ok</p>';
	}else if(data.id==null){
		document.getElementById('start').disabled=false;
		document.getElementById('end').disabled=true;
		enabled = false;
		document.getElementById('msg').innerHTML = '<p style="color:green">PlotBot 空闲</p>';
	}else{
		document.getElementById('start').disabled=true;
		document.getElementById('end').disabled=true;
		enabled = false;
		document.getElementById('msg').innerHTML = '<p style="color:orange">PlotBot 正在被占用</p>';
	}
})

socket.on('up', function() {
	if(!enabled){
		_release();
	}
})

socket.on('down', function(p) {
	if(!enabled){
		_press(bot2canv(p));
	}
})

socket.on('lineto', function(p) {
	if(!enabled){
		_drag(bot2canv(p));
	}
})

socket.on('lines', function(lines) {
	lines.forEach((line)=>{
		var first = true;
		line.forEach((p)=>{
			if(first){
				first=false;
				_press(bot2canv(p));
			}
			else{
				_drag(bot2canv(p));
			}
		});
		_release();
	});
})

socket.on('reset', clear);
