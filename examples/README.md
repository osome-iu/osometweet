### Examples

> This folder is intended to house example scripts which are actually useful for new users **learning** how the package works.


##### Explaining the different types of scripts
* `xxxxxx-simple.py` : Scripts with `simple.py` at the end are written to explain very simply to the user (with lots of comments) how a method is used. 
    * See `user-lookup-simple.py` for an example.
* Other scripts : All other scripts scripts without the `simple` marker are meant to be more practically useful for general purpose goals. 
    * `user-lookup.py` : A solid command-line script for scraping many users account information. This script takes a file containing user IDs on each line as an input. You can test this script with the file [`test_data/test_user_ids.txt`](https://github.com/truthy/osometweet/blob/master/examples/test_data/test_user_ids.txt) which is a random collection of user IDs, one per row. If you'd like to use this script on a different set of user IDs the input file of new user IDs must follow the same format.