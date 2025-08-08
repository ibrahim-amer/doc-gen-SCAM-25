/**
* Calculates the dominant eigenvector of a given adjacency matrix using the power iteration method.
*
* @param ADJACENCY_MATRIX A 2D vector representing the adjacency matrix of a graph.
* @param delta A threshold for convergence of the eigenvector calculation.
* @return A vector containing the dominant eigenvector corresponding to the largest eigenvalue.
*/
vector<double> get_eigenvector(vector<vector<int>> ADJACENCY_MATRIX, double delta)
{
	
	vector<double> max_eigenvector_a(ADJACENCY_MATRIX.size(),1.0);//"startup" vector is set to 1...
	vector<double> AUX_max_eigenvector_a(ADJACENCY_MATRIX.size(),0.0);
	
	vector<double> max_eigenvector_b(ADJACENCY_MATRIX.size(),0.0);
	vector<double> AUX_max_eigenvector_b(ADJACENCY_MATRIX.size(),0.0);

	double norm_a=get_L2_norm(max_eigenvector_a);
	double norm_b=get_L2_norm(max_eigenvector_b);

	while (true)
	{
		for (size_t i = 0; i < ADJACENCY_MATRIX.size(); i++)//for every row of the routing matrix...
			for (size_t j = 0; j < ADJACENCY_MATRIX[0].size(); j++)	
				max_eigenvector_b[i] += ADJACENCY_MATRIX[i][j]*max_eigenvector_a[j];//row by column_vector
				//print_vector_double(max_eigenvector_a,"max_eigenvector_a_RR");//TEST - OK
				//print_vector_double(max_eigenvector_b,"max_eigenvector_b_RR");//TEST - OK
		//normalize b
		norm_b=get_L2_norm(max_eigenvector_b);
		//cout<<"norm_b --> "<<norm_b<<endl;//TEST - OK
		for (size_t m = 0; m < max_eigenvector_a.size(); m++)
			AUX_max_eigenvector_b[m] = max_eigenvector_b[m]/norm_b;
		max_eigenvector_b=AUX_max_eigenvector_b;
		//print_vector_double(max_eigenvector_b,"max_eigenvector_b_NORM");//TEST - OK
		if (abs(norm_a-norm_b) < delta)
			return max_eigenvector_a;
		else//reset  max_eigenvector_a for next round...
		{
			vector<double> AUX_1(ADJACENCY_MATRIX.size(),0.0);
			max_eigenvector_a=AUX_1;
		}
			
		for (size_t i = 0; i < ADJACENCY_MATRIX.size(); i++)//for every row of the routing matrix...
			for (size_t j = 0; j < ADJACENCY_MATRIX[0].size(); j++)	
				max_eigenvector_a[i] += ADJACENCY_MATRIX[i][j]*max_eigenvector_b[j];//row by column_vector	
				//print_vector_double(max_eigenvector_a,"max_eigenvector_a_KK");//TEST - OK
				//print_vector_double(max_eigenvector_b,"max_eigenvector_b_KK");//TEST - OK
		//normalize a
		norm_a=get_L2_norm(max_eigenvector_a);
		//cout<<"norm_a --> "<<norm_a<<endl;//TEST - OK
		for (size_t k = 0; k < max_eigenvector_a.size(); k++)
			AUX_max_eigenvector_a[k] = max_eigenvector_a[k]/norm_a;	
		max_eigenvector_a=AUX_max_eigenvector_a;	
		//print_vector_double(max_eigenvector_a,"max_eigenvector_a_NORM");//TEST - OK
		if (abs(norm_a-norm_b)  < delta)
			return max_eigenvector_b;
		else//reset  max_eigenvector_b for next round...
			{
				vector<double> AUX_2(ADJACENCY_MATRIX.size(),0.0);
				max_eigenvector_b=AUX_2;
			}
	}
}