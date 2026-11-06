/**
 * "Undo the last command" command. Undo is itself a command object, so the
 * console treats it exactly like every other function.
 */
public class UndoCommand extends AbstractCommand {

    public UndoCommand(CommandContext context) {
        super("u", context);
    }

    @Override
    public void execute() {
        getContext().getCommandManager().undo();
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Undo";
    }
}
