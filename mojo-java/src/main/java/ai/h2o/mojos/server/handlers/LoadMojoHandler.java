package ai.h2o.mojos.server.handlers;

import ai.h2o.mojos.server.core.MojoStore;
import hex.genmodel.MojoModel;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * Servlet that handles API request
 * <pre>{@code
 *   GET /loadmojo?file=...
 * }</pre>
 * This will instantiate a {@link MojoModel} from the given {@code file},
 * storing it in the {@link MojoStore}, and returns an id of the new model
 * (in a plain text format). The file name should be given with absolute path,
 * or otherwise it probably won't be found.
 * <p>
 * If the model cannot instantiated for whatever reason, a 400 error will
 * be raised.
 */
public class LoadMojoHandler extends BaseHandler {

  @Override
  public void getImpl(HttpServletRequest request, HttpServletResponse response) throws IOException {
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
  }

}
