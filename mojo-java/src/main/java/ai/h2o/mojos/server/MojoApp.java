package ai.h2o.mojos.server;

import ai.h2o.mojos.server.handlers.LoadMojoHandler;
import ai.h2o.mojos.server.handlers.MojoApiHandler;
import ai.h2o.mojos.server.handlers.ShutdownHandler;
import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import hex.genmodel.MojoModel;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.ServletContextHandler;


/**
 * MojoApp is a framework that enables one to instantiate {@link MojoModel}s
 * and then access them via a simple REST API.
 *
 */
public class MojoApp {
  @Parameter(names = "--port", description = "Port on which the server is going to be listening.")
  private int port = 54320;

  public static transient Server server;


  /**
   * This only handles parsing of command-line args. The real action occurs
   * in {@link #run()}.
   */
  public static void main(String[] args) throws Exception {
    MojoApp mojoApp = new MojoApp();
    JCommander jc = new JCommander(mojoApp);
    try {
      jc.parse(args);
    } catch (Exception e) {
      System.out.println(e.toString());
      System.out.println();
      jc.usage();
      System.exit(1);
    }
    mojoApp.run();
  }

  /**
   * MojoApp is a server that provides REST API to mojos. Thus this method
   * starts the (Jetty) server and then waits for incoming connections.
   */
  private void run() throws Exception {
    server = new Server(port);
    server.setStopAtShutdown(true);
    registerEndpoints();
    server.start();
    // This phrase is searched for in backend.py. Please synchronize modifications.
    System.out.println("MojoServer started on port " + port);
    server.join();  // Join the current thread and wait until server is done executing (i.e. forever)
    System.out.println("MojoServer on port " + port + " has shut down.");
  }

  /**
   * Register all endpoints on the provided server instance.
   */
  private void registerEndpoints() {
    ServletContextHandler handler = new ServletContextHandler();
    handler.addServlet(LoadMojoHandler.class, "/loadmojo");
    handler.addServlet(MojoApiHandler.class, "/mojos/*");
    handler.addServlet(ShutdownHandler.class, "/shutdown");
    server.setHandler(handler);
  }

}
