/**
* Calculates and sets the degree centrality for each node in the graph.
*
* @param adjacency_matrix A 2D vector representing the adjacency matrix of the graph.
* @param NODES_LIST A reference to a vector of node_struct containing node information.
*/
void set_degree_centrality(vector<vector<int>> adjacency_matrix,vector<node_struct> &NODES_LIST)
{
	double deg_centrality_aux = 0;
	for (size_t i = 0; i < NODES_LIST.size(); i++)
	{
		for (size_t j = 0; j < NODES_LIST.size(); j++)
			deg_centrality_aux += adjacency_matrix[i][j];
		NODES_LIST[i].degree_centrality = deg_centrality_aux;
		deg_centrality_aux =0;//reset
	}
}