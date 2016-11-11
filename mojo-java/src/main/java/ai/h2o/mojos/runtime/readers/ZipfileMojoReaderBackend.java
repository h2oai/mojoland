package ai.h2o.mojos.runtime.readers;

import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

/**
 */
public class ZipfileMojoReaderBackend implements MojoReaderBackend {
  private ZipFile zf;

  public ZipfileMojoReaderBackend(String archivename) throws IOException {
    zf = new ZipFile(archivename);
  }

  @Override
  public BufferedReader getTextFile(String filename) throws IOException {
    InputStream input = zf.getInputStream(zf.getEntry(filename));
    return new BufferedReader(new InputStreamReader(input));
  }

  @Override
  public byte[] getBinaryFile(String filename) throws IOException {
    ZipEntry za = zf.getEntry(filename);
    if (za == null)
      throw new IOException("Tree file " + filename + " not found");
    byte[] out = new byte[(int) za.getSize()];
    DataInputStream dis = new DataInputStream(zf.getInputStream(za));
    dis.readFully(out);
    return out;
  }

}
