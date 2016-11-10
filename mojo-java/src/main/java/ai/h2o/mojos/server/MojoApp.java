package ai.h2o.mojos.server;

import ai.h2o.mojos.server.handlers.LoadMojoHandler;
import ai.h2o.mojos.server.handlers.MojoApiHandler;
import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import hex.genmodel.MojoModel;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.ServletContextHandler;


/**
 * <p>MojoApp is a framework that enables one to instantiate {@link MojoModel}s
 * and then access them via a simple REST API.</p>
 *
 */
public class MojoApp {
  @Parameter(names = "--port", description = "Port on which the server is going to be listening.")
  private int port = 54320;


  public static void main(String[] args) {
    MojoApp main = new MojoApp();
    new JCommander(main, args);
    main.run();
  }

  private void run() {
    try {
      Server server = new Server(port);
      registerApi(server);
      server.start();
      server.join();  // Join the current thread and wait until server is done executing (i.e. forever)
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void registerApi(Server server) {
    ServletContextHandler handler = new ServletContextHandler();
    handler.addServlet(LoadMojoHandler.class, "/loadmojo");
    handler.addServlet(MojoApiHandler.class, "/mojos/*");
    server.setHandler(handler);
  }

}
