/**
* Writes traffic data to a CSV file, including node IDs and traffic in Mb/s.
*
* @param LINK_TRAFFIC A vector of link_struct containing traffic data.
* @param out_file The output CSV file name to write traffic data.
* @param NODE_DICTIONARY A map linking node IDs to their corresponding names.
*/
void print_links_traffic_csv_CLLI(vector<link_struct> LINK_TRAFFIC, string out_file, map<int,string> NODE_DICTIONARY )
{
	std::ofstream output;
	output.open(out_file.c_str());

	output << "A_NODE_ID,B_NODE_ID,TRAFFIC [Mb/s]" << endl;

	for (size_t i = 0; i < LINK_TRAFFIC.size(); i++)
	{
		string buffer_1 = NODE_DICTIONARY[(LINK_TRAFFIC[i].a_node_id)] + "," + NODE_DICTIONARY[(LINK_TRAFFIC[i].b_node_id)] + "," + to_string(LINK_TRAFFIC[i].traffic);//line-oriented output
		
		output << buffer_1 << endl;
		buffer_1 ="";//reset
	
	}
}