/**
* Parses a string of commands into a vector of parameter names based on a separator.
*
* @param input_commands A string containing commands separated by a specified character.
* @param separator The character used to separate commands in the input string.
* @return A vector of strings containing the separated command names.
*/
vector<string> input_parser::get_parameter_names(string input_commands, char separator)
{
    vector<string> tokens;
    string temp_buf;
    stringstream ss(input_commands);
    while (getline(ss,temp_buf,separator))
        tokens.push_back(temp_buf);

    return tokens;
}