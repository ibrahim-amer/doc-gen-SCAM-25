/**
* Tokenizes a string into a vector of strings based on a specified separator.
*
* @param line The input string to be tokenized based on the separator.
* @param separator The character used to separate tokens in the input string.
* @return A vector of strings containing the separated tokens.
*/
vector<string> NFD_line_tokenizer(string line, char separator)
{
    vector<string> tokens;
    string temp_buf;
    stringstream ss(line);
    while (getline(ss,temp_buf,separator))
        tokens.push_back(temp_buf);
    return tokens;
}