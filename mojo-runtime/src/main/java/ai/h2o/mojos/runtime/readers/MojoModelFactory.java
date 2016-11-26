package ai.h2o.mojos.runtime.readers;

import ai.h2o.mojos.runtime.models.drf.DrfMojoReader0;
import ai.h2o.mojos.runtime.models.gbm.GbmMojoReader0;

import java.io.IOException;

/**
 * Factory class for instantiating specific MojoModel classes based on algo
 * name and version. This is a helper class for {@link MojoReader}.
 */
class MojoModelFactory {

  public static MojoReader<?> getMojoReader(String algo, String version) throws IOException {
    if (algo == null || version == null)
      throw new IOException("Unable to find information about the model's version and algorithm.");

    // Decode the version number into major/minor parts
    double dversion = Double.parseDouble(version);
    int majver = (int) Math.floor(dversion);
    int minver = (int) Math.round(100 * (dversion - majver));
    if (majver == 1 && minver == 0) majver = 0;

    MojoReader<?> reader;
    switch (algo) {
      case "Gradient Boosting Method":
      case "Gradient Boosting Machine":
        reader = getGbmMojoReader(majver);
        break;

      case "Distributed Random Forest":
        reader = getDrfMojoReader(majver);
        break;

      /*
      case "Deep Water":
        return new DeepwaterMojoReader();

      case "Generalized Low Rank Modeling":
      case "Generalized Low Rank Model":
        return new GlrmMojoReader();
      */

      default:
        throw new IOException("Unsupported MOJO algorithm: " + algo);
    }

    if (reader == null)
      throw new IOException(String.format("Unable to instantiate mojo of version %d.%02d", majver, minver));
    return reader;
  }


  private static MojoReader<?> getGbmMojoReader(int majver) throws IOException {
    if (majver == 0) return new GbmMojoReader0();
    return null;
  }


  private static MojoReader<?> getDrfMojoReader(int majver) throws IOException {
    if (majver == 0) return new DrfMojoReader0();
    return null;
  }

}
