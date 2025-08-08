/**
* Calculates the sum of weights for links associated with a specific node ID.
*
* @param links_list A vector of link_struct containing weights and node IDs.
* @param node_id The ID of the node for which weights are summed.
* @return The total sum of weights for unvisited links associated with the node ID.
*/
double sum_weights_end_node(vector<link_struct> links_list, int node_id)
{
	double sum_weights = 0;

	for (size_t j = 0; j < links_list.size(); j++)
	{
		if (links_list[j].b_node_id == node_id && links_list[j].visited == false)
		{
			if (links_list[j].weight == 0) // if one of the weights is == 0 --> return 0 
			{
				sum_weights = 0;//reset sum_weights
				return sum_weights;
			}
			sum_weights += links_list[j].weight;
			links_list[j].visited = true;
		}
	}
	return sum_weights;
};