 /**
 * Compares two path_struct objects based on their dst_id.
 *
 * @param path_1 First path_struct object to compare.
 * @param path_2 Second path_struct object to compare.
 * @return Returns true if path_1 has a smaller dst_id than path_2, otherwise false.
 */
 
 bool dst_id_path_ordering(path_struct path_1, path_struct path_2)
	{
		return (path_1.dst_id < path_2.dst_id);
	}