package ai.h2o.mojos.server.handlers;

import ai.h2o.mojos.server.core.MojoApi;
import ai.h2o.mojos.server.core.MojoStore;
import hex.genmodel.MojoModel;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.MalformedURLException;


/**
 * This servlet handles several mojo-api related requests.
 * <br>
 * <br>
 * First endpoint is:
 * <pre>{@code    GET /mojos/{model_id}}</pre>
 * Returns mojo's public API: list of methods supported together with their
 * argument types. More specifically, the response will be in plain text format
 * each line having a single api method in Java traditional form
 * <pre>{@code    {returnType} {methodName}({arg1Type}, ..., {argNType});}</pre>
 * The only difference is that <code>methodName</code>s are mangled in case
 * they are overloaded in the mojo's class.
 * <br>
 * <br>
 * The second endpoint is
 * <pre>{@code    GET /mojos/{model_id}/{method}?arg1=...&...&argN=...}</pre>
 * This will execute <code>method</code> on the model <code>model_id</code>,
 * passing arguments <code>arg1</code>, ..., <code>argN</code>. The name of
 * the method must be exactly as given by the first endpoint. In particular,
 * if the method is overloaded, then this name will be mangled to make it
 * unique.<br>
 * The endpoint will produce a plain text file with
 * <br>
 * <br>
 * Lastly, endpoint
 * <pre>{@code    DELETE /mojos/{model_id}}</pre>
 * removes a previously loaded model.
 */
public class MojoApiHandler extends BaseHandler {

  @Override
  protected void getImpl(HttpServletRequest request, HttpServletResponse response) throws Exception {
    String[] pathParts = pathParts(request);
    if (pathParts.length == 2)
      getModelApi(pathParts[1], response);
    else if (pathParts.length == 3)
      executeModelMethod(pathParts[1], pathParts[2], request, response);
    else
      throw new MalformedURLException("Unexpected URL " + request.getRequestURI());
  }

  @Override
  public void doDelete(HttpServletRequest request, HttpServletResponse response) throws IOException {
    String pathInfo = request.getPathInfo();
    if (pathInfo == null || pathInfo.length() < 2 || !pathInfo.startsWith("/"))
      throw new MalformedURLException("Expected URL of the form /mojos/{mojo_id}");

    String modelId = pathInfo.substring(1);
    MojoStore.delModel(modelId);
  }

  private void getModelApi(String modelId, HttpServletResponse response) throws IOException {
    // Verify validity of input parameters
    MojoModel model = MojoStore.getModel(modelId);
    MojoApi api = MojoStore.getModelApi(model);
    if (model == null || api == null)
      throw new IllegalArgumentException("Model " + modelId + " was not loaded");

    // Write the output
    PrintWriter out = makeTextResponse(response);
    for (MojoApi.ApiMethod method : api.listMethods())
      out.println(method.signature());
  }

  private void executeModelMethod(
      String modelId,
      String methodName,
      HttpServletRequest request,
      HttpServletResponse response
  ) throws Exception {
    // Verify validity of input parameters
    MojoModel model = MojoStore.getModel(modelId);
    MojoApi api = MojoStore.getModelApi(model);
    if (model == null || api == null)
      throw new IllegalArgumentException("Model " + modelId + " was not loaded");
    if (!api.hasMethodWithUniqueName(methodName)) {
      if (api.hasMethodWithName(methodName))
        throw new IllegalArgumentException("Class " + api.name() + " has multiple methods with name " + methodName);
      else
        throw new IllegalArgumentException("Class " + api.name() + " doesn't have a method with name " + methodName);
    }

    // Execute the request
    MojoApi.ApiMethod methodApi = api.getMethodByUniqueName(methodName);
    int nArgs = methodApi.numArgs();
    String[] queryArgs = new String[nArgs];
    for (int i = 1; i <= nArgs; i++)
      queryArgs[i - 1] = request.getParameter("arg" + i);
    String result = methodApi.invoke(model, queryArgs);

    // Write the output
    PrintWriter out = makeTextResponse(response);
    out.println(result);
  }
}
