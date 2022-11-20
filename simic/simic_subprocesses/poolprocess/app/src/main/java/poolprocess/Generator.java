/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package poolprocess;

public class Generator {

    public static void main(String[] args) {
        CLI cli = new CLI(args);
        String diff = runDiff(cli.getDiffInfo());
        System.out.println(diff);
    }

    public static String runDiff(String[] diffInfo) {
        String diff = new Git().collect(diffInfo);
        if (diff == null) {
            return null;
        }
        return diff;
    }
}