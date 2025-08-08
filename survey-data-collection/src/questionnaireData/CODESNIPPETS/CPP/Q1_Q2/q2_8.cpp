/**
* Parses command-line input and stores parameters in a map.
*
* @param argc The number of command-line arguments passed to the program.
* @param argv An array of command-line argument strings.
*/
void input_parser::parse_input(int argc, char* argv[])
{
    for (size_t i = 0; i < argc; i++)
    {
        //input_string.push_back( (string)argv[i] );
        for(size_t j = 0 ; j < this->INPUT_PARAMETERS.size() ; j++ )
            if( (string)argv[i] == this->INPUT_PARAMETERS[j]    )
                this->INPUT[(string)argv[i]] = (string)argv[i+1];
    }
}