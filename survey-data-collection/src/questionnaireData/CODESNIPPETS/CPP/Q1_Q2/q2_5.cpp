/**
* Prints each link_struct object in the provided vector.
*
* @param links_list A vector of link_struct objects to be printed.
*/
void print_vector_links(vector<link_struct> links_list)
{
	for (size_t i = 0; i < links_list.size(); i++)
	{
		print_link(links_list[i]);
	}
}