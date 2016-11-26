package ai.h2o.mojos.runtime;

import ai.h2o.mojos.runtime.readers.*;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;


/**
 * Prediction model based on the persisted binary data ("mojo file").
 */
public abstract class MojoModel {

  /**
   * Primary factory method for constructing MojoModel instances.
   *
   * @param file Name of the model's .mojo file. This file can be obtained
   *             either through the <code>GET /3/Models/{model_id}/mojo</code>
   *             REST API endpoint, or <code>model.download_mojo()</code>
   *             method call in Python/R clients.
   *
   * @return New <code>MojoModel</code> object.
   * @throws IOException if <code>file</code> does not exist, or cannot be
   *                     read, or does not represent a valid model.
   */
  @SuppressWarnings("unused")
  public static MojoModel load(String file) throws IOException {
    File f = new File(file);
    if (!f.isFile())
      throw new FileNotFoundException("File " + file + " cannot be found.");
    MojoReaderBackend cr = new MojofileMojoReaderBackend(file);
    return MojoReader.readFrom(cr);
  }


  /**
   * Advanced way of constructing Mojo models by supplying a custom
   * mojo reader backend. For example a {@link FolderMojoReaderBackend} can be
   * used to read an unzipped mojo model from a folder. Alternatively, you can
   * implement your own backend, for example to read models stored on network
   * locations, or load them from a database, etc.
   *
   * @param mojoReader a class implementing the {@link MojoReaderBackend}
   *                   interface.
   *
   * @return New <code>MojoModel</code> object.
   * @throws IOException if mojo reader fails to read the model, or if the
   *                     model retrieved is not valid.
   */
  @SuppressWarnings("unused")
  public static MojoModel load(MojoReaderBackend mojoReader) throws IOException {
    return MojoReader.readFrom(mojoReader);
  }

}
