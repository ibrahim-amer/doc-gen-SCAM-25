/**
* Computes traffic for each link based on routing matrix and traffic demands.
*
* @param ROUTING_MATRIX A matrix representing routing information for traffic.
* @param TRAFFIC_VECTOR A vector containing traffic demands for each link.
* @param links_list A reference to a list of link structures to store computed traffic.
*/
void forward_problem_OPT(vector< vector<double> > ROUTING_MATRIX,vector<demand_struct> TRAFFIC_VECTOR,vector<link_struct> &links_list)
{
	//vector<link_struct> LINK_TRAFFIC;
	link_struct AUX_link;

	for (size_t i = 0; i < ROUTING_MATRIX.size(); i++)//for every row of the routing matrix...
	{
		AUX_link.traffic = 0.0;//INITIALIZE: +1.0 added to compensate for link_struct.traffic being initialized to -1.0

		for (size_t j = 0; j < ROUTING_MATRIX[0].size(); j++)
			AUX_link.traffic += ROUTING_MATRIX[i][j]*TRAFFIC_VECTOR[j].traffic;//row by column_vector
		

		AUX_link.link_id = links_list[i].link_id;
		AUX_link.a_node_id = links_list[i].a_node_id;
		AUX_link.b_node_id = links_list[i].b_node_id;

		//stores computed link traffic in the corresponding variable in the main LINKS_LIST
		links_list[i].traffic_computed = AUX_link.traffic;

		//LINK_TRAFFIC.push_back(AUX_link);

		AUX_link = {};//reset		
	}
//	return LINK_TRAFFIC;
}