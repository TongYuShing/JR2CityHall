import java.util.Scanner;

/**
 * Thin wrapper around Scanner that prints the prompt before reading a line.
 * A null is returned when the input stream has no more lines.
 */
public class ConsoleInput {

    private final Scanner scanner;

    public ConsoleInput(Scanner scanner) {
        this.scanner = scanner;
    }

    /** Prints a prompt and returns the next input line, or null at end of input. */
    public String readLine(String prompt) {
        System.out.print(prompt);
        if (!scanner.hasNextLine()) {
            return null;
        }
        return scanner.nextLine().trim();
    }

    /** Prints a prompt and returns the next input line as a role code, or -1. */
    public int readRole(String prompt) {
        String line = readLine(prompt);
        if (line == null) {
            return -1;
        }
        try {
            return Integer.parseInt(line.trim());
        } catch (NumberFormatException ex) {
            return -1;
        }
    }

    /**
     * Reads a line of the form "id, name" and returns a two element array,
     * or null when the line cannot be split into exactly two parts.
     */
    public String[] readDriverInformation() {
        String line = readLine("Please input driver information (id, name):- ");
        if (line == null) {
            return null;
        }
        String[] parts = line.split(",", 2);
        if (parts.length < 2) {
            return null;
        }
        String id = parts[0].trim();
        String name = parts[1].trim();
        if (id.isEmpty() || name.isEmpty()) {
            return null;
        }
        return new String[] {id, name};
    }
}
