package ai.h2o.mojos.server.handlers;

import ai.h2o.mojos.server.MojoStore;
import hex.genmodel.MojoModel;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * <p>Servlet that handles API request
 * <pre>{@code
 *   GET /loadmojo?file=...
 * }</pre>
 * This will instantiate a {@link MojoModel} from the given <code>file</code>,
 * storing it in the {@link MojoStore}, and returns an id of the new model
 * (in a plain text format). The file name should be given with absolute path,
 * or otherwise it probably won't be found.</p>
 *
 * <p>If the model cannot instantiated for whatever reason, a 400 error will
 * be raised.</p>
 */
public class LoadMojoHandler extends HttpServlet {

  @Override
  public void doGet(HttpServletRequest request, HttpServletResponse response) {
    try {
      // Verify input parameters
      String mojofile = request.getParameter("file");
      if (mojofile == null)
        throw new IllegalArgumentException("Parameter `file` is missing.");

      // Load the model
      MojoModel model = MojoModel.load(mojofile);
      String id = MojoStore.addModel(model);

      // Produce the response
      response.setContentType("text/plain");
      response.setStatus(HttpServletResponse.SC_OK);
      response.getWriter().println(id);
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

}
