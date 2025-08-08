/**
* Updates flow traffic for interfaces based on provided microflows.
*
* @param micro_flows A vector of FLOW objects representing microflows.
* @param NODES_MAP_IP A map linking source IPs to simple_NODE objects.
* @param INTERFACE_MAP A map linking IPs to their respective interface information.
*/
void check_SNMP_microflows(vector<FLOW> micro_flows , map<string,simple_NODE> &NODES_MAP_IP, map<string,map<int,string>> INTERFACE_MAP)
{
    for (size_t i = 0; i < micro_flows.size(); i++)
        NODES_MAP_IP[   micro_flows[i].PEER_SRC_IP   ].interfaces[    INTERFACE_MAP[ micro_flows[i].PEER_SRC_IP ][  micro_flows[i].IN_IFACE]     ].flow_traffic_mFlows += micro_flows[i].raw_traffic;
}