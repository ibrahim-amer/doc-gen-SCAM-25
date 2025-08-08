/**
* Processes a CSV file to extract flow data and populate a vector of FLOW structures.
*
* @param file_name The name of the CSV file to read flow data from.
* @param NODES_MAP_IP A map of nodes indexed by their IP addresses.
* @param INTERFACE_MAP A reference to a map for storing interface details.
* @return A vector of FLOW objects containing parsed flow data from the input file.
*/
vector<FLOW> get_flows_FM_V2( string file_name, map<string,simple_NODE> NODES_MAP_IP , map<string,map<int,string>>& INTERFACE_MAP )
{    
    vector<string> input_file = read_csv(file_name);//read input file
    //cout<<"HERE ?"<<endl;//TEST - OK


    vector<FLOW> flows;//result
    FLOW flow_entry_AUX;
    vector<string> tokens;
    vector<string> AS_path;

    for (size_t i = 1; i < input_file.size(); i++)//starts from second row, i.e. skips header row
    {
       // cout<<"LINE --> "<<i<<endl;//TEST - 

        tokens = line_tokenizer(input_file[i], ';');//semicolon-separated input file

        //tokens[0] == ETYPE --> SKIP


        //SRC_AS
        if (isdigit(tokens[1][0]))
            flow_entry_AUX.SRC_AS = stoul(tokens[1]);
        
        //DST_AS
        if (isdigit(tokens[2][0]))
            flow_entry_AUX.DST_AS = stoul(tokens[2]);

        //AS_PATH
        flow_entry_AUX.AS_PATH = tokens[3];
        /* //Computationnaly intensive --> use ONLY if necessary to work directly with ASN to reconstruct AS path
        AS_path = line_tokenizer(tokens[2], '_');
        for (size_t j = 0; j < AS_path.size(); j++)
        {
            if (isdigit(AS_path[j][0]))
                flow_entry_AUX.AS_PATH.push_back(stoul(AS_path[j]));

            else if (AS_path[j].size() != 0)//remove curly brackets before recording AS number
            {
                string aux_ASN = AS_path[j].substr(1, AS_path[j].size() - 1);
                flow_entry_AUX.AS_PATH.push_back(stoul(aux_ASN));
            }
        }
        */

        //PEER_DST_AS
         if (isdigit(tokens[4][0]))
            flow_entry_AUX.PEER_DST_AS = stoul(tokens[4]);

        //PEER_SRC_IP
            flow_entry_AUX.PEER_SRC_IP = tokens[5];

        //PEER_DST_IP
            flow_entry_AUX.PEER_DST_IP = tokens[6];

        //IN_IFACE
         if (isdigit(tokens[7][0]))
            flow_entry_AUX.IN_IFACE = stoi(tokens[7]);     

        //IN_IFACE_GLOBAL --> tokens[8] --> SKIPPED

        //OUT_IFACE
         if (isdigit(tokens[9][0]))
            flow_entry_AUX.OUT_IFACE = stoi(tokens[9]);   

        //OUT_IFACE_GLOBAL --> tokens[10] --> SKIPPED

        //TOS --> tokens[11] --> SKIPPED

        //SAMPLING_RATE
         if (isdigit(tokens[12][0]))
            flow_entry_AUX.SAMPLING_RATE = stoi(tokens[12]);  

        //PACKETS
         if (isdigit(tokens[13][0]))
            flow_entry_AUX.PACKETS = stoull(tokens[13]);  

        //BYTES
         if (isdigit(tokens[14][0]))
            flow_entry_AUX.BYTES = stoull(tokens[14]); 

        //compute traffic for the flow
        flow_entry_AUX.raw_traffic = ((long long)flow_entry_AUX.BYTES*8.0*(long long )flow_entry_AUX.SAMPLING_RATE)/(600*1000000);


        flows.push_back(flow_entry_AUX);//add to main struct

        //Assemble interface map
        auto const& node_map = NODES_MAP_IP[ flow_entry_AUX.PEER_SRC_IP].interfaces ;//range for iterating through ALL interfaces of ' NODES_MAP_IP[FM[1].PEER_SRC_IP] '

        for(auto const& itr : node_map)
            INTERFACE_MAP[flow_entry_AUX.PEER_SRC_IP][stoi(itr.second.index)] = itr.second.name;


       //resets
        tokens = {};
        AS_path = {};
        flow_entry_AUX = {};
    }
    return flows;

}