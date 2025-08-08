/**
* Reads a CSV file and returns a list of nodes with their attributes.
*
* @param file_name The name of the CSV file to read node data from.
* @return A vector of simple_NODE containing the parsed node information from the file.
*/
vector<simple_NODE> get_nodes_list(string file_name)
{
    vector<string> tokens;
    simple_NODE node_entry_AUX;
    vector<simple_NODE> NODES_LIST;//stores the result
    vector<string> input_nodes = read_csv(file_name);//reads input file into a vector<string>

    for (size_t i = 1; i < input_nodes.size(); i++)//skip first line of the file with the column name
    {
        tokens = line_tokenizer(input_nodes[i],',');

        //node CLLI 
            node_entry_AUX.CLLI = tokens[0];
        //NODE AS
        if ( isdigit(tokens[1][0]))
            node_entry_AUX.AS = stoul(tokens[1]);
        //node BGP ID
            node_entry_AUX.BGPID = tokens[2];
        //IP ADDRESS
            node_entry_AUX.IPAddress = tokens[3];
        //interface count
        if( isdigit(tokens[4][0]))
            node_entry_AUX.InterfaceCount = stoi(tokens[4]);
        //vendor
            node_entry_AUX.Vendor = tokens[5];
        //model
            node_entry_AUX.Model = tokens[6];
        //OS
            node_entry_AUX.OS = tokens[7];
        NODES_LIST.push_back(node_entry_AUX);//store
        //reset
        tokens ={};
        node_entry_AUX ={};
    }
    return NODES_LIST;
}