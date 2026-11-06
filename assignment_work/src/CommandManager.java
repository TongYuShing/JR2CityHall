import java.util.List;
import java.util.Vector;

/**
 * Invoker of the Command pattern. It executes commands and keeps the two
 * history lists used by Undo and Redo.
 */
public class CommandManager {

    private final Vector<Command> undoList = new Vector<Command>();
    private final Vector<Command> redoList = new Vector<Command>();

    /** Executes a command and records it when it is an undoable command. */
    public void execute(Command command) {
        command.execute();
        if (command.isUndoable()) {
            undoList.add(command);
            redoList.clear();
        }
    }

    /** Undoes the most recent undoable command. */
    public void undo() {
        if (undoList.isEmpty()) {
            System.out.println("No command can be undone.");
            return;
        }
        Command command = undoList.remove(undoList.size() - 1);
        command.undo();
        redoList.add(command);
        System.out.println("Command (" + command.getDescription() + ") is undone.");
    }

    /** Redoes the most recently undone command. */
    public void redo() {
        if (redoList.isEmpty()) {
            System.out.println("No command can be redone.");
            return;
        }
        Command command = redoList.remove(redoList.size() - 1);
        command.redo();
        undoList.add(command);
        System.out.println("Command (" + command.getDescription() + ") is redone.");
    }

    /** Prints both history lists, oldest entry first. */
    public void showLists() {
        System.out.println("Undo List");
        for (Command command : undoList) {
            System.out.println(command.getDescription());
        }
        System.out.println("-- End of undo list --");
        System.out.println("Redo List");
        for (Command command : redoList) {
            System.out.println(command.getDescription());
        }
        System.out.println("-- End of redo list --");
    }

    public List<Command> getUndoList() {
        return undoList;
    }

    public List<Command> getRedoList() {
        return redoList;
    }
}
