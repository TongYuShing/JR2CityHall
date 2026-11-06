/**
 * Common behaviour shared by all SDFMS commands.
 */
public abstract class AbstractCommand implements Command {

    private final String commandCode;
    private final CommandContext context;

    protected AbstractCommand(String commandCode, CommandContext context) {
        this.commandCode = commandCode;
        this.context = context;
    }

    public String getCommandCode() {
        return commandCode;
    }

    protected CommandContext getContext() {
        return context;
    }

    @Override
    public boolean isUndoable() {
        return true;
    }

    @Override
    public void undo() {
        // Commands that do not change persistent data override nothing.
    }

    @Override
    public void redo() {
        execute();
    }

    @Override
    public String getDescription() {
        return commandCode;
    }
}
