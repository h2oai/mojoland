package ai.h2o.mojos.server.handlers;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.lang.reflect.InvocationTargetException;
import java.net.MalformedURLException;

/**
 * Base class for all our handlers. Intercepts any exceptions that may occur
 * within the handlers and converts them to a reasonable error response.
 */
public abstract class BaseHandler extends HttpServlet {

  @Override
  public final void doGet(HttpServletRequest request, HttpServletResponse response) {
    try {
      getImpl(request, response);
    } catch (IllegalArgumentException e) {
      makeErrorResponse(e.toString(), 400, response);
    } catch (MalformedURLException e) {
      makeErrorResponse(e.toString(), 404, response);
    } catch (InvocationTargetException e) {
      Throwable oe = e.getCause();
      StringBuilder sb = new StringBuilder(oe.toString()).append("\n\n");
      for (StackTraceElement elem : oe.getStackTrace()) {
        String str = elem.toString();
        if (str.startsWith("ai.h2o.") || str.startsWith("hex.") || str.startsWith("water."))
          sb.append(str).append('\n');
      }
      makeErrorResponse(sb.toString(), 400, response);
    } catch (Exception e) {
      makeErrorResponse(e.toString(), 500, response);
    }
  }


  protected abstract void getImpl(HttpServletRequest request, HttpServletResponse response) throws Exception;

  protected String[] pathParts(HttpServletRequest request) throws MalformedURLException {
    String pathInfo = request.getPathInfo();
    String[] pathParts = pathInfo == null? null : pathInfo.split("/");
    if (pathParts == null || pathParts.length == 0 || !pathParts[0].isEmpty())
      throw new MalformedURLException("Unexpected URL " + request.getRequestURI());
    return pathParts;
  }

  protected PrintWriter makeTextResponse(HttpServletResponse response) throws IOException {
    response.setStatus(200);
    response.setContentType("text/plain");
    return response.getWriter();
  }


  private void makeErrorResponse(String errorMessage, int errorCode, HttpServletResponse response) {
    response.setStatus(errorCode);
    response.setContentType("text/plain");
    try {
      response.getWriter().print(errorMessage);
    } catch (IOException e) {
      response.setStatus(500);
    }
  }
}
