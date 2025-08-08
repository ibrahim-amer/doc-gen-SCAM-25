/**
* Counts the number of links associated with a specified node in a path structure.
*
* @param path A structure containing a list of links to analyze.
* @param node_id The ID of the node for which to count links.
* @return The number of links connected to the specified node ID.
*/
int num_links_init_node(path_struct path, int node_id)
{
	int num_links = 0;

	for (size_t j = 0; j < path.links_list.size(); j++)
	{
		if (path.links_list[j].a_node_id == node_id)
		{
			num_links++;
		}
	}
	return num_links;
};