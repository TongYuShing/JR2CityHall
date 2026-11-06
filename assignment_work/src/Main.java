import java.util.Scanner;

/**
 * Entry point of SDFMS. It wires the console, the repository, the command
 * manager and the abstract factory together and starts the application.
 */
public class Main {

    public static void main(String[] args) {
        FleetRepository repository = new FleetRepository();
        ConsoleInput input = new ConsoleInput(new Scanner(System.in));
        CommandContext context = new CommandContext(repository, input);
        context.setCommandManager(new CommandManager());
        context.setFactory(new SDFMSFactory(context));
        new SDFMSApplication(context).run();
    }
}
