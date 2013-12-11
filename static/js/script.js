$(document).ready(function(){
	var players={}
	$.ajax({
		url:"getRecommendations",
		datatype:"json",
		success:function(data){
			if(data){
				setPlayers(data);
				var team=[];
				$.each(data, function(key,player){
					team.push(player[1][1]);
				});
				$.each(team, function(key,value){
						if(value[2] == "WR"){
							$("#receivers").append("<div id='"+value[0]+"' class='card'><header><span>"+value[1]+"</span></header><img src='static/images/"+value[1]+".jpg' alt='"+value[1]+"'><div id='stats'><div>"+value[2]+"</div><div><span>Rating<br>"+value[3].toFixed(2)+"</span></div></div><div id='rec'><img src='static/images/Thumbs-Up.jpg'><a id='"+value[0]+"' class='analysis' href='#'>Why?</a></div>");
						}
						else if(value[2] == "TE"){
							$("#tightends").append("<div id='"+value[0]+"' class='card'><header><span>"+value[1]+"</span></header><img src='static/images/"+value[1]+".jpg' alt='"+value[1]+"'><div id='stats'><div>"+value[2]+"</div><div><span>Rating<br>"+value[3].toFixed(2)+"</div></div><div id='rec'><img src='static/images/Thumbs-Up.jpg'><a id='"+value[0]+"' class='analysis' href='#'>Why?</a></div>");
						}
						else if(value[2] == "QB"){
							$("#quarterbacks").append("<div id='"+value[0]+"' class='card'><header><span>"+value[1]+"</span></header><img src='static/images/"+value[1]+".jpg' alt='"+value[1]+"'><div id='stats'><div>"+value[2]+"</div><div><span>Rating<br>"+value[3].toFixed(2)+"</div></div><div id='rec'><img src='static/images/Thumbs-Up.jpg'><a id='"+value[0]+"' class='analysis' href='#'>Why?</a></div>");
						}
						else if(value[2] == "RB"){
							$("#runningbacks").append("<div id='"+value[0]+"' class='card'><header><span>"+value[1]+"</span></header><img src='static/images/"+value[1]+".jpg' alt='"+value[1]+"'><div id='stats'><div>"+value[2]+"</div><div><span>Rating<br>"+value[3].toFixed(2)+"</div></div><div id='rec'><img src='static/images/Thumbs-Up.jpg'><a id='"+value[0]+"' class='analysis' href='#'>Why?</a></div>");
						}
						else if(value[2] == "DEF"){
							$("#defense").append("<div id='"+value[0]+"' class='card def'><header><span>"+value[1]+"</span></header><img src='static/images/"+value[1]+".jpg' alt='"+value[1]+"'><div id='stats'><div>"+value[2]+"</div><div><span>Rating<br>"+value[3].toFixed(2)+"</div></div><div id='rec'><img src='static/images/Thumbs-Up.jpg'><a id='"+value[0]+"' class='analysis' href='#'>Why?</a></div>");
						}
						else 
							$("#kicker").append("<div id='"+value[0]+"' class='card'><header><span>"+value[1]+"</span></header><img src='static/images/"+value[1]+".jpg' alt='"+value[1]+"'><div id='stats'><div>"+value[2]+"</div><div><span>Rating<br>"+value[3].toFixed(2)+"</div></div><div id='rec'><img src='static/images/Thumbs-Up.jpg'><a id='"+value[0]+"' class='analysis' href='#'>Why?</a></div>");
				});
			}
		}
	});
	function setPlayers(data){
		players=data;
	}
	$(".analysis").on("click",function(){
		alert("hi");
		var ide = this.id;
		console.log(ide);
	});
	
});

