/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package editscript;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Generator {

    public static void main(String[] args) {
        String[] files = new CLI(args).getFiles();
        String srcFileSource, dstFileSource;
        try {
            srcFileSource = Files.readString(Path.of(files[0]));
            dstFileSource = Files.readString(Path.of(files[1]));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        if (srcFileSource.isEmpty() || dstFileSource.isEmpty()) {
            System.err.println("error: Cannot read file");
        }
        String changeVector = new GumTree().generateChangeVector(new String[]{srcFileSource, dstFileSource});
        System.out.println(changeVector);
    }
}