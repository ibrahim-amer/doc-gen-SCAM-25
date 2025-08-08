/**
* Prints various attributes of a network link including IDs, traffic, and centrality measures.
*
* @param link A structure containing details about a network link.
*/
void print_link(link_struct link)
{
	cout << "\n link --> " << link.a_node_id << " - " << link.b_node_id << endl;
	cout << " link link ID --> " << link.link_id << endl;
	cout << " link Traffic [Mb/s] --> " << link.traffic << endl;
	cout << " link visited --> " << link.visited << endl;
	cout << " link weight --> " << link.weight << endl << endl;
	cout << " link Traffic (COMPUTED) [Mb/s] --> " << link.traffic_computed << endl;
	cout << " link capacity --> " << link.capacity << endl << endl;


	//centrality measures:
	
	cout<<"Routed Centrality --> "<< link.routed_centrality<< endl;//"routed"  cerntrality
	cout<<"Routed Centrality (Normalized) --> "<<link.routed_centrality_normalized<< endl;//"routed" betweeenness cerntrality normalized wrt total number of active paths  
	cout<<"Utilization Factor --> "<< link.utilization_factor<< endl;
	cout<<"Link Utiliation --> "<< link.link_utilization<< endl;

	//Compound Centrality measures:
	cout<<"Weighted Utilization Factor --> "<< link.weighted_utilization_factor<< endl;//utilization factor * link traffic ratio ( * 100)
	cout<<"Weighted Routed Centrality --> "<< link.weighted_routed_centrality<< endl;//routed_centrality * link traffic ratio ( * 100)

}