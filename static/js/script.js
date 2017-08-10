	queue()
	.defer(d3.json, "/get_decisions/")
	.await(makeGraphs);

	function makeGraphs(error,recordsJson) {
		if(error) console.log(error);

		$("td").tooltip({tooltipClass: "custom-tooltip"});

		console.log(recordsJson);
		build_tree(recordsJson);

		$( "#slider" ).slider({
			range:true,
			min: 1990,
			max: 2017,
			step: 1,
			values: [ 1990, 2017 ],
			slide: function( event, ui ) {
				if(ui.values[0] == ui.values[1]){
					$( "#date" ).val( " " + ui.values[0] );
				}
				else{
					$( "#date" ).val( " entre " + ui.values[0] + " et " + ui.values[1] + " " );
				}
			}
		});
		$( "#date" ).val( " entre " + $( "#slider" ).slider( "values", 0 ) + " et " + $( "#slider" ).slider( "values", 1 ) + " " );

		var opt = $("#slider").data().uiSlider.options;
		var vals = opt.max - opt.min;

		for (var i = 1; i <= vals+1; i+=3) {

			var el = $('<label>'+(1989+i)+'</label>').css('left',((i-1)/vals*100)+'%');

			$( "#slider" ).append(el);

		}

		var count = 0;
		document.getElementById("createGroupe").onclick = function() {
			villes = [];

			$("input[type=checkbox]:checked", ".villes").each ( function() {
				villes.push($(this).val());

			});
			count++;
			//document.getElementById("groups").innerHTML += "Groupe "+count+": "+villes +"<br>";

			var p = document.createElement("p");
				var parentNode = document.getElementById("groups");
				p.id = count;
				p.innerHTML = "Groupe "+count+": "+villes ;
				parentNode.appendChild(p);
				
			deselectAll("villes");
		}

		//document.getElementById("deselectAll").onclick = function() {deselectAll("categories")};
		//document.getElementById("selectAll").onclick = function() {selectAll("categories")};
		document.getElementById("deselectAllV").onclick = function() {deselectAll("villes")};
		document.getElementById("selectAllV").onclick = function() {selectAll("villes")};

		function deselectAll(type) {
			$('input:checkbox', "."+type).prop('checked', false);
		}


		function selectAll(type) {
			$('input:checkbox', "."+type).prop('checked', true);
		}

		var categories = [],
		villes = [],
		quantumD = [],
		quantumR = [],
		resultats = [],
		date = [],
		full_texte ="";

		$('#clearFiltres').click(function(){
			console.log("clear");
			var inputDate = document.getElementById("date1");
			var inputFullTexte = document.getElementById("searchByKW");
			$( "#slider" ).slider( "values", 0, 1990 );
			$( "#slider" ).slider( "values", 1, 2017 );
			$( "#date" ).val( " entre " + $( "#slider" ).slider( "values", 0 ) + " et " + $( "#slider" ).slider( "values", 1 ) + " " );
			count = 0;
			var pNode = document.getElementById("groups");
			while (pNode.firstChild) {
   			 pNode.removeChild(pNode.firstChild);
			}
			//inputDate.value = "";
			inputFullTexte.value = "";
			deselectAll("villes");

		});
		

		function updateTabel(data){
			var tbody = $('#tbody');
			tbody.empty();
			console.log("updateTabel");
			data.forEach(function(decision) {
				var tr = $('<tr/>').appendTo(tbody);

				tr.append('<td>' + decision[1] + '</td>');
				tr.append('<td>' + decision[2] + '</td>');
				tr.append('<td>' + decision[3] + '</td>');
				tr.append('<td>' + decision[4] + '</td>');
				//tr.append('<td>' + decision[5] + '</td>');
				tr.append('<td>' + decision[7] + '</td>');
				tr.append('<td>' + decision[8] + '</td>');
				tr.append('<td>' + decision[14] + '</td>');
				tr.append('<td>' + decision[16] + '</td>');
				tr.append('<td>' + decision[9] + '</td>');
				//console.log(decision[5].split("\"")[0]);
				
				var splDec = decision[5].split("\"");

				var appendDec = '';

				splDec.forEach(function(elem) {
					appendDec += elem;

				});
				
				//dict.forEach(function(d) {
					tr.append("<td>  <a href='#' title=\" "+ appendDec + " \" onclick=\"openDescription(this)\" > Voir </a> </td>");

				})
		};

		function search(){
			//par date
			date = [];

			var date1 = $( "#slider" ).slider( "values", 0 );
			var date2 = $( "#slider" ).slider( "values", 1 );
			if(date1 > 1990 && date2 <= 2017){
				if(date1 == date2){
					date.push(date1);
				}
				else
				{
					date.push(date1);
					date.push(date2);
				}
			}

			//par mot-cle
			full_texte = "";
			var inputFullTexte = document.getElementById("searchByKW").value;
			full_texte = inputFullTexte;
			
			//par ville
			villes=[];

			$("input[type=checkbox]:checked", ".villes").each ( function() {
				villes.push($(this).val());

			});
			/*
			if(villes.length==0){
				$("input[type=checkbox]", ".villes").each ( function() {
					villes.push($(this).val());

				});
			}
			*/
			var groups = []
			if(document.getElementById("groups").hasChildNodes()){

				for(var i = 1; i <= document.getElementById("groups").childNodes.length; i++){
					var group = document.getElementById(i).innerHTML;
					var pos = group.indexOf(":") + 2;
					groups.push(group.slice(pos, group.length));
				}
			}
			console.log(groups);
			var categorie = document.getElementById("sortTreeCategorie").checked;
			var ville = document.getElementById("sortTreeVille").checked;
			var root_search = '/sortByCategorie/';
			if (ville){
				root_search = '/sortByVille/';
			}
			if(groups.length != 0){
				root_search = '/groupVille/';
			}
			console.log(root_search);
			$.getJSON($SCRIPT_ROOT + root_search, {
				categories: JSON.stringify(categories),
				villes: JSON.stringify(villes),
				date: JSON.stringify(date),
				texte: JSON.stringify(full_texte),
				groups: JSON.stringify(groups),
				juridiction: JSON.stringify([]),
				quantumD: JSON.stringify(quantumD),
				quantumR: JSON.stringify(quantumR),
				resultat: JSON.stringify(resultats)
			}, function(data){
				var showRes = document.getElementById("resultat");

				//var inputDate = document.getElementById("date1").value;
				var inputFullTexte = document.getElementById("searchByKW").value;
				//var condDate = document.getElementById("sel_cond_date").value;
				var parametreRecherche = " <br> Recherche effectuée: ";
				//var villesChecked =" <strong>ville(s)</strong> <i>"+villes+"</i> ";
				
				if(date1 >= 1990 && date2 <= 2017){
					if (date1 == date2) {
						parametreRecherche+="<strong>date</strong> <i>" +date1+"</i>";

					} else{
						parametreRecherche+="<strong>date</strong> entre <i>" +date1+"</i> et <i>"+date2+"</i> ";
					}
				}
				/*
				if(villes.length < 34){
					parametreRecherche += villesChecked;
				}
				*/
				if (inputFullTexte != ""){
					parametreRecherche+="<strong>mot-clé</strong> <i>"+inputFullTexte+"</i> ";
				}

				if(data.tree.nb == 0){
					showRes.style="display: ;"
					showRes.innerHTML = "Désolé, aucun résultat ne correspond pas à votre recherche."+parametreRecherche;
				}else{

					showRes.style="display: ;"
					showRes.innerHTML = "Voici les demandes correspondant à votre recherche."+parametreRecherche;//<strong>"+ data.tree.nb+ "</strong>

				}
				console.log(data);
				
				//updateTabel(data.result);

				var div_tree = document.getElementById("tree_map");
				console.log(div_tree);
				div_tree.remove();//(div_tree.childNodes[0]);
				
				var histogram_n = document.createElement("div");
				var parentNode = document.getElementById("popup");
				histogram_n.id = "tree_map";
				parentNode.appendChild(histogram_n);
				
				build_tree(data);
				var isExpanded = $("#showFiltres").attr("aria-expanded");

				if( isExpanded == 'true'){
					console.log("isExpandedTRUE");
					$("#showFiltres").click();
				}	

			});

		}

		$("#searchByCity").click(function() {
			villes=[];

			$("input[type=checkbox]:checked", ".villes").each ( function() {
				console.log($(this).val());
				villes.push($(this).val());

			});

			if(villes.length == 0){
				document.getElementById("fltrVilles").style = "display:none";
			}else{
				document.getElementById("fltrVilles").style = "display:";

			}
			search();
		});


		/* Pagination */ 
		$("#showFiltres").click(function() {
			var isExpanded = $("#showFiltres").attr("aria-expanded");
			var parentNode = document.getElementById("pagination");
			
			if(isExpanded == 'false' || isExpanded == undefined)
			{
				console.log("click isExpanded "+isExpanded);
				$.getJSON($SCRIPT_ROOT + 'show_text', {
					categories: JSON.stringify(categories),
					villes: JSON.stringify(villes),
					date: JSON.stringify(date),
					texte: JSON.stringify(full_texte),
					juridiction: JSON.stringify([]),
					quantumD: JSON.stringify(quantumD),
					quantumR: JSON.stringify(quantumR),
					resultat: JSON.stringify(resultats)
				}, function(data){
					console.log(data);
					updateTabel(data.result);
					var nbPage = data.nbPage;
					
					for(var i = 0; i < nbPage; i++){
						var li = document.createElement("li");
						li.className = "page-item";
						var a = document.createElement("a");
						a.innerHTML = i+1;
						a.className = "getPage";
						parentNode.appendChild(li);
						li.appendChild(a);
					};

					var allPages = document.getElementsByClassName("getPage");

					

					for (var i = 0; i < allPages.length; i++) {
						allPages[i].addEventListener('click', getPageContent, false);
					}

				});

			} else{
				parentNode.remove();
				var apppendTo = document.getElementById("panel-show-data")
				var ulPagination = document.createElement("ul");
				ulPagination.id = "pagination";
				ulPagination.className = "pagination justify-content-center"
				apppendTo.appendChild(ulPagination);
				

			}
		});

		function getPageContent() {
			//class="active"
			$("li.active").each ( function() {
				console.log(this);
				this.className = "";
			});

			console.log(this.parentElement);
			this.parentElement.className = "active";
			var numPage = this.innerHTML-1 ;
			console.log(numPage);
			$.getJSON($SCRIPT_ROOT + 'show_page', {
				numPage: JSON.stringify(numPage),
				categories: JSON.stringify(categories),
				villes: JSON.stringify(villes),
				date: JSON.stringify(date),
				texte: JSON.stringify(full_texte),
				juridiction: JSON.stringify([]),
				quantumD: JSON.stringify(quantumD),
				quantumR: JSON.stringify(quantumR),
				resultat: JSON.stringify(resultats)
			}, function(data){
				console.log(data.result);
				updateTabel(data.result);

			});
		};

		/* Tree map */
		function build_tree(recordsJson){
			console.log("build_tree");
			var margin = {
				top: 20,
				right: 120,
				bottom: 20,
				left: 120
			},
			width = 1600 - margin.right - margin.left,
			height = 800 - margin.top - margin.bottom;

			var i = 0,
			j = 0,
			duration = 450,
			root,
			root2;

			var tree = d3.layout.tree()
			.size([height, width]);
			//tree2 = d3.layout.tree().size([height, width]);

			var diagonal = d3.svg.diagonal()
			.projection(function (d) {
				return [d.y, d.x];
			});

			var svg = d3.select("#tree_map").append("svg")
			//.attr("width", width + margin.right + margin.left)
			//.attr("height", height + margin.top + margin.bottom)
			.attr("width", "100%")
			.attr("height", "600px")
			.call(d3.behavior.zoom()
				.scaleExtent([0.7, 5])
				.on("zoom", function () {
					svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
				}))
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		//root is {name,parent,children}
		root = recordsJson.tree;
		root.x0 = height / 2;
		root.y0 = 0;

		function collapse(d) {
			if (d.children) {
				d._children = d.children;
				d._children.forEach(collapse);
				d.children = null;
			}
		}

		//use this command to visualize only the root and its first descendants in the start page
		//collapse(root);
		root.children.forEach(collapse);
		
		//update(tree2, root2, -500., -1, "nodeD", "linkD", j);
		update(root);

		d3.select(self.frameElement).style("height", "800px");

		function update(myroot) {

			// Compute the new tree layout.
			var nodes = tree.nodes(myroot).reverse(),
			links = tree.links(nodes);

			// Normalize for fixed-depth.

			nodes.forEach(function (d) {
				if(d.tree == "Villes" || d.tree == "Categories"  || d.tree == "Normes"){
					d.y = d.depth * 200;
				}else{
					d.y = d.depth * 170;
				}
			});

			// Add popup with number of occurrence
			var div = d3.select("body").append("div")   
			.attr("class", "tooltip")               
			.style("opacity", 0);

			// Update the nodes
			var node = svg.selectAll("g.node")
			.data(nodes, function (d) {
				return d.id || (d.id = ++i);
			});

			// Enter any new nodes at the parent's previous position.
			var nodeEnter = node.enter().append("g")
			.attr("class", "node")
			.attr("transform", function (d) {
				return "translate(" + (+myroot.y0) + "," + myroot.x0 + ")";
			})
			.on("click", click);

			nodeEnter.append("circle")
			.attr("r", 1e-6)
			.style("fill", function (d) {
				return d._children ? d.color : "#fff";
			});

			nodeEnter.append("text")
			.attr("x", function (d) {
				return d.children || d._children ? -15 : 15;
			})
			.attr("dy", ".10em")
			.attr("text-anchor", function (d) {
				return d.children || d._children ? "end" : "start";
			})
			.text(function (d) {
				if (d.name.length > 25 ){
					var words = d.name.split(" ");
						//console.log()
						return words[0]+" "+ words[1]+" "+words[3]+"...";

					} else
					{
						return d.name;
					}
				})  
			.on("mouseover", function(d) {
				if (d.name.length > 25){
					div.transition()        
					.duration(200)      
					.style("opacity", .9);      
					div.html(d.name + "<br/>")    
					.style("left", (d3.event.pageX) + "px")     
					.style("top", (d3.event.pageY - 28) + "px") 
					.style("width", "250px")
					.style("height", "35px");

				}
			}) 
			.on("mouseout", function(d) { 
				div.transition()        
				.duration(500)      
				.style("opacity", 0) 
			})
			.on("keydown", function () { console.log("div key", i); })   
			.style("fill-opacity", 1e-6);

			// Transition nodes to their new position.
			var nodeUpdate = node.transition()
			.duration(duration)
			.attr("transform", function (d) {
				return "translate(" + (+d.y) + "," + d.x + ")";
			});

			function normalize(max,dt,scaleTo){    
				var scale = d3.scale.linear().domain([1, max]).range([1, scaleTo]);
				//console.log(max+" "+dt+" "+scaleTo +" " +scale(dt));
				return scale(dt);
			}	

			nodeUpdate.select("circle")
			.attr("r",  function(d) {  
				if(d.tree != undefined){
					var toStroke = d.nb;
					if(toStroke>200){
						toStroke = 200;
					}
					return  normalize(200, toStroke, 15);
				}
				return d.children || d._children ? 14 : 10;})
			.style("fill", function (d) {
				return d._children ? d.color : "#fff";
			})
			.style("stroke", function(d) { return d.color; });


			nodeUpdate.select("text")
			.style("fill-opacity", 1);

			// Transition exiting nodes to the parent's new position.
			var nodeExit = node.exit().transition()
			.duration(duration)
			.attr("transform", function (d) {
				return "translate(" + myroot.y + "," + myroot.x + ")";
			})
			.remove();

			nodeExit.select("circle")
			.attr("r", 1e-6);

			nodeExit.select("text")
			.style("fill-opacity", 1e-6);

			// Update the links
			var link = svg.selectAll("path.link")
			.data(links, function (d) {
				return d.target.id;
			});

			// Enter any new links at the parent's previous position.
			link.enter().insert("path", "g")
			.attr("class", "link")
			.attr("d", function (d) {
				var o = {
					x: myroot.x0,
					y: myroot.y0
				};
				return diagonal({
					source: o,
					target: o
				});
			});
					  //Stroke and style links
			  //var stroke = 1;
			  link.style('stroke-width', function(d) {
			  	var tostroke = d.target.nb;
			  	if(tostroke>200){
			  		tostroke = 200;
			  	}
			  	var stroke = normalize(200,tostroke,20);
			  	return stroke+"px";
			  });

			  link.style('stroke', function(d) { return d.target.color; });
			  
			  link.on("mouseover", function(d) {
			  	this.style.opacity = 1;
			  	if (d.target.nb != undefined){  
			  		div.transition()        
			  		.duration(200)      
			  		.style("opacity", .9);      
			  		div .html(d.target.nb + "<br/>")
			  		.style("width", "60px")
			  		.style("height", "28px")    
			  		.style("left", (d3.event.pageX) + "px")     
			  		.style("top", (d3.event.pageY - 28) + "px");    

			  	}
			  })
			  .on("mouseout", function(d) { 
			  	this.style.opacity = 0.5;

			  	div.transition()        
			  	.duration(500)      
			  	.style("opacity", 0) });   

			// Transition links to their new position.
			link.transition()
			.duration(duration)
			.attr("d", diagonal);
			// Transition exiting nodes to the parent's new position.
			link.exit().transition()
			.duration(duration)
			.attr("d", function (d) {
				var o = {
					x: myroot.x,
					y: myroot.y
				};
				return diagonal({
					source: o,
					target: o
				});
			})
			.remove();

			// Stash the old positions for transition.
			nodes.forEach(function (d) {
				d.x0 = d.x;
			});
		}

		function build_histogram(dataq){
			
			dataq.quantums.forEach(function (d){
				d.quantum_demande = Math.round(Number(d.quantum_demande.replace(",",".").replace(/[^0-9\.]+/g,"")));
				d.quantum_resultat = Math.round(Number(d.quantum_resultat.replace(",",".").replace(/[^0-9\.]+/g,"")));
			})
			
			var data = dataq.quantums;//[{"date":"2012-03-20","total":3},{"date":"2012-03-21","total":8},{"date":"2012-03-22","total":2},{"date":"2012-03-23","total":10},{"date":"2012-03-24","total":5},{"date":"2012-03-25","total":20},{"date":"2012-03-26","total":12}];

			//var data1 = [{"date":"2012-03-20","total":8},{"date":"2012-03-21","total":2},{"date":"2012-03-22","total":1},{"date":"2012-03-23","total":14},{"date":"2012-03-24","total":3},{"date":"2012-03-25","total":2},{"date":"2012-03-26","total":10}];

			var margin = {top: 40, right: 40, bottom: 40, left:80},
			width = 700,
			height = 500;
			var nbTicks = 10;
			if(dataq.quantums.length < 10){
				nbTicks = dataq.quantums.length;
			} 
			var x = d3.time.scale()
				//console.log(new Date(data[0].date));
				.domain([new Date(data[0].date), d3.time.day.offset(new Date(data[data.length - 1].date), 1)])
				.rangeRound([0, width - margin.left - margin.right]);

				var y = d3.scale.linear()
				.domain([0, d3.max(data, function(d) { return d.quantum_demande; })])
				.range([height - margin.top - margin.bottom, 0]);

				var xAxis = d3.svg.axis()
				.scale(x)
				.orient('bottom')
				//.ticks(d3.time.days, 1)
				.ticks(nbTicks)
				.tickFormat(d3.time.format('%Y'))
				.tickSize(0)
				.tickPadding(8);

				var yAxis = d3.svg.axis()
				.scale(y)
				.orient('left')
				.tickFormat(function(d) { return d + "€"; })
				.tickPadding(8);

				var svg = d3.select('#histogram').append('svg')
				.attr('class', 'chart')
				.attr('width', width)
				.attr('height', height)
				.append('g')
				.attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

				svg.selectAll('.chart')
				.data(data)
				.enter().append('rect')
				.attr('class', 'bar')
				.attr('x', function(d) { return x(new Date(d.date)); })
				.attr('y', function(d) { return height - margin.top - margin.bottom - (height - margin.top - margin.bottom - y(d.quantum_demande)) })
				.attr('width', 10)
				.attr('height', function(d) { return height - margin.top - margin.bottom - y(d.quantum_demande) });
				
				svg.selectAll('.chart')
				.data(data)
				.enter().append('rect')
				.attr('class', 'bar1')
				.attr('x', function(d) { return x(new Date(d.date)); })
				.attr('y', function(d) { return height - margin.top - margin.bottom - (height - margin.top - margin.bottom - y(d.quantum_resultat)) })
				.attr('width', 10)
				.attr('height', function(d) { return height - margin.top - margin.bottom - y(d.quantum_resultat) });
				
				svg.append('g')
				.attr('class', 'x axis')
				.attr('transform', 'translate(0, ' + (height - margin.top - margin.bottom) + ')')
				.call(xAxis);

				svg.append('g')
				.attr('class', 'y axis')
				.call(yAxis);

				// add legend   
				svg.append("text")
				.attr('class', 'bar')
				.attr("y", "-10")
				.style('stroke', "0px")
				.text("Quantum demandé");

				svg.append("text")
				.attr('class', 'bar1')
				.attr("y", "-10") 
				.attr("x", "100") 
				.style('stroke', "0px")
				.text("Quantum resultat");
				
			}
		

		// Toggle children on click.
		function click(d) {
			function addChildren(type){
			$.getJSON($SCRIPT_ROOT + type, {
				resultat: JSON.stringify(resultat),
				norme: JSON.stringify(norme),
				objet: JSON.stringify(objet),
				date: JSON.stringify(date),
				texte: JSON.stringify(full_texte),
				villes: JSON.stringify(villes)
			}, function(data){
				data.tree.forEach(function(child){
					if (!tree.nodes(d)[0]._children){
						tree.nodes(d)[0]._children = [];
					}
					child.x = d.x0;
					child.y = d.y0;
					tree.nodes(d)[0]._children.push(child);
				});
				
				if (d.children) {
					d._children = d.children;
					d.children = 0;
				}
				else {
					d.children = d._children;
					d._children = 0;
				} 
				update(root);

			});	
		}

		function putVille(ville) {
			villes = [];
			
				if (Array.isArray(ville)) {
					ville.forEach(function (v) { 
					villes.push(v);
					});
					
				}else
				if (ville != "Filtres"){
				villes.push(ville);
				}
		}

			if (d.name == "Filtres"){
				//console.log(d.name);

				$("#dialog-filtres").dialog(
				{
					title: "Filtres",
					resizable: false,
					height: "auto",
					width: 600,
					position: { my: "center top", at: "center top", of: window },
					modal: true,
					buttons: {
						"Valider":{
							id: "filtreValide",
							text: "Valider",
							class: "btn btn-info",
							click: function(){
								search();
								$( this ).dialog( "close" );
							}  
						},
						"Annulrer":{ 
							text: "Annulrer",
							class: "btn btn-info",
							click: function() {
								$( this ).dialog( "close" );
							}
						}
					}

				}).dialog("open");


			}

			if (d.tree == "Villes" && d._children.length == 0 ){
				var ville = d.name;
				putVille(ville);
				addChildren('get_categorie');
			}

			if (d.tree == "Categories" && d._children.length == 0 ){	
				var objet = d.name,
				ville = d.parent.name;
				putVille(ville);
				
				addChildren('get_norme');
			}

			if (d.tree == "Normes" && d._children.length == 0 ){

				var norme = d.name,
				objet = d.parent.name,
				ville = d.parent.parent.name;
				
				putVille(ville);

				addChildren('get_resultat');
				
			}		

			if (d.tree == "Resultats"){
				var resultat = d.name,
				objet = d.parent.name,
				norme = d.parent.parent.name
				ville = d.parent.parent.parent.name;

				var div_histogram = document.getElementById("histogram");
				div_histogram.remove();
				var histogram_n = document.createElement("div");
				var parentNode = document.getElementById("dialog-quantum");
				histogram_n.id = "histogram";
				parentNode.appendChild(histogram_n);
				var text = document.createElement("div");

				text.innerHTML ="<i>Objet:</i> " +objet+", <i>norme:</i> "+ norme + ", <i>resultat:</i> " + resultat +".";
				histogram_n.appendChild(text);
				
				putVille(ville);

				$.getJSON($SCRIPT_ROOT + 'get_quantum', {
					resultat: JSON.stringify(resultat),
					norme: JSON.stringify(norme),
					objet: JSON.stringify(objet),
					date: JSON.stringify(date),
					texte: JSON.stringify(full_texte),
					villes: JSON.stringify(villes)
				}, function(data){
					//console.log(data);
					build_histogram(data);
					$("#dialog-quantum").dialog(
					{
						title: "Quantum demandé et quantum resultat",
						resizable: false,
						height: "auto",
						width: 750,
						position: { my: "center top", at: "center top", of: window },
						modal: true,
						buttons: {
							"Fermer":{ 
								text: "Fermer",
								class: "btn btn-info",
								click: function() {
									$( this ).dialog( "close" );
								}
							}
						}

					}).dialog("open");

				});
			}
			if (d.name != "Filtres"){ 
				if (d.children) {
					d._children = d.children;
					d.children = 0;
				} else {
					d.children = d._children;
					d._children = 0;
				}
				update(root);
			} 
		}

	}


};