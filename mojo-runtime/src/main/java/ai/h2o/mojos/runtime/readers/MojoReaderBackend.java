package ai.h2o.mojos.runtime.readers;

import java.io.BufferedReader;
import java.io.Closeable;
import java.io.IOException;


/**
 * Interface representing a class capable of reading mojos. Usually the class
 * implementing this interface will have a constructor taking an "address" of
 * the mojo file that should be read. The class would then have to implement
 * the logic for reading the referred mojo from the source.
 * <p>
 * For example, a hypothetical <code>MysqlMojoReaderBackend</code> may have
 * a constructor taking the URL of the server, connection credentials, and
 * a SQL query for retrieving the mojo record. The class would then implement
 * the logic for connecting to the database and fetching the mojo (whole or in
 * parts). It would also throw an {@link IOException} if anything fails.
 * <p>
 * The actual interface that the class needs to implement is for reading either
 * text or binary fragments from within the mojo. This is because a
 * <code>.mojo</code> file is actually a zip archive, and hence it contains
 * several "files" inside. The user may decide to repackage the mojo contents
 * into a different container: a plain directory for easier access, a
 * <code>.7z</code> file for better compression, an encrypted Zip file for
 * better security, etc. If the reader doesn't wish to re-package the mojo
 * contents and only retrieve it from non-filesystem source, then it may
 * create a temporary .mojo file and pass it to the
 * {@link MojofileMojoReaderBackend} reader.
 */
public interface MojoReaderBackend extends Closeable {

  /** Retrieve text content inside the mojo, as a {@link BufferedReader}. */
  BufferedReader getTextFile(String filename) throws IOException;

  /** Retrieve binary content inside the mojo, as a <code>byte[]</code> array. */
  byte[] getBinaryFile(String filename) throws IOException;

}
