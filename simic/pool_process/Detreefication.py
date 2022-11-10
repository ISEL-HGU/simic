from anytree import Node, RenderTree, LevelOrderGroupIter
# from .dataProcess.SubProcessor import SubProcessor
from dataProcess.DataProcessor import DataProcessor
import pickle
import sys
import re



class Detreefication:
    
    def __init__(self):

        with open('./combinedChangeVector.tree','rb') as file:
            unpickler = pickle.Unpickler(file)
            print(unpickler.__str__)
            self.static = unpickler.load()
        code_list = 0

    def test_1(self):
        code_list = code_list+1

    def execute(self):
        #When API rquest comes
        edit_script = open(sys.argv[2],'r').read()
        parsed_script = edit_script.split('|')
        if '' in parsed_script:
            parsed_script.remove('')
        node = self.traverse_tree(self.static,parsed_script)

        #Search Results
        hunks = []
        if node is None:
            print('exact match not found!')
        else:
            print(str(len(node.repo)) + ' exact matches found' + '\n')
            for i in range (0,len(node.repo)):
                print(node.repo[i] + '\t' + node.cpc[i] + '\t' + node.pc[i] + '\t' + node.file_path[i] + '\t' + node.blamed_line[i] + '\n')

    def traverse_tree(self, static, parsed_script):
        found_node = None

        for root in static.trees:
            if parsed_script[0] == root.name:
                if len(root.children) == 0:
                    return root
                else:
                    found_node = self.traverse_tree_recur(root,parsed_script)
                    break
        
        return found_node

    def traverse_tree_recur(self, root ,parsed_script):
        children = root.children
        if len(children) > 0:
            for node in children:
                if parsed_script[node.depth] == node.name:
                    if len(parsed_script) == node.depth+1:
                        return node
                    return self.traverse_tree_recur(node,parsed_script)
                
            return None
    # else:
    #     print(str(len(node.repo)) + 'exact matches found' + '\n')
    #     for i in range(0,len(node.repo)):
    #         hunks.append(SubProcessor('./app -proj ' + node.repo[i] 
    #         + ' -cpc ' + node.cpc[i] + ' -pc ' + node.pc[i] + ' -file ' + node.file_path[i] 
    #         + ' -line \"' + node.blame_line[i] + '\"').code_snippet)
    #To do: Do multi programming to boost up the process

    # if len(hunks) != 0:
    #     for hunk in hunks:
    #         temp_list = re.split(hunk, '@@ -[0-9]+,[0-9]+ \\+[0-9]+,[0-9]+ @@\n')
    #         code = temp_list[len(temp_list)-1]


# if __name__ == '__main__':
#     main()