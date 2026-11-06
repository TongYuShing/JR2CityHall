/**
 * Factory that turns a command code typed by the user into a Command object.
 */
public interface CommandFactory {

    /** Returns the command for the code, or null when the code is unknown. */
    Command createCommand(String commandCode);
}
