/**
 * A command in the sense of the Command pattern.
 *
 * <p>Every user function of SDFMS is represented by one command object,
 * including "undo", "redo" and "show undo/redo lists". Command objects
 * encapsulate the request together with everything needed to carry it out,
 * so the console only has to create the object and execute it.</p>
 */
public interface Command {

    /** Carries out the request, including any interaction with the user. */
    void execute();

    /** Reverses the effect of a previous execution. */
    void undo();

    /** Re-applies the effect after it has been undone. */
    void redo();

    /** Text used in the undo/redo lists and in the undo/redo messages. */
    String getDescription();

    /** Tells the command manager whether this command belongs to the history. */
    boolean isUndoable();
}
