/** "Redo the last undone command" command. */
public class RedoCommand extends AbstractCommand {

    public RedoCommand(CommandContext context) {
        super("r", context);
    }

    @Override
    public void execute() {
        getContext().getCommandManager().redo();
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Redo";
    }
}
