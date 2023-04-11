import sys
from visualize import visualize


if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    json_path = "samples/standard-FA-sample/dfa-sample.json"#args[0]  
     # the relative path of the json file containing the dfa or nfa in the desired format
    visualize(json_path)  # visualize the FA
    print("hey")





