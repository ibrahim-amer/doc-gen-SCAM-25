 /**
 * Compares two path_struct objects based on their src_id values.
 *
 * @param path_1 First path_struct object to compare.
 * @param path_2 Second path_struct object to compare.
 * @return Returns true if path_1 has a smaller src_id than path_2, otherwise false.
 */
 
 bool src_id_path_ordering(path_struct path_1, path_struct path_2)
	{
		return (path_1.src_id < path_2.src_id);
	}