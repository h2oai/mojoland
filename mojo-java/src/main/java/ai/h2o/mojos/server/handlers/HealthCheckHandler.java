package ai.h2o.mojos.server.handlers;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Handler for
 * <pre>{@code  GET /healthcheck}</pre>
 * request, which can be used by the client to verify that a service running
 * on some port is indeed a {@code MojoServer}. This handler returns an
 * empty return code with HTTP status code 418.
 */
public class HealthCheckHandler extends BaseHandler {

  @Override
  protected void getImpl(HttpServletRequest request, HttpServletResponse response) throws Exception {
    response.setStatus(418);  // I'm a teapot (RFC 2324)
  }

}
