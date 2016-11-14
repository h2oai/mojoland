package ai.h2o.mojos.server.handlers;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 */
public class HealthCheckHandler extends BaseHandler {

  @Override
  protected void getImpl(HttpServletRequest request, HttpServletResponse response) throws Exception {
    response.setStatus(418);  // I'm a teapot (RFC 2324)
  }

}
