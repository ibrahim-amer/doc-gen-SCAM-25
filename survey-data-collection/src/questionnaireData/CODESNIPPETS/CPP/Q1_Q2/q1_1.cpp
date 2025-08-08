/**
* Calculates and sets the weighted routed centrality for each link in the LINKS_LIST.
*
* @param LINKS_LIST A vector of link_struct containing traffic and centrality data.
* @param TOTAL_TRAFFIC The total traffic value used for calculating weighted routed centrality.
*/
void set_weighted_routed_centrality(vector<link_struct> &LINKS_LIST, double TOTAL_TRAFFIC)
{
	for (size_t i = 0; i < LINKS_LIST.size(); i++)
		LINKS_LIST[i].weighted_routed_centrality = LINKS_LIST[i].routed_centrality * (	LINKS_LIST[i].traffic/TOTAL_TRAFFIC	) * 100;	
}