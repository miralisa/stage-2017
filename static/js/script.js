	queue()
	.defer(d3.json, "/get_decisions/") //get a tree with children 'villes'
	.await(makeFilters);

	/* Create slider */
	function slider(){
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
	};

	/* Create map of France */
	function map() {
		var width = 400,
		height = 500;

		var projection = d3.geo.conicConformalFrance();

		var path = d3.geo.path()
		.projection(projection);

		var svg = d3.select("#map")
		.append("svg")
		.attr("width", width)
		.attr("height", height);

		d3.json("../static/input/france.json", function(error, regions) {
			var land = topojson.feature(regions, regions.objects.regions);

			svg.selectAll("path")
			.data(land.features)
			.enter()
			.append("path")
			.attr("d", path)
			.attr("class", "county-boundary");

			svg
			.append("path")
			.style("fill","none")
			.style("stroke","rgb(189, 185, 185)")
			.attr("d", projection.getCompositionBorders());


		});
		var tooltip = d3.select("body").append("div")   
		.attr("class", "tooltip")               
		.style("opacity", 0);

		d3.csv('../static/input/villes.csv', function(data) {
			svg.selectAll("circle")
			.data(data)
			.enter()
			.append("circle")
			.attr("cx", function(d) {
				return projection([d.lng, d.lat])[0];
			})
			.attr("cy", function(d) {
				return projection([d.lng, d.lat])[1];
			})
			.attr("r", 4)
			.style("fill", "#0582ff")
			.on("mouseover", function(d) {

				tooltip.transition()        
				.duration(200)      
				.style("opacity", .9)     
				tooltip.html(d.city)
				.style("width", "65px")
				.style("height", "26px")    
				.style("left", (d3.event.pageX) + "px")     
				.style("top", (d3.event.pageY - 26) + "px");    


			})
			.on("mouseout", function(d) { 
				tooltip.transition()        
				.duration(500)      
				.style("opacity", 0) 
			})
			.on("click", function(d) {
				if(this.style.fill !="rgb(5, 130, 255)"){
					this.style = "fill:#0582ff";
				} else {
					this.style = "fill:#4e9903";
				}
			});
		});

	};

	function buildHistogram(dataq){
		/* normalise data */
		dataq.quantums.forEach(function (d){
			d.quantum_demande = Math.round(Number(d.quantum_demande.replace(",",".").replace(/[^0-9\.]+/g,"")));
			d.quantum_resultat = Math.round(Number(d.quantum_resultat.replace(",",".").replace(/[^0-9\.]+/g,"")));
		})

		var data = dataq.quantums;

		var margin = {top: 40, right: 40, bottom: 40, left:80},
		width = 700,
		height = 500;
		var nbTicks = 10;
		if(dataq.quantums.length < 10){
			nbTicks = dataq.quantums.length;
		}

		var tooltip = d3.select("body").append("div")   
		.attr("class", "tooltip")               
		.style("opacity", 0);

		var x = d3.time.scale()
		.domain([new Date(data[0].date), d3.time.day.offset(new Date(data[data.length - 1].date), 1)])
		.rangeRound([0, width - margin.left - margin.right]);

		var y = d3.scale.linear()
		.domain([0, d3.max(data, function(d) { return d.quantum_demande; })])
		.range([height - margin.top - margin.bottom, 0]);

		var xAxis = d3.svg.axis()
		.scale(x)
		.orient('bottom')
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
		/* quantum_demande bars */
		svg.selectAll('.chart')
		.data(data)
		.enter().append('rect')
		.attr('class', 'bar')
		.attr('x', function(d) { return x(new Date(d.date)); })
		.attr('y', function(d) { return height - margin.top - margin.bottom - (height - margin.top - margin.bottom - y(d.quantum_demande)) })
		.attr('width', 10)
		.attr('height', function(d) { return height - margin.top - margin.bottom - y(d.quantum_demande) })
		.on("mouseover", function(d) {
			tooltip.transition()        
			.duration(200)      
			.style("opacity", .9);      
			tooltip.html(d.quantum_demande + " €")    
			.style("left", (d3.event.pageX) + "px")     
			.style("top", (d3.event.pageY - 28) + "px")
			.style("background", "#cccce5")
			.style("opacity", .3)
			.style("width", "100px")
			.style("height", "25px");

		})
		.on("mouseout", function(d) { 
			tooltip.transition()        
			.duration(500)      
			.style("opacity", 0) 
		});

		/* quantum_result bars */
		svg.selectAll('.chart')
		.data(data)
		.enter().append('rect')
		.attr('class', 'bar1')
		.attr('x', function(d) { return x(new Date(d.date)); })
		.attr('y', function(d) { return height - margin.top - margin.bottom - (height - margin.top - margin.bottom - y(d.quantum_resultat)) })
		.attr('width', 10)
		.attr('height', function(d) { return height - margin.top - margin.bottom - y(d.quantum_resultat) })
		.on("mouseover", function(d) {
			tooltip.transition()        
			.duration(200)      
			.style("opacity", .9);      
			tooltip.html(d.quantum_resultat + " €")    
			.style("left", (d3.event.pageX) + "px")     
			.style("top", (d3.event.pageY - 28) + "px")
			.style("background", "#99cc99")
			.style("opacity", .3)
			.style("width", "100px")
			.style("height", "25px");

		})
		.on("mouseout", function(d) { 
			tooltip.transition()        
			.duration(500)      
			.style("opacity", 0) 
		});

		svg.append('g')
		.attr('class', 'x axis')
		.attr('transform', 'translate(0, ' + (height - margin.top - margin.bottom) + ')')
		.call(xAxis);

		svg.append('g')
		.attr('class', 'y axis')
		.call(yAxis);

		/* add legend */  
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

	};

	/* Update tabel of search results */
	function updateTabel(data){
		var tbody = $('#tbody');
		tbody.empty();
		data.forEach(function(decision) {
			var tr = $('<tr/>').appendTo(tbody);

			tr.append('<td>' + decision[1] + '</td>');
			tr.append('<td>' + decision[2] + '</td>');
			tr.append('<td>' + decision[3] + '</td>');
			tr.append('<td>' + decision[4] + '</td>');
			tr.append('<td>' + decision[7] + '</td>');
			tr.append('<td>' + decision[8] + '</td>');
			tr.append('<td>' + decision[14] + '</td>');
			tr.append('<td>' + decision[16] + '</td>');
			tr.append('<td>' + decision[9] + '</td>');
			
			/* delete " in description */
			var splDec = decision[5].split("\"");
			var appendDec = '';
			splDec.forEach(function(elem) {
				appendDec += elem;

			});
			
			tr.append("<td>  <a href='#' title=\" "+ appendDec + " \" onclick=\"openDescription(this)\" > Voir </a> </td>");

		})
	};

	
	function makeFilters(error, decisions) {
		if(error) console.log(error);

		buildTree(decisions);
		map();
		slider();
		/* declaration of variables for filters */
		var categories = [],
		villes = [],
		date = [],
		full_texte = "";



		var count = 0;
		/* event listener on  "createGroupe" button: select all green circles and store in array "ville" and then display
		them in p tag  */
		document.getElementById("createGroupe").onclick = function() {
			villes = [];
			var svg = d3.select("#map");

			var villesData = svg.selectAll('[style = "fill: rgb(78, 153, 3);"]').data();
			villesData.forEach( function(v) {
				villes.push(v.city);
			});
			count++;

			var p = document.createElement("p");
			var parentNode = document.getElementById("groups");
			p.id = count;
			p.innerHTML = "Groupe "+count+": "+villes ;
			parentNode.appendChild(p);

			svg.selectAll("circle").style("fill", "#0582ff");
		}

		/* deselect all "ville" */
		document.getElementById("deselectAllV").onclick = function() {
			var svg = d3.select("#map");
			svg.selectAll("circle").style("fill", "#0582ff");
		}

		/* select all "ville" */
		document.getElementById("selectAllV").onclick = function() {
			var svg = d3.select("#map");		
			svg.selectAll("circle").style("fill", "#4e9903");
		};

		/* clear filters*/
		$('#clearFiltres').click(function(){
			/* cleaar date */
			$( "#slider" ).slider( "values", 0, 1990 );
			$( "#slider" ).slider( "values", 1, 2017 );
			$( "#date" ).val( " entre " + $( "#slider" ).slider( "values", 0 ) + " et " + $( "#slider" ).slider( "values", 1 ) + " " );
			/* clear groups of "villes" */
			count = 0;
			var pNode = document.getElementById("groups");
			while (pNode.firstChild) {
				pNode.removeChild(pNode.firstChild);
			}
			/* clear full text input field */
			var inputFullTexte = document.getElementById("searchByKW");
			inputFullTexte.value = "";
			/* clear map: deselect "villes" */
			var svg = d3.select("#map");
			svg.selectAll("circle").style("fill", "#0582ff");

		});
		


		function search(){
			//by date
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

			//by key words
			full_texte = "";
			var inputFullTexte = document.getElementById("searchByKW").value;
			full_texte = inputFullTexte;
			
			//by city
			villes=[];
			var svg = d3.select("#map");
			
			var villesData = svg.selectAll('[style = "fill: rgb(78, 153, 3);"]').data();
			villesData.forEach( function(v) {
				villes.push(v.city);
			});
			
			// add groups of cities
			var groups = []
			if(document.getElementById("groups").hasChildNodes()){

				for(var i = 1; i <= document.getElementById("groups").childNodes.length; i++){
					var group = document.getElementById(i).innerHTML;
					var pos = group.indexOf(":") + 2;
					groups.push(group.slice(pos, group.length));
				}
			}
			
			/* define parameter of sorting results */		
			var categorie = document.getElementById("sortTreeCategorie").checked;
			var ville = document.getElementById("sortTreeVille").checked;
			var root_search = '/sortByCategorie/';
			if (ville){
				root_search = '/sortByVille/';
			}
			if(groups.length != 0){
				villes = [];
				root_search = '/groupVille/';
			}
			/* send request */
			$.getJSON($SCRIPT_ROOT + root_search, {
				//categories: JSON.stringify(categories),
				villes: JSON.stringify(villes),
				date: JSON.stringify(date),
				texte: JSON.stringify(full_texte),
				groups: JSON.stringify(groups),
				//juridiction: JSON.stringify([]),
				//quantumD: JSON.stringify(quantumD),
				//quantumR: JSON.stringify(quantumR),
				//resultat: JSON.stringify(resultats)
			}, function(data){
				/* display choosen filers and number of search results */
				var showRes = document.getElementById("resultat");
				var inputFullTexte = document.getElementById("searchByKW").value;
				var parametreRecherche = " <br> Recherche effectuée: ";
				
				if(date1 >= 1990 && date2 <= 2017){
					if (date1 == date2) {
						parametreRecherche+="<strong>date</strong> <i>" +date1+"</i>";

					} else{
						parametreRecherche+="<strong>date</strong> entre <i>" +date1+"</i> et <i>"+date2+"</i> ";
					}
				}

				if (inputFullTexte != ""){
					parametreRecherche+="<strong>mot-clé</strong> <i>"+inputFullTexte+"</i> ";
				}

				if(data.tree.nb == 0){
					showRes.style="display: ;"
					showRes.innerHTML = "Désolé, aucun résultat ne correspond pas à votre recherche."+parametreRecherche;
				}else{

					showRes.style="display: ;"
					showRes.innerHTML = "Voici "+ data.tree.nb+" demande(s) correspondant à votre recherche."+parametreRecherche;//<strong>"+ data.tree.nb+ "</strong>

				}
				/* remove old tree */
				var div_tree = document.getElementById("tree_map");
				div_tree.remove();
				var histogram_n = document.createElement("div");
				var parentNode = document.getElementById("popup");
				histogram_n.id = "tree_map";
				parentNode.appendChild(histogram_n);
				
				/* build tree with search results*/
				buildTree(data);
				/* if */
				var isExpanded = $("#showResultsTabel").attr("aria-expanded");
				if( isExpanded == 'true'){
					$("#showResultsTabel").click();
				}	

			});

		}
		
		/* Pagination */ 
		$("#showResultsTabel").click(function() {
			var isExpanded = $("#showResultsTabel").attr("aria-expanded");
			var parentNode = document.getElementById("pagination");
			
			if(isExpanded == 'false' || isExpanded == undefined)
			{
				$.getJSON($SCRIPT_ROOT + 'show_text', {
					villes: JSON.stringify(villes),
					date: JSON.stringify(date),
					texte: JSON.stringify(full_texte)
				}, function(data){

					updateTabel(data.result);
					var nbPage = data.nbPage;
					/* create page links */
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
				$("li.active").each ( function() {
					this.className = "";
				});
				this.parentElement.className = "active";
				var numPage = this.innerHTML-1 ;
				$.getJSON($SCRIPT_ROOT + 'show_page', {
					numPage: JSON.stringify(numPage),
					villes: JSON.stringify(villes),
					date: JSON.stringify(date),
					texte: JSON.stringify(full_texte)
				}, function(data){
					updateTabel(data.result);

				});
			};
		

		/* Build tree */
		function buildTree(decisions){
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
			root;
			/* create tree layout */
			var tree = d3.layout.tree()
			.size([height, width]);

			/* links */
			var diagonal = d3.svg.diagonal()
			.projection(function (d) {
				return [d.y, d.x];
			});

			var svg = d3.select("#tree_map").append("svg")
			.attr("width", "100%")
			.attr("height", "600px")
			.call(d3.behavior.zoom()
				.scaleExtent([0.7, 5])
				.on("zoom", function () {
					svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
				}))
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

			root = decisions.tree;
			root.x0 = height / 2;
			root.y0 = 0;

			function collapse(d) {
				if (d.children) {
					d._children = d.children;
					d._children.forEach(collapse);
					d.children = null;
				}
			};

			//visualize only the root and its first descendants
			//collapse(root);
			root.children.forEach(collapse);
			
			update(root);

			d3.select(self.frameElement).style("height", "800px");

			function update(myroot) {

				// compute the new tree layout
				var nodes = tree.nodes(myroot).reverse(),
				links = tree.links(nodes);

				// normalize for fixed-depth
				nodes.forEach(function (d) {
					if(d.tree == "Villes" || d.tree == "Categories"  || d.tree == "Normes"){
						d.y = d.depth * 200;
					}else{
						d.y = d.depth * 170;
					}
				});

				// add popup with number of occurrence
				var div = d3.select("body").append("div")   
				.attr("class", "tooltip")               
				.style("opacity", 0);

				// update the nodes
				var node = svg.selectAll("g.node")
				.data(nodes, function (d) {
					return d.id || (d.id = ++i);
				});

				// enter any new nodes at the parent's previous position
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
						return words[0]+" "+ words[1]+" "+words[3]+"...";
					} else {
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
				.style("fill-opacity", 1e-6);

				// transition nodes to their new position
				var nodeUpdate = node.transition()
				.duration(duration)
				.attr("transform", function (d) {
					return "translate(" + (+d.y) + "," + d.x + ")";
				});

				function normalize(max,dt,scaleTo){    
					var scale = d3.scale.linear().domain([1, max]).range([1, scaleTo]);
					return scale(dt);
				};

				nodeUpdate.select("circle")
				.attr("r",  function(d) {  
					if(d.tree != undefined){
						var toStroke = d.nb;
						if(toStroke > 200){
							toStroke = 200;
						}
						return normalize(200, toStroke, 15);
					}
					return d.children || d._children ? 14 : 10;
				})
				.style("fill", function (d) {
					return d._children ? d.color : "#fff";
				})
				.style("stroke", function(d) { return d.color; });


				nodeUpdate.select("text")
				.style("fill-opacity", 1);

				// transition exiting nodes to the parent's new position
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

				// update the links
				var link = svg.selectAll("path.link")
				.data(links, function (d) {
					return d.target.id;
				});

				// enter any new links at the parent's previous position
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

				// stroke and style links
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

				// transition links to their new position
				link.transition()
				.duration(duration)
				.attr("d", diagonal);
				// transition exiting nodes to the parent's new position
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

				// stash the old positions for transition
				nodes.forEach(function (d) {
					d.x0 = d.x;
				});

			};

		// toggle children on click
		function click(d) {
			/* update tree : add new children */
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
			};

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
			};

			if (d.name == "Filtres"){

				$("#dialog-filtres").dialog(
				{
					title: "Filtres",
					resizable: false,
					height: "auto",
					width: 600,
					position: { my: "center top", at: "center top+55", of: window },
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
					buildHistogram(data);
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