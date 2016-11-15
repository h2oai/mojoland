package ai.h2o.mojos.runtime.readers;

import ai.h2o.mojos.runtime.MojoModel;
import hex.genmodel.utils.ParseUtils;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


/**
 * Helper class to deserialize a model from MOJO format. This is a counterpart to `ModelMojoWriter`.
 */
public abstract class MojoReader<M extends MojoModel> {

  protected M _model;

  private MojoReaderBackend _reader;
  private Map<String, Object> _lkv;


  public static MojoModel readFrom(MojoReaderBackend reader) throws IOException {
    Map<String, Object> info = parseModelInfo(reader);
    String algo = (String) info.get("algorithm");
    String version = (String) info.get("mojo_version");
    MojoReader<?> mmr = MojoModelFactory.getMojoReader(algo, version);
    mmr._lkv = info;
    mmr._reader = reader;
    mmr.readAll();
    return mmr._model;
  }


  //--------------------------------------------------------------------------------------------------------------------
  // Inheritance interface: MojoReader subclasses are expected to override these methods to provide custom behavior
  //--------------------------------------------------------------------------------------------------------------------

  protected abstract void readModelData() throws IOException;

  protected abstract M makeModel(String[] columns, String[][] domains);


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
    return (T) _lkv.get(key);
  }

  /**
   * Retrieve binary data previously saved to the mojo file using `writeblob(key, blob)`.
   */
  protected byte[] readblob(String name) throws IOException {
    return _reader.getBinaryFile(name);
  }

  /**
   * Retrieve text previously saved using `startWritingTextFile` + `writeln` as an array of lines. Each line is
   * trimmed to remove the leading and trailing whitespace.
   */
  protected Iterable<String> readtext(String name) throws IOException {
    BufferedReader br = _reader.getTextFile(name);
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

  private void readAll() throws IOException {
    String[] columns = (String[]) _lkv.get("[columns]");
    String[][] domains = parseModelDomains(columns.length);
    _model = makeModel(columns, domains);
    /*
    _model._uuid = readkv("uuid");
    _model._category = hex.ModelCategory.valueOf((String) readkv("category"));
    _model._supervised = readkv("supervised");
    _model._nfeatures = readkv("n_features");
    _model._nclasses = readkv("n_classes");
    _model._balanceClasses = readkv("balance_classes");
    _model._defaultThreshold = readkv("default_threshold");
    _model._priorClassDistrib = readkv("prior_class_distrib");
    _model._modelClassDistrib = readkv("model_class_distrib");
    _model._offsetColumn = readkv("offset_column");
    */
    readModelData();
  }

  private static Map<String, Object> parseModelInfo(MojoReaderBackend reader) throws IOException {
    BufferedReader br = reader.getTextFile("model.ini");
    Map<String, Object> info = new HashMap<>();
    String line;
    int section = 0;
    int ic = 0;  // Index for `columns` array
    String[] columns = new String[0];  // array of column names, will be initialized later
    Map<Integer, String> domains = new HashMap<>();  // map of (categorical column index => name of the domain file)
    while (true) {
      line = br.readLine();
      if (line == null) break;
      line = line.trim();
      if (line.startsWith("#") || line.isEmpty()) continue;
      if (line.equals("[info]"))
        section = 1;
      else if (line.equals("[columns]")) {
        section = 2;  // Enter the [columns] section
        Integer n_columns = (Integer) info.get("n_columns");
        if (n_columns == null)
          throw new IOException("`n_columns` variable is missing in the model info.");
        columns = new String[n_columns];
        info.put("[columns]", columns);
      } else if (line.equals("[domains]")) {
        section = 3; // Enter the [domains] section
        info.put("[domains]", domains);
      } else if (section == 1) {
        // [info] section: just parse key-value pairs and store them into the `info` map.
        String[] res = line.split("\\s*=\\s*", 2);
        info.put(res[0], res[0].equals("uuid")? res[1] : ParseUtils.tryParse(res[1]));
      } else if (section == 2) {
        // [columns] section
        if (ic >= columns.length)
          throw new IOException("`n_columns` variable is too small.");
        columns[ic++] = line;
      } else if (section == 3) {
        // [domains] section
        String[] res = line.split(":\\s*", 2);
        int col_index = Integer.parseInt(res[0]);
        domains.put(col_index, res[1]);
      }
    }
    return info;
  }

  private String[][] parseModelDomains(int n_columns) throws IOException {
    String[][] domains = new String[n_columns][];
    // noinspection unchecked
    Map<Integer, String> domass = (Map) _lkv.get("[domains]");
    for (Map.Entry<Integer, String> e : domass.entrySet()) {
      int col_index = e.getKey();
      // There is a file with categories of the response column, but we ignore it.
      if (col_index >= n_columns) continue;
      String[] info = e.getValue().split(" ", 2);
      int n_elements = Integer.parseInt(info[0]);
      String domfile = info[1];
      String[] domain = new String[n_elements];
      BufferedReader br = _reader.getTextFile("domains/" + domfile);
      String line;
      int id = 0;  // domain elements counter
      while (true) {
        line = br.readLine();
        if (line == null) break;
        domain[id++] = line;
      }
      if (id != n_elements)
        throw new IOException("Not enough elements in the domain file");
      domains[col_index] = domain;
    }
    return domains;
  }

}
