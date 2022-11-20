package editscript;

import com.github.gumtreediff.actions.EditScript;
import com.github.gumtreediff.actions.EditScriptGenerator;
import com.github.gumtreediff.actions.SimplifiedChawatheScriptGenerator;
import com.github.gumtreediff.actions.model.Action;
import com.github.gumtreediff.client.Run;
import com.github.gumtreediff.gen.python.PythonTreeGenerator;
import com.github.gumtreediff.matchers.CompositeMatchers;
import com.github.gumtreediff.matchers.MappingStore;
import com.github.gumtreediff.tree.Tree;
import com.github.gumtreediff.tree.TreeContext;

public class GumTree {
    public String generateChangeVector(String[] fileSources) {
        String srcFileSource = fileSources[0];
        String dstFileSource = fileSources[1];

        Run.initGenerators(); // registers the available parsers
        TreeContext srcTree = null, dstTree = null;
        try {
            srcTree = new PythonTreeGenerator().generateFrom().string(srcFileSource);
            dstTree = new PythonTreeGenerator().generateFrom().string(dstFileSource);
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("$ ERROR ::GumTree::  Cannot generate PythonTree");
            return null;
        }
        EditScript editScript = null;
        if (srcTree!= null && dstTree!=null) {
            Tree src = srcTree.getRoot();
            Tree dst = dstTree.getRoot();
            MappingStore mappings = new CompositeMatchers.SimpleGumtree().match(src, dst);
            EditScriptGenerator editScriptGenerator = new SimplifiedChawatheScriptGenerator();
            editScript = editScriptGenerator.computeActions(mappings);
        }

        if (editScript.asList().size()==0) {
            System.err.println("$ LOG   ::GumTree::  no changes mapped");
            return null;
        }

        String changeVector = "";
        for (Action action : editScript.asList()) {
            String location;
            if (action.getName().contains("delete") || action.getName().contains("update"))
                location = "";
            else location = getActionLocation(action);
            changeVector += action.getName() + "@"
                    + action.getNode().getType().toString()
                    .replaceAll("\\:\\s\\S$", "")
                    .replaceAll("[0-9+,+0-9]", "")
                    .replaceAll("\\[", "")
                    .replaceAll("\\]","")
                    + location.replace(" ", "") + "|";
        }
        return changeVector;
    }

    private String getActionLocation(Action action) {
        String[] actionStringList = action.toString().split("\n");
        boolean checked = false;
        for (int i=0; i<actionStringList.length; i++) {
            if (checked) {
                return "2" + actionStringList[i]
                        .replaceAll("\\:\\s\\S$", "")
                        .replaceAll("[0-9+,+0-9]", "")
                        .replaceAll("\\[", "")
                        .replaceAll("\\]","");
            }
            if (actionStringList[i].contains("\\[")) continue;
            else if (actionStringList[i].indexOf("to") == 0) checked = true;
        }
        return "";
    }
}
