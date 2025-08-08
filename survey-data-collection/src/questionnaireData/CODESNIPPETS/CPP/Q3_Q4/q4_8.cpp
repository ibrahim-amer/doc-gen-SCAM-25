/**
* Calculates and sets various node centrality measures for a given path based on nodes in the path.
*
* @param path A structure representing the path with various centrality measures.
* @param NODES_LIST A vector of node structures containing centrality measures for each node.
* @param TOTAL_TRAFFIC The total traffic value used for calculations of centrality measures.
* @return This function does not return a value; it modifies the path structure directly.
*/
void set_path_node_centrality_measures_S(path_struct &path, vector<node_struct> NODES_LIST,double TOTAL_TRAFFIC)
{

	//SIMPLE MEASURES (node centrality based)
	double degree_centrality=0;
	double routed_degree_centrality = 0;
	double routed_degree_centrality_normalized = 0;
	double eigenvector_centrality = 0;
	
	double routed_centrality = 0;
	double routed_centrality_normalized = 0;

	
	//COMPOUND MEASURES 
	double weighted_eigencentrality = 0.0;//Eigenvector centrality * node traffic ratio
	
	double log_centrality_node_A = 0.0;//log(BASE = traffic ratio, ARG = routed_centrality + 1 ) -- EXPERIMENTAL



//END TESTING


	int node_counter = 1;//test only: normalize wrt #nodes in each path | init to 1 to account for last node in the path!

	for (size_t i = 0; i < path.links_list.size(); i++)//for all links in the path
	{
		if (NODES_LIST[path.links_list[i].a_node_id].visited==false)
		{
			degree_centrality += NODES_LIST[path.links_list[i].a_node_id].degree_centrality;
			routed_degree_centrality +=NODES_LIST[path.links_list[i].a_node_id].routed_degree_centrality;
			routed_degree_centrality_normalized += NODES_LIST[path.links_list[i].a_node_id].routed_degree_centrality_normalized;
			eigenvector_centrality += NODES_LIST[path.links_list[i].a_node_id].eigenvector_centrality;

			routed_centrality += NODES_LIST[path.links_list[i].a_node_id].routed_centrality;
			//routed_centrality_normalized += NODES_LIST[path.links_list[i].a_node_id].routed_centrality_normalized;

			//COMPOUND MEASURES
			weighted_eigencentrality += NODES_LIST[path.links_list[i].a_node_id].weighted_eigencentrality;
			log_centrality_node_A += NODES_LIST[path.links_list[i].a_node_id].log_centrality_node_A;//EXPERIMENTAL


			node_counter++;//TEST ONLY: used for normalized versions of the KPI

		}
		NODES_LIST[path.links_list[i].a_node_id].visited=true;//mark node as visited so it is not counted twice
	}

	//handling LAST NODE in the path...
	degree_centrality += NODES_LIST[path.dst_id].degree_centrality;//add deg centrality for destination (last node in the path)	
	routed_degree_centrality += NODES_LIST[path.dst_id].routed_degree_centrality;//set for last node
	routed_degree_centrality_normalized += NODES_LIST[path.dst_id].routed_degree_centrality_normalized;//set for last node
	eigenvector_centrality += NODES_LIST[path.dst_id].eigenvector_centrality;//set for last node
	
	routed_centrality += NODES_LIST[path.dst_id].routed_centrality;//set for last node
	//routed_centrality_normalized += NODES_LIST[path.dst_id].routed_centrality_normalized;//set for last node

	//COMPOUND MEASURES
	weighted_eigencentrality += NODES_LIST[path.dst_id].weighted_eigencentrality;//set for last node
	log_centrality_node_A += NODES_LIST[path.dst_id].log_centrality_node_A;//EXPERIMENTAL




	//set values in path parameters --> NON-NORMALIZED
	path.N_degree_centrality_S = degree_centrality;
	path.N_routed_degree_centrality_S = routed_degree_centrality;
	path.N_routed_degree_centrality_normalized_S = routed_degree_centrality_normalized;
	path.N_eigenvector_centrality_S = eigenvector_centrality;

	path.N_routed_centrality_S = routed_centrality;

	//COMPOUND MEASURES
	path.N_weighted_eigencentrality_S = weighted_eigencentrality;
	path.N_log_centrality_node_A_S = log_centrality_node_A;//EXPERIMENTAL
	

	
	//NORMALIZED VERSIONS 
	path.N_degree_centrality_SN = degree_centrality/double(node_counter);
	path.N_routed_degree_centrality_SN = routed_degree_centrality/double(node_counter);
	path.N_routed_degree_centrality_normalized_SN = routed_degree_centrality_normalized/double(node_counter);
	path.N_eigenvector_centrality_SN = eigenvector_centrality/double(node_counter);

	path.N_routed_centrality_SN = routed_centrality/double(node_counter);

	//COMPOUND MEASURES
	path.N_weighted_eigencentrality_SN = weighted_eigencentrality/double(node_counter);
	path.N_log_centrality_node_A_SN = log_centrality_node_A/double(node_counter);//EXPERIMENTAL
}