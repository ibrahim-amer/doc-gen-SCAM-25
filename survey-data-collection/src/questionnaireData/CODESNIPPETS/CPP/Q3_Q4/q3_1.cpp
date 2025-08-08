/**
* Creates a map from a vector of strings, parsing each string into key-value pairs.
*
* @param dictionary A vector of strings containing key-value pairs separated by commas.
* @return A map where keys are integers and values are strings from the input vector.
*/
map<int,string> get_node_dictionary(vector<string> dictionary )
{
	map<int,string> NODE_DICTIONARY;
	vector<string> tokens;
	for (size_t k = 0; k < dictionary.size(); k++)
	{	
		tokens = line_tokenizer(dictionary[k],',');
		NODE_DICTIONARY.insert(pair<int,string>(stoi(tokens[1]),tokens[0]));
		tokens = {};//reset
	}
	return NODE_DICTIONARY;
}