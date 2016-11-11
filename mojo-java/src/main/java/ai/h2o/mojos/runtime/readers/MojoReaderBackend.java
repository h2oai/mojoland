package ai.h2o.mojos.runtime.readers;

import java.io.BufferedReader;
import java.io.IOException;

/**
 */
public interface MojoReaderBackend {

  BufferedReader getTextFile(String filename) throws IOException;

  byte[] getBinaryFile(String filename) throws IOException;
}
