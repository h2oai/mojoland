package ai.h2o.mojos.server.handlers;

import ai.h2o.mojos.server.MojoApp;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * <pre>{@code    POST /shutdown}</pre>
 */
public class ShutdownHandler extends BaseHandler {

  @Override protected void getImpl(HttpServletRequest request, HttpServletResponse response) throws Exception {}

  @Override public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
    response.setStatus(HttpServletResponse.SC_ACCEPTED);
    response.flushBuffer();
    new Thread() {
      @Override public void run() {
        try {
          MojoApp.server.stop();
        } catch (Exception e) {
          System.err.println("Error when stopping Jetty: " + e);
        }
      }
    }.start();
  }
}
