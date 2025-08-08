/**
* Extracts paths and their associated traffic from given file paths and matrices.
*
* @param full_file_paths A vector of strings containing file paths with source and destination IDs.
* @param LINKS_MATRIX A matrix representing links between nodes, used to retrieve link IDs.
* @param TRAFFIC_MATRIX A matrix containing traffic data between source and destination nodes.
* @return A vector of path_struct containing source, destination, traffic, and links information.
*/
vector<path_struct> get_demands_paths(vector<string> full_file_paths, vector<vector<int>> LINKS_MATRIX, vector<vector<double>> TRAFFIC_MATRIX)
{
	
	vector<path_struct> paths_set;
	path_struct aux_path;
	vector<string> tokens;

	for (size_t i = 0; i < full_file_paths.size(); i++)
    {
        tokens = line_tokenizer(full_file_paths[i],',');

		//set SRC and DST and path_traffic
		aux_path.src_id = stoi(tokens[0]);//SRC
		aux_path.dst_id = stoi(tokens[1]);//DST


		aux_path.path_traffic = TRAFFIC_MATRIX[aux_path.src_id][aux_path.dst_id];
		
		/*
		cout<<"aux_path.src_id --> "<<aux_path.src_id<<endl;//TEST - OK
		cout<<"aux_path.dst_id --> "<<aux_path.dst_id<<endl;//TEST - OK
		cout<<"aux_path.path_traffic --> "<<aux_path.path_traffic<<endl;//TEST - OK
	*/

		link_struct aux_link;
		for (size_t j = 2; j < tokens.size()-1; j++)
		{
			//cout<<tokens[j]<<" => ";//TEST - OK

			aux_link.a_node_id = stoi(tokens[j]);
			aux_link.b_node_id = stoi(tokens[j+1]);

			aux_link.link_id = LINKS_MATRIX[aux_link.a_node_id ][aux_link.b_node_id];//Assign link ID 
		
			aux_path.links_list.push_back(aux_link);// save link to path
			aux_link ={};//reset  
			j++;//processing pairs only
		}

		aux_path.path_id = i;//assign (UNIQUE) link ID

		paths_set.push_back(aux_path);

		tokens ={};//reset
		aux_path = {};//reset        
    }


	return paths_set;


}