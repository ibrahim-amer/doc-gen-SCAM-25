/**
* Writes a 2D matrix of doubles to a CSV file format.
*
* @param dbl_matrix A 2D vector containing double values to be printed.
* @param out_file The name of the output file where the CSV data will be written.
*/
void print_double_matrix_csv_OPT(vector<vector<double>> dbl_matrix, string out_file)
{
	//assemble 
	vector<string> file_buffer;
	for (int i = 0; i < dbl_matrix.size(); i++) {
		for (int j = 0; j < dbl_matrix[i].size(); j++)
			file_buffer.push_back ( to_string(dbl_matrix[i][j]) + ",");
		file_buffer.push_back("\n");
	}

	//print to FILE
	std::ofstream output;
	output.open(out_file.c_str());

	for (size_t j = 0; j < file_buffer.size(); j++)
	{
		output <<file_buffer[j];//line-oriented output
	}
}