package ai.h2o.mojos.runtime.models;

import ai.h2o.mojos.runtime.readers.MojoReader;
import ai.h2o.mojos.runtime.shared.ModelCategory;

import java.io.IOException;
import java.nio.ByteOrder;

/**
 */
public abstract strictfp class MojoReader0<M extends MojoModel0> extends MojoReader<M> {

  @Override
  protected void readModelData() throws IOException {
    super.readModelData();

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

}
