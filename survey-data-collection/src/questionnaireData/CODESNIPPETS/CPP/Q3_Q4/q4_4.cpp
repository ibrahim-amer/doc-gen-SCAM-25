/**
* Reads a file containing tables and extracts them into a map of table names and their contents.
*
* @param tables_path_file Path to the file containing tables to read.
* @param separator Character used to separate values in the file.
* @param filler Character used to fill empty values in the table.
* @return A map where keys are table names and values are vectors of rows (vectors of strings).
*/
map< string, vector< vector<string> >  > read_table_extract_WAE(string tables_path_file, char separator, string filler)
{
	map< string, vector< vector<string> >  > WAE_TABLES;


	//support variables
	string table_name;
	vector<vector<string>> table = {};//initialize to empty()

	//Read the whole file --> fully tokenized, default separator (--> "")
	FILE_READER tables_file_READER(tables_path_file, "single_file_full", separator, filler);

	vector<vector<string>> tables_file = tables_file_READER._get_file().CONTENT;//read_csv(tables_path_file);

	//Process tables
	for (size_t i = 0; i < tables_file.size(); i++)
	{
		if( ! tables_file[i].empty() )//IF current line ( vector<string> ) is NOT EMPTY --> process it
		{
			if(tables_file[i][0][0] == '<' && i < 1 )//found the beginning of the first table	
			{				
				table_name = line_tokenizer(	tables_file[i][0].substr( 1, tables_file[i][0].size()	) , '>')[0];//record table name
				table.clear();//reset table - redundant...
			}

			else if( tables_file[i][0][0] == '<' && i > 1 && i != tables_file.size()-1 ) //  found the beginning of next table (but not last table ) --> save previous table and initialize next table
			{
				//save table
				WAE_TABLES[table_name] = table;			
				//reset AUX variables
				table_name.clear();//reset...
				table.clear();//reset...

				table_name = line_tokenizer(	tables_file[i][0].substr( 1, tables_file[i][0].size()	)	,'>')[0];//record NEW table name
			}

			else if( i == tables_file.size() -1  ) //  end of last table
			{				
				table.push_back( tables_file[i]	);
				//save table
				WAE_TABLES[table_name] = table;			
				//reset AUX variables
				table_name.clear();//reset...
				table.clear();//reset...
			}		
			else 
			{
				table.push_back( tables_file[i]	);
			}
		}//END process NON-EMPTY line ( vector<string> )			
	}	


	return WAE_TABLES;    
}