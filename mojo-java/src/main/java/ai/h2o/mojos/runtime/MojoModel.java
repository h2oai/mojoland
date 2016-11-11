package ai.h2o.mojos.runtime;

import ai.h2o.mojos.runtime.readers.FolderMojoReaderBackend;
import ai.h2o.mojos.runtime.readers.MojoReader;
import ai.h2o.mojos.runtime.readers.MojoReaderBackend;
import ai.h2o.mojos.runtime.readers.ZipfileMojoReaderBackend;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;


/**
 * Prediction model based on the persisted binary data.
 */
public abstract class MojoModel {

  /**
   * Primary factory method for constructing MojoModel instances.
   *
   * @param file Name of the .mojo file (or folder) with the model's data. This should be the data retrieved via
   *             the `GET /3/Models/{model_id}/mojo` endpoint.
   * @return New `MojoModel` object.
   * @throws IOException if `file` does not exist, or cannot be read, or does not represent a valid model.
   */
  public static MojoModel load(String file) throws IOException {
    File f = new File(file);
    if (!f.exists())
      throw new FileNotFoundException("File " + file + " cannot be found.");
    MojoReaderBackend cr = f.isDirectory()? new FolderMojoReaderBackend(file)
        : new ZipfileMojoReaderBackend(file);
    return MojoReader.readFrom(cr);
  }

  /**
   * Advanced way of constructing Mojo models by supplying a custom mojoReader.
   *
   * @param mojoReader a class that implements the {@link MojoReaderBackend} interface.
   * @return New `MojoModel` object
   * @throws IOException if the mojoReader does
   */
  public static MojoModel load(MojoReaderBackend mojoReader) throws IOException {
    return MojoReader.readFrom(mojoReader);
  }

}
