	queue()
	.defer(d3.json, "/all_decisions/")
	.await(makeGraphs);

	function makeGraphs(error,recordsJson) {
		if(error) console.log(error);

		$("td").tooltip({tooltipClass: "custom-tooltip"});

		console.log(recordsJson);
		build_tree(recordsJson);

		document.getElementById("deselectAll").onclick = function() {deselectAll("categories")};
		document.getElementById("selectAll").onclick = function() {selectAll("categories")};
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
				var child = document.getElementById("entre_date");
				
				if(child!=null){
					console.log("remove "+child);

					parentNode.removeChild(child);
				}
			}
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
				tr.append('<td>' + decision[9] + '</td>');
				tr.append('<td>' + decision[10] + '</td>');
				tr.append("<td>  <a href='#' title=\""+ decision[5] + "\">+</a> </td>");

			})
		};

		function search(){
			$.getJSON($SCRIPT_ROOT + '/search/', {
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

				if(data.result.length == 0){
					showRes.style="display: ;"
					showRes.innerHTML = "Désolé, aucun résultat ne correspond pas à votre recherche."
				}else{
					showRes.style="display: ;"
					showRes.innerHTML = "Voici <strong>"+ data.result.length+ "</strong> demande(s) correspondant à votre recherche. "

				}
				console.log(data);
				updateTabel(data.result);

				var div_tree = document.getElementById("tree-container");
				console.log(div_tree);
				div_tree.remove();//(div_tree.childNodes[0]);
				
				var div_tree_n = document.createElement("div");
				var parentNode = document.getElementById("popup");
				div_tree_n.id = "tree-container"
				parentNode.appendChild(div_tree_n);
				
				if(data.children !=null){   
					build_tree(data);
				} else{
					console.log(recordsJson);
					
					build_tree(recordsJson);

				}
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



/*
		$.getJSON($SCRIPT_ROOT + '/searchByCity/', {
				villes: JSON.stringify(villes)
			}, function(data){
				updateTabel(data.result);
				// $( "table" ).text(data.result);
			});

			*/

		});
/*
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
			tr.append('<td>' + decision[6] + '</td>');
			tr.append('<td>' + decision[7] + '</td>');
			tr.append('<td>' + decision[8] + '</td>');
			tr.append('<td>' + decision[9] + '</td>');
			
		})
	};
	*/
	/* Tree map */
	function build_tree(recordsJson){
		var margin = {
		    top: 20,
		    right: 120,
		    bottom: 20,
		    left: 120
		},
		    width = 1200 - margin.right - margin.left,
		    height = 500 - margin.top - margin.bottom;

		var i = 0,
		    j = 0,
		    duration = 750,
		    root,
		    root2;

		var tree = d3.layout.tree()
		    .size([height, width]),
		    tree2 = d3.layout.tree()
		        .size([height, width]);

		var diagonal = d3.svg.diagonal()
		    .projection(function (d) {
		    return [d.y, d.x];
		});

		var svg = d3.select("#tree_map").append("svg")
		    //.attr("width", width + margin.right + margin.left)
		    //.attr("height", height + margin.top + margin.bottom)
		    .attr("width", "100%")
		    .attr("height", "800px")
		    .call(d3.behavior.zoom()
		        .scaleExtent([0.7, 50])
		        .on("zoom", function () {
		        svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
		    }))
		    .append("g")
		    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		//root is {name,parent,children}
		root = recordsJson.tree;
		root.x0 = height / 2;
		root.y0 = 0;

		root2 = recordsJson.tree2;
		root2.x0 = height / 2;
		root2.y0 = 0;

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

		root2.children.forEach(collapse);
		update(tree2, root2, -500., -1, "nodeD", "linkD", j);
		update(tree, root, -500, 1, "nodeA", "linkA", i);

		d3.select(self.frameElement).style("height", "800px");

		// Function to center node when clicked/dropped so node doesn't get lost when collapsing/moving with large amount of children.
		function centerNode(source) {
		    x = -source.y0;
		    y = -source.x0;
		    x = x + width / 2;
		    y = y + height / 2;
		    d3.select('g').transition()
		        .duration(duration)
		        .attr("transform", "translate(" + x + "," + y + ")");
		    //zoomListener.translate([x, y]);
		}

		function update(mytree, myroot, position, symmetry, myclass, mylinks, ii) {

		    // Compute the new tree layout.
		    var nodes = mytree.nodes(myroot).reverse(),
		        links = mytree.links(nodes);

		    // Normalize for fixed-depth.
		    nodes.forEach(function (d) {
		        d.y = symmetry * d.depth * 180;
		    });

		    // Add popup with number of occurrence
		    var div = d3.select("body").append("div")   
		    .attr("class", "tooltip")               
		    .style("opacity", 0);

		    // Update the nodes
		    var node = svg.selectAll("g." + myclass)
		        .data(nodes, function (d) {
		        return d.id || (d.id = ++ii);
		    });

		    // Enter any new nodes at the parent's previous position.
		    var nodeEnter = node.enter().append("g")
		        .attr("class", myclass)
		        .attr("transform", function (d) {
		         return "translate(" + (+myroot.y0 - position) + "," + myroot.x0 + ")";
		    })
		        .on("click", function (d) {
		        return click(d, tree, myroot, position, symmetry, myclass, mylinks, ii);
		    });

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
		        return d.name;
		    })      
		        .style("fill-opacity", 1e-6);

		    // Transition nodes to their new position.
		    var nodeUpdate = node.transition()
		        .duration(duration)
		        .attr("transform", function (d) {
		        return "translate(" + (+d.y - position) + "," + d.x + ")";
		    });

		    nodeUpdate.select("circle")
		        .attr("r",  function(d) {  return d.children || d._children ? 10 : 8;})
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
		    var link = svg.selectAll("path." + mylinks)
		        .data(links, function (d) {
		        return d.target.id;
		    });

		    // Enter any new links at the parent's previous position.
		    link.enter().insert("path", "g")
		        .attr("class", mylinks)
		        .attr("d", function (d) {
		        var o = {
		            x: myroot.x0,
		            y: myroot.y0
		        };
		        return diagonal({
		            source: o,
		            target: o
		        });
		    })
		        .attr("transform", function (d) {
		        return "translate(" + (-position) + ",0)";
		    });
		      //Stroke and style links
		      //var stroke = 1;
		      link.style('stroke-width', function(d) {
		        var tostroke = d.target.nb;
		        var stroke = '';
		        if( tostroke!='undefined' && tostroke > 200){
		            stroke = tostroke/22;
		        } else  if(tostroke < 100 && tostroke > 10){
		            stroke = tostroke/5;
		        }else  if(tostroke < 200 && tostroke > 100){
		            stroke = tostroke/10;
		        }
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
		function click(d, mytree, myroot, position, symmetry, myclass, mylinks, ii) {
		    if (d.children) {
		        d._children = d.children;
		        d.children = null;
		    } else {
		        d.children = d._children;
		        d._children = null;
		    }
		    update(mytree, myroot, position, symmetry, myclass, mylinks, ii);
		    //centerNode(root);
		    //centerNode(root2);
		} 

	}


};