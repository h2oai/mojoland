package ai.h2o.mojos.runtime.models;

import ai.h2o.mojos.runtime.readers.MojoReader;
import ai.h2o.mojos.runtime.shared.ModelCategory;

import java.io.IOException;
import java.nio.ByteOrder;
import java.util.Map;

/**
 */
public abstract strictfp class MojoReader0<M extends MojoModel0> extends MojoReader<M> {

  @Override
  protected void readModelData(ParseSetup ps) throws IOException {
    super.readModelData(ps);
    model.names = ps.columns;
    model.domains = parseModelDomains(ps);

    model.uuid = readkv("uuid");
    model.category = readEnum(ModelCategory.class, "category");
    model.supervised = readkv("supervised");
    model.nfeatures = readkv("n_features");
    model.nclasses = readkv("n_classes");
    model.balanceClasses = readkv("balance_classes");
    model.defaultThreshold = readkv("default_threshold");
    model.priorClassDistrib = readkv("prior_class_distrib");
    model.modelClassDistrib = readkv("model_class_distrib");
    model.offsetColumn = readkv("offset_column");
    String endianness = readkv("endianness");
    if (endianness == null) model.endianness = ByteOrder.nativeOrder();
    else if (endianness.equals("BIG_ENDIAN")) model.endianness = ByteOrder.BIG_ENDIAN;
    else if (endianness.equals("LITTLE_ENDIAN")) model.endianness = ByteOrder.LITTLE_ENDIAN;
    else throw new RuntimeException("Unexpected endianness field: " + endianness);
  }


  private String[][] parseModelDomains(ParseSetup ps) throws IOException {
    int n_columns = ps.columns.length;
    String[][] domains = new String[n_columns][];
    for (Map.Entry<Integer, String> e : ps.domains.entrySet()) {
      int col_index = e.getKey();
      String[] info = e.getValue().split(" ", 2);
      int n_elements = Integer.parseInt(info[0]);
      String domfile = info[1];
      String[] domain = new String[n_elements];
      int id = 0;  // domain elements counter
      for (String line: readtext("domains/" + domfile)) {
        domain[id++] = line;
      }
      if (id != n_elements)
        throw new IOException("Not enough elements in the domain file");
      domains[col_index] = domain;
    }
    return domains;
  }
}
