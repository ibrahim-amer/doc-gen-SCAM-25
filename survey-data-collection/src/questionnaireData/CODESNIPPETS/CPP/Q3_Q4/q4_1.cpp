
/**
* Computes traffic volumes based on routing matrices and known traffic data.
*
* @param routing_matrix_BR 2D vector representing the routing matrix for BR.
* @param routing_matrix_SD 2D vector representing the routing matrix for SD.
* @param links Vector of link_struct containing link information.
* @param PATHS_TABLE_BR Vector of path_struct for BR source-destination pairs.
* @param PATHS_TABLE_SD Vector of path_struct for SD source-destination pairs.
* @param KNOWN_TRAFFIC_MATRIX 2D vector representing known traffic volumes between pairs.
* @return A vector of implicit_demand_struct containing computed traffic volumes for each pair.
*/
vector<implicit_demand_struct> compute_traffic_volumes_V2(vector<vector<double>> routing_matrix_BR, vector<vector<double>> routing_matrix_SD, vector<link_struct> links, vector<path_struct> PATHS_TABLE_BR, vector<path_struct> PATHS_TABLE_SD, vector<vector<double>> KNOWN_TRAFFIC_MATRIX)
{
	bool match = true;

	double alpha = 0;
	double beta = 0;
	double epsilon = 0;//	--> min[ alpha, beta	]

	vector<implicit_demand_struct> traffic_volumes;//stores the results of the TV computations for all provided pairs
	implicit_demand_struct traffic_volumes_aux;//auxiliary variable for traffic volume of single pair


	for (size_t j = 0; j < routing_matrix_BR[0].size(); j++)//cycles through every column of BR
	{
		//cout << "\n\n\n Column BR --> " << j <<" \n" <<endl;//TEST

		//Initialize/Reset  current src/dst pair
		traffic_volumes_aux.src_id = PATHS_TABLE_BR[j].src_id;
		traffic_volumes_aux.dst_id = PATHS_TABLE_BR[j].dst_id;
		traffic_volumes_aux.traffic = 0;//initialize
		traffic_volumes_aux.visited = true;//mark as visited (unused, for now)


		epsilon = 0;//RESET

		for (size_t k = 0; k < routing_matrix_SD[0].size(); k++)//cycles through every column of SD
		{
			//cout << "\n\n\n Column SD --> " << k << " \n" << endl;//TEST
			match = true;//RESET

			for (size_t n = 0; n < routing_matrix_SD.size(); n++)//cycles through every row of SD/BR
			{

				if (((routing_matrix_BR[n][j] != 0) && (routing_matrix_SD[n][k] != 0)))
				{
					match = true;

					if (links[n].a_node_id == PATHS_TABLE_BR[j].src_id)//check for a_node_ID == src_ID and increment Alpha -- NEW
					{
						//cout << "SOURCE MATCH" << endl;//TEST
						//print_link(links[n]);//TEST

						alpha += routing_matrix_SD[n][k];//increment alpha
					}
					if (links[n].b_node_id == PATHS_TABLE_BR[j].dst_id)//check for a_node_ID == src_ID and increment beta -- NEW
					{
						//cout << "DESTINATION MATCH" << endl;//TEST
						//print_link(links[n]);//TEST

						beta += routing_matrix_SD[n][k];//increment beta
					}


				}
				else if ((routing_matrix_BR[n][j] != 0) && (routing_matrix_SD[n][k] == 0))//NEW
				{
					match = false;
					alpha = beta = epsilon = 0;//RESET - NEW
					break;//as soon as a mismatch is found --> skip column...
				}
			}
			if (match)
			{
				epsilon = (alpha < beta) ? alpha : beta;
			
				traffic_volumes_aux.traffic += epsilon * KNOWN_TRAFFIC_MATRIX[PATHS_TABLE_SD[k].src_id /*SRC*/][PATHS_TABLE_SD[k].dst_id  /*DST*/];

				//cout << "Traffic volume -->  " << traffic_volumes_aux.traffic << endl;//TEST

				//NEW
				demand_struct explicit_demand_tracker;

				explicit_demand_tracker.src_id = PATHS_TABLE_SD[k].src_id;
				explicit_demand_tracker.dst_id = PATHS_TABLE_SD[k].dst_id;				
				//Shows the portion of impacting traffic for each explicit demand
				explicit_demand_tracker.traffic = KNOWN_TRAFFIC_MATRIX[PATHS_TABLE_SD[k].src_id /*SRC*/][PATHS_TABLE_SD[k].dst_id  /*DST*/]*epsilon;

				traffic_volumes_aux.explicit_demands_list.push_back(explicit_demand_tracker);

				explicit_demand_tracker = {};//reset

				//END NEW



				alpha = beta = 0;//RESET
			}
		}
		traffic_volumes.push_back(traffic_volumes_aux);//store result

		//NEW
		traffic_volumes_aux.explicit_demands_list = {};//reset 
		//END NEW


	}
	return traffic_volumes;
}