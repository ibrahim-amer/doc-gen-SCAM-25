/**
* Constructor for input_parser class that initializes input parameters from a string.
*
* @param PARAMETERS_string A string containing parameters separated by commas.
*/
input_parser::input_parser(string PARAMETERS_string)
{
    this->INPUT_PARAMETERS = this->get_parameter_names(PARAMETERS_string,',');
}