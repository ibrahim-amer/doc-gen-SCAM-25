/**
* Prints the inputs stored in the INPUT member variable of the input_parser class.
*/
void input_parser::print_inputs()
{
    cout<<endl;
    auto const& in_list = this->INPUT;
    for(auto const& in_list_itr : in_list)
        cout<<in_list_itr.first<<" --> "<<in_list_itr.second<<endl;
    cout<<endl;
}