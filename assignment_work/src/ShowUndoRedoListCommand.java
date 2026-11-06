/** "Show the undo/redo lists" command. */
public class ShowUndoRedoListCommand extends AbstractCommand {

    public ShowUndoRedoListCommand(CommandContext context) {
        super("l", context);
    }

    @Override
    public void execute() {
        getContext().getCommandManager().showLists();
    }

    @Override
    public boolean isUndoable() {
        return false;
    }

    @Override
    public String getDescription() {
        return "Show undo/redo lists";
    }
}
