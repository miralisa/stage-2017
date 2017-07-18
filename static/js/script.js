	queue()
	.defer(d3.json, "/all_decisions/")
	.await(makeGraphs);

	function makeGraphs(error,recordsJson) {
		if(error) console.log(error);

		$("td").tooltip({tooltipClass: "custom-tooltip"});

		console.log(recordsJson);
		build_tree(recordsJson);


		//document.getElementById("deselectAll").onclick = function() {deselectAll("categories")};
		//document.getElementById("selectAll").onclick = function() {selectAll("categories")};
		document.getElementById("deselectAllV").onclick = function() {deselectAll("villes")};
		document.getElementById("selectAllV").onclick = function() {selectAll("villes")};

		document.getElementById("removeFullTexte").onclick = function() {
			document.getElementById("searchByKW").value = "";
			full_texte ="";
			document.getElementById("fltrMotCle").style = "display:none";
			search();


		};

		document.getElementById("editFullTexte").onclick = function() {
			editFilters("motCle");  
		};

		document.getElementById("removeCategories").onclick = function() {
			deselectAll("categories");
			document.getElementById("searchByCategory").click();

		};

		document.getElementById("editCategories").onclick = function() {
			editFilters("categories");
		};

		document.getElementById("removeVilles").onclick = function() {
			deselectAll("villes");
			document.getElementById("searchByCity").click();

		};

		document.getElementById("editVilles").onclick = function() {
			editFilters("villes");  
		};

		document.getElementById("removeResultats").onclick = function() {
			deselectAll("resultats");
			document.getElementById("searchByResultat").click();

		};

		document.getElementById("editResultats").onclick = function() {
			editFilters("resultats");

		};

		document.getElementById("removeDate").onclick = function() {
			var res1 = document.getElementById("date1");
			var res2 = document.getElementById("date2");
			if(res2!=null){
				res2.value = "";
			}
			res1.value = "";
			date = [];
			search();
			document.getElementById("fltrDate").style = "display:none";
			//document.getElementById("searchByDate").click();

		};

		document.getElementById("editDate").onclick = function() {
			editFilters("date");

		};

		function editFilters(type){
			var isExpanded = $("#filtres").attr("aria-expanded");

			if(isExpanded == 'false')
			{
				document.getElementById("showFiltres").click();
			}
			document.getElementById(type).click();

		}

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
			
			inputDate.value = "";
			inputFullTexte.value = "";
			deselectAll("villes");
			


		});
		
		
		

		$('#searchByDate').click(function(){
			date = [];

			var cond_date = document.getElementById("sel_cond_date").value;
			var res1 = document.getElementById("date1").value;
			console.log(res1);
			date.push(cond_date);

			if (cond_date == "entre"){
				var res2 = document.getElementById("date2").value;
				date.push(res2);
			}
			date.push(res1);
			console.log(date.length);

			if(res1 == ""){
				document.getElementById("fltrDate").style = "display:none";
			}else{
				document.getElementById("fltrDate").style = "display:";

			}
			if(res1!=""){
				search();

			}
			
		});
		
		$('#searchByKeyWord').click(function(){
			full_texte = "";
			var inputFullTexte = document.getElementById("searchByKW").value;
			console.log("click " + inputFullTexte);
			full_texte = inputFullTexte;
			if(full_texte.length == 0){
				document.getElementById("fltrMotCle").style = "display:none";
			}else{
				document.getElementById("fltrMotCle").style = "display:";
				search();
			}
			

		});

		$('#searchByResultat').click(function(){
			resultats = [];
			$("input[type=checkbox]:checked", ".resultats").each ( function() {
				console.log($(this).val());
				resultats.push($(this).val());

			});

			if(resultats.length == 0){
				document.getElementById("fltrResultats").style = "display:none";
			}else{
				document.getElementById("fltrResultats").style = "display:";

			}
			search();

		});


		

		$("#searchByCategory").click(function() {
			categories=[];

			$("input[type=checkbox]:checked", ".categories").each ( function() {
				console.log($(this).val());
				categories.push($(this).val());

			});
			console.log("categories.length "+categories.length);

			if(categories.length == 0){
				document.getElementById("fltrCategories").style = "display:none";
			}else{
				document.getElementById("fltrCategories").style = "display:";

			}

			search();

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
				
				tr.append("<td>  <a href='#' title=\" "+ appendDec + " \" onclick=\"openDescription(this)\" > Voir </a> </td>");

			})
		};

		function search(){
			//par date
			date = [];


			var cond_date = document.getElementById("sel_cond_date").value;
			var res1 = document.getElementById("date1").value;
			console.log(res1);
			
			if(res1 !=""){
				date.push(cond_date);

			if (cond_date == "entre"){
				var res2 = document.getElementById("date2").value;
				date.push(res2);
			}
			date.push(res1);
			console.log(date.length);
			}
			if(res1!=""){
				//search();

			}

			//par mot-cle
			full_texte = "";
			var inputFullTexte = document.getElementById("searchByKW").value;
			console.log("click " + inputFullTexte);
			full_texte = inputFullTexte;
			

			//par ville
			villes=[];

			$("input[type=checkbox]:checked", ".villes").each ( function() {
				villes.push($(this).val());

			});

			if(villes.length==0){
				$("input[type=checkbox]", ".villes").each ( function() {
					villes.push($(this).val());

				});
			}
			

			$.getJSON($SCRIPT_ROOT + '/filtres/', {
				categories: JSON.stringify(categories),
				villes: JSON.stringify(villes),
				date: JSON.stringify(date),
				texte: JSON.stringify(full_texte),
				juridiction: JSON.stringify([]),
				quantumD: JSON.stringify(quantumD),
				quantumR: JSON.stringify(quantumR),
				resultat: JSON.stringify(resultats)
			}, function(data){
				var showRes = document.getElementById("resultat");

				var inputDate = document.getElementById("date1").value;
				var inputFullTexte = document.getElementById("searchByKW").value;
				var condDate = document.getElementById("sel_cond_date").value;
				var parametreRecherche = " <br> Recherche effectuée: ";
				if (inputDate != ""){
					if (condDate !="entre"){
						parametreRecherche+="<strong>date</strong> " +condDate+" <i>"+inputDate+"</i> ";
					} else{
						var inputDate2 = document.getElementById("date2").value;
						parametreRecherche+="<strong>date</strong> " + condDate+" <i>"+inputDate+"</i> et <i>"+inputDate2+"</i> ";
					}
				}
				if (inputFullTexte != ""){
					parametreRecherche+="<strong>mot-clé</strong> <i>"+inputFullTexte+"</i> ";
				}
		
				if(data.result.length == 0){
					showRes.style="display: ;"
					showRes.innerHTML = "Désolé, aucun résultat ne correspond pas à votre recherche."+parametreRecherche;
				}else{

					showRes.style="display: ;"
					showRes.innerHTML = "Voici <strong>"+ data.result.length+ "</strong> demande(s) correspondant à votre recherche."+parametreRecherche;

				}
				console.log(data);
				updateTabel(data.result);

				var div_tree = document.getElementById("tree_map");
				console.log(div_tree);
				div_tree.remove();//(div_tree.childNodes[0]);
				
				var div_tree_n = document.createElement("div");
				var parentNode = document.getElementById("popup");
				div_tree_n.id = "tree_map";
				parentNode.appendChild(div_tree_n);
				
				build_tree(data);
				/*
				if(data.children !=null){   
					build_tree(data.tree);
				} else{
					console.log(recordsJson.tree);
					
					build_tree(recordsJson);

				}*/
				// $( "table" ).text(data.result);
			//}
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


		$("#filtreValide").click(function() {
			console.log("click valider");
		});

		document.getElementById("sel_cond_date").onchange = function() {
			var inputDate = document.createElement("input");
			var parentNode = document.getElementById("form_date");
			if(this.value=="entre"){
				inputDate.className = "form-control input-sm";
				inputDate.type = "date";
				inputDate.id = "date2";
				inputDate.placeholder = "aaaa-mm-jj";
				parentNode.appendChild(inputDate);
			} else{
				var child = document.getElementById("date2");
				
				if(child!=null){
					console.log("remove "+child);

					parentNode.removeChild(child);
				}
			}
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
/*
		root2 = recordsJson.tree2;
		root2.x0 = height / 2;
		root2.y0 = 0;
*/
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

		    //Add popup button
		    /*
		    var button = d3.select("body").append("button").attr("type","button")   
		    .attr("class", "tooltip")               
		    .style("opacity", 0);
			*/

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
		    /*
		    	.on("mouseover", function(d) {
		    		if(d.name =="Filtres"){
		    	   	    div.transition()        
		    	        .duration(200)      
		    	        .style("opacity", .9);      
		    	        div.html(d.name + "<br/>")    
		    	        .style("left", (d3.event.pageX -128) + "px")     
		    	        .style("top", (d3.event.pageY - 28) + "px") 
		    	        .style("width", "150px")
		    	        .style("height", "35px");
		    	    }

		    	}) 
		    	.on("mouseout", function(d) {  
		    	  div.transition()        
		    	  .duration(500)      
		    	  .style("opacity", 0) 
		    	}); */

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
		        	if (d.name.length > 25){
		        		var words = d.name.split(" ");
		        		//console.log()
		        		 return words[0]+" "+ words[1]+" "+words[3]+"...";

		        	} else{
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
		        /*
		        if( tostroke!='undefined' && tostroke > 200){
		            stroke = tostroke/22;
		        } else  if(tostroke < 100 && tostroke > 10){
		            stroke = tostroke/5;
		        }else  if(tostroke < 200 && tostroke > 100){
		            stroke = tostroke/10;
		        }*/
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

		// Toggle children on click.
		function click(d) {

			if (d.name == "Filtres"){
				//console.log(d.name);

				$("#dialog-filtres").dialog(
					{
					title: "Filtres",
					resizable: false,
					height: "auto",
					width: 500,
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


			} else{


		    if (d.children) {
		        d._children = d.children;
		        d.children = null;
		    } else {
		        d.children = d._children;
		        d._children = null;
		    }
		    update(root);
		} 
	}

	}


};