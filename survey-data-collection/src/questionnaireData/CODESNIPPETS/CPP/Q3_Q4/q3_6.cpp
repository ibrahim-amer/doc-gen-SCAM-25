/**
* Creates a mapping of node IDs to their corresponding names and populates a node list.
*
* @param dictionary A vector of strings containing node information.
* @param NODES_LIST A reference to a vector of node_struct to store node details.
* @return A map of node IDs to their names as strings.
*/
map<int,string> get_node_dictionary_and_list(vector<string> dictionary , vector<node_struct> &NODES_LIST)
{
	map<int,string> NODE_DICTIONARY;
	vector<string> tokens;
	node_struct node;
	//populates NODE_DICTIONARY
	for (size_t k = 0; k < dictionary.size(); k++)
	{	
		tokens = line_tokenizer(dictionary[k],',');
		NODE_DICTIONARY.insert(pair<int,string>(stoi(tokens[1]),tokens[0]));
		node.CLLI = tokens[0];
		node.NODE_ID = stoi(tokens[1]);
		tokens = {};//reset
		NODES_LIST.push_back(node);
		node={};//reset
	}
	//"bulletproofing" NODE_LIST ordering --> guarantees NODES_LIST is always ordered from node_ID =0 to node_ID=MAX_NODE_ID
	sort(NODES_LIST.begin(), NODES_LIST.end(),node_id_ordering);//redundant if NODE_DICTIONARY IS ALREADY ORDERED by node_ID, impact on computing time is minimal

	return NODE_DICTIONARY;
}