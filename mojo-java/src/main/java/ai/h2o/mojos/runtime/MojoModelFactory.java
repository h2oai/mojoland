package ai.h2o.mojos.runtime;

import ai.h2o.mojos.runtime.readers.MojoReader;

import java.io.IOException;

/**
 * Factory class for instantiating specific MojoModel classes based on algo
 * name and version.
 */
public class MojoModelFactory {

  public static MojoReader<?> getMojoReader(String algo) throws IOException {
    if (algo == null)
      throw new IOException("Unable to find information about the model's algorithm.");

    switch (algo) {
      /*
      case "Distributed Random Forest":
        return new DrfMojoReader();

      case "Gradient Boosting Method":
      case "Gradient Boosting Machine":
        return new GbmMojoReader();

      case "Deep Water":
        return new DeepwaterMojoReader();

      case "Generalized Low Rank Modeling":
      case "Generalized Low Rank Model":
        return new GlrmMojoReader();
      */

      default:
        throw new IOException("Unsupported MOJO algorithm: " + algo);
    }
  }

}
