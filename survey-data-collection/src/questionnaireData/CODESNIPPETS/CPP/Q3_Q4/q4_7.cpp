/**
* Assigns weights to links in a path based on their connections and initial weights.
*
* @param path A structure containing the path and its associated links.
* @param routing_matrix A matrix to store the weights of the links in the path.
*/
void assign_weights_V2(path_struct& path, vector<vector<double>>& routing_matrix)
{


	vector<link_struct> temp_links;//testing...
	bool src_node = true;//testing...

	//Assign weights to a single PATH

	int begin = 0;//sets the beginning point for the next step of the algorithm

	//Set weight(s) for the first link(s)--> this starts the algorithm
	if (src_node)
	{
		for (size_t i = 0; i < path.links_list.size(); i++)
		{
			if (path.links_list[i].a_node_id == path.src_id)
			{
				int num_links_1 = num_links_init_node(path, path.src_id);

				path.links_list[i].weight = W_INIT / num_links_1;//set weight for first link(s)

				src_node = false;

				begin = num_links_1;//sets the beginning point for the next step of the algorithm

				//set corresponding weight in "A"
				routing_matrix[ path.links_list[i].link_id ][path.path_id] = path.links_list[i].weight;

			}
		}
	}


	//	cout << "\n\n FIRST LINKS are now SET \n\n";

		//Start from first element in path.links_list without a weight

		//for each element in path.links_list --> try to calculate the link weights
		//using W(A,B) = SUM [ W(*,A) ] / NUM [ (A,*) ]
		//save the links missing any of the W(*,A) in an auxiliary table "temp_links", 
		//and deal with them during the "second pass" (see below)
	for (size_t i = begin; i < path.links_list.size(); i++)
	{
		double temp_weight = 0;
		int num_links = 0;

		num_links = num_links_init_node(path, path.links_list[i].a_node_id);
		temp_weight = sum_weights_end_node(path.links_list, path.links_list[i].a_node_id);

		if (temp_weight != 0.0)
		{
			path.links_list[i].weight = temp_weight / num_links;

			//set corresponding weight in "A"
			routing_matrix[path.links_list[i].link_id][path.path_id] = path.links_list[i].weight;
		}
		else
		{
			temp_links.push_back(path.links_list[i]);
		}
	}



	//"second pass", implementation 2 --> works regardless of the number of passes required
	while (!temp_links.empty())
	{
		for (size_t i = 0; i < path.links_list.size(); i++)
		{
			if (path.links_list[i].weight == 0.0)//if you find an element with no weight yet...try to compute
			{
				double temp_weight = 0;
				int num_links = 0;

				num_links = num_links_init_node(path, path.links_list[i].a_node_id);
				temp_weight = sum_weights_end_node(path.links_list, path.links_list[i].a_node_id);

				if (temp_weight != 0.0)
				{
					path.links_list[i].weight = temp_weight / num_links;
					temp_links.pop_back();

					//set corresponding weight in "A"
					routing_matrix[path.links_list[i].link_id][path.path_id] = path.links_list[i].weight;
				}
			}
		}
	}


	//END --> Assign weights to a single PATH



}