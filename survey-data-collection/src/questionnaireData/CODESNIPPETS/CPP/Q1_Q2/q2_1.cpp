/**
* Calculates weighted link centrality measures based on traffic and total traffic.
*
* @param LINKS_LIST A vector of link_struct containing traffic and centrality data.
* @param TOTAL_TRAFFIC The total traffic value used for normalization of centrality measures.
* @return This function does not return a value; it modifies the LINKS_LIST in place.
*/
void set_weighted_link_centrality_measures(vector<link_struct> &LINKS_LIST, double TOTAL_TRAFFIC)
{
	for (size_t i = 0; i < LINKS_LIST.size(); i++)
	{
		LINKS_LIST[i].weighted_utilization_factor = LINKS_LIST[i].utilization_factor * (	LINKS_LIST[i].traffic/TOTAL_TRAFFIC	) * 100;
		LINKS_LIST[i].weighted_routed_centrality = LINKS_LIST[i].routed_centrality * (	LINKS_LIST[i].traffic/TOTAL_TRAFFIC	) * 100;
	}
			
}