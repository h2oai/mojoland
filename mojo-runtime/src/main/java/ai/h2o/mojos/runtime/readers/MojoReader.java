package ai.h2o.mojos.runtime.readers;

import ai.h2o.mojos.runtime.MojoModel;
import ai.h2o.mojos.runtime.utils.ParseUtils;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;


/**
 * Base class for deserialization of a model from a mojo file. This is
 * effectively a counterpart to `ModelMojoWriter` (in h2o-core).
 * <p>
 * The workflow of this class is the following: first a caller (which is the
 * {@link MojoModel} class) invokes {@code MojoReader.readFrom(backend)}
 * passing a {@link MojoReaderBackend} instance. The {@code readFrom()} method
 * then does preliminary parsing of the <tt>model.ini</tt> file. After that
 * it uses {@link MojoModelFactory} to determine (based on the algo and the
 * version) the appropriate subclass of itself that should handle the reading
 * of the model. Finally the subclass will handle reading the mojo file (with
 * the help of this base class).
 *
 * @param <M> subclass of the MojoModel that the reader will be instantiating.
 */
public abstract class MojoReader<M extends MojoModel> {

  protected M model;

  private MojoReaderBackend reader;
  private Map<String, String> kvstore;

  protected static class ParseSetup {
    String algorithm;
    String version;
    Map<String, String> kvs;
    public String[] columns;
    public Map<Integer, String> domains;
  }


  public static MojoModel readFrom(MojoReaderBackend reader) throws IOException {
    ParseSetup ps = parseModelInfo(reader);
    MojoReader<?> mmr = MojoModelFactory.getMojoReader(ps.algorithm, ps.version);
    mmr.reader = reader;
    mmr.kvstore = ps.kvs;
    mmr.makeModel();
    assert mmr.model != null;
    mmr.readModelData(ps);
    return mmr.model;
  }


  //--------------------------------------------------------------------------------------------------------------------
  // Inheritance interface: MojoReader subclasses are expected to override these methods to provide custom behavior
  //--------------------------------------------------------------------------------------------------------------------

  protected abstract void makeModel();

  protected void readModelData(ParseSetup ps) throws IOException {}


  //--------------------------------------------------------------------------------------------------------------------
  // Interface for subclasses
  //--------------------------------------------------------------------------------------------------------------------

  /**
   * Retrieve value from the model's kv store which was previously put there using `writekv(key, value)`. We will
   * attempt to cast to your expected type, but this is obviously unsafe. Note that the value is deserialized from
   * the underlying string representation using {@link ParseUtils#tryParse(String)}, which occasionally may get the
   * answer wrong.
   * If the `key` is missing in the local kv store, null will be returned. However when assigning to a primitive type
   * this would result in an NPE, so beware.
   */
  @SuppressWarnings("unchecked")
  protected <T> T readkv(String key) {
    return (T) ParseUtils.tryParse(kvstore.get(key));
  }

  protected String readString(String key) {
    return kvstore.get(key);
  }

  protected <T extends Enum<T>> T readEnum(Class<T> klass, String key) {
    return Enum.valueOf(klass, readString(key));
  }

  /**
   * Retrieve binary data previously saved to the mojo file using `writeblob(key, blob)`.
   */
  protected byte[] readblob(String name) throws IOException {
    return reader.getBinaryFile(name);
  }

  /**
   * Retrieve text previously saved using `startWritingTextFile` + `writeln` as an array of lines. Each line is
   * trimmed to remove the leading and trailing whitespace.
   */
  @SuppressWarnings("unused")
  protected Iterable<String> readtext(String name) throws IOException {
    BufferedReader br = reader.getTextFile(name);
    String line;
    ArrayList<String> res = new ArrayList<>(50);
    while (true) {
      line = br.readLine();
      if (line == null) break;
      res.add(line.trim());
    }
    return res;
  }


  //--------------------------------------------------------------------------------------------------------------------
  // Private
  //--------------------------------------------------------------------------------------------------------------------

  private static ParseSetup parseModelInfo(MojoReaderBackend reader) throws IOException {
    ParseSetup ps = new ParseSetup();
    ps.kvs = new HashMap<>(20);

    BufferedReader br = reader.getTextFile("model.ini");
    Pattern kvSplitter = Pattern.compile("\\s*=\\s*");
    Pattern domainSplitter = Pattern.compile(":\\s*");

    int section = 0;
    int icol = 0;     // Index for `ps.columns` array
    String line;
    while ((line = br.readLine()) != null) {
      line = line.trim();
      if (line.startsWith("#") || line.isEmpty()) continue;

      switch (section) {
        case 0:  // File preamble
          if (line.equals("[info]")) {
            section = 1;
          } else
            throw new IOException("Unexpected line before the beginning of the [info] section:\n" + line);
          break;

        case 1:  // [info] section: key-value pairs
          if (line.equals("[columns]")) {
            section = 2;
            if (!ps.kvs.containsKey("n_columns"))
              throw new IOException("`n_columns` variable is missing in the model info.");
            int nCols = Integer.parseInt(ps.kvs.get("n_columns"));
            ps.columns = new String[nCols];
          } else {
            String[] res = kvSplitter.split(line, 2);
            if (res.length != 2)
              throw new IOException("Cannot read a key-value pair from line\n" + line);
            ps.kvs.put(res[0], res[1]);
          }
          break;

        case 2:  // [columns] section: list of columns
          if (line.equals("[domains]")) {
            section = 3;
            ps.domains = new HashMap<>();
          } else {
            if (icol >= ps.columns.length)
              throw new IOException("`n_columns` variable is less than the actual number of columns.");
            ps.columns[icol++] = line;
          }
          break;

        case 3:
          String[] res = domainSplitter.split(line, 2);
          int col_index = Integer.parseInt(res[0]);
          if (ps.domains.containsKey(col_index))
            throw new IOException("Column " + col_index + " has more than one domain declared.");
          if (col_index < 0 || col_index >= ps.columns.length)
            throw new IOException("Invalid column " + col_index + " for domain " + res[1]);
          ps.domains.put(col_index, res[1]);
          break;
      }
    }
    if (section != 3)
      throw new IOException("Some sections are missing from the model.ini file");
    if (icol != ps.columns.length)
      throw new IOException("Not all columns were read when parsing the [columns] section");
    if (!ps.kvs.containsKey("algorithm"))
      throw new IOException("`algorithm` key is missing in the model info");

    // Return the parsed result
    ps.algorithm = ps.kvs.get("algorithm");
    ps.version = ps.kvs.get("mojo_version");
    return ps;
  }

}
