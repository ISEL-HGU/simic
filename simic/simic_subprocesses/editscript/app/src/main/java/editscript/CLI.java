package editscript;

import org.apache.commons.cli.*;

public class CLI {
    private String srcFile;
    private String dstFile;

    public CLI (String[] args) {
        Options options = createOptions();
        if(parseOptions(options, args)){ printHelp(options); }
    }

    public String[] getFiles() { return new String[]{srcFile, dstFile}; }

    private boolean parseOptions(Options options, String[] args) {
        CommandLineParser parser = new DefaultParser();
        try {
            CommandLine cmd = parser.parse(options, args);
            srcFile = cmd.getOptionValue("src");
            dstFile = cmd.getOptionValue("dst");
        } catch (Exception e) {
            e.printStackTrace();
            printHelp(options);
            return true;
        }
        return false;
    }

    private Options createOptions() {
        Options options = new Options();

        options.addOption(Option.builder("src")
                .required()
                .desc("source file")
                .hasArg()
                .argName("srcFile")
                .build());

        options.addOption(Option.builder("dst")
                .required()
                .desc("destination file")
                .hasArg()
                .argName("dstFile")
                .build());

        options.addOption(Option.builder("h").longOpt("help")
                .desc("Help")
                .build());

        return options;
    }

    private void printHelp(Options options) {
        HelpFormatter formatter = new HelpFormatter();
        String header = "editscript";
        String footer ="\nPlease report issues at https://github.com/GuinZack/simic_BE";
        formatter.printHelp("editscript", header, options, footer, true);
    }
}