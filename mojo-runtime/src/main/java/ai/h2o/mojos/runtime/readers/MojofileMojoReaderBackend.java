package ai.h2o.mojos.runtime.readers;

import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

/**
 * Backend for reading <code>.mojo</code> files.
 */
public class MojofileMojoReaderBackend implements MojoReaderBackend {
  private ZipFile zf;


  public MojofileMojoReaderBackend(String archivename) throws IOException {
    zf = new ZipFile(archivename);
  }

  @Override
  public BufferedReader getTextFile(String filename) throws IOException {
    InputStream input = zf.getInputStream(getEntry(filename));
    return new BufferedReader(new InputStreamReader(input));
  }

  @Override
  public byte[] getBinaryFile(String filename) throws IOException {
    ZipEntry entry = getEntry(filename);
    byte[] out = new byte[(int) entry.getSize()];
    DataInputStream dis = new DataInputStream(zf.getInputStream(entry));
    dis.readFully(out);
    return out;
  }

  @Override
  public void close() throws IOException {
    zf.close();
  }


  private ZipEntry getEntry(String filename) throws IOException {
    ZipEntry ze = zf.getEntry(filename);
    if (ze == null)
      throw new IOException("Tree file " + filename + " not found");
    return ze;
  }
}
