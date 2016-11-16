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

    _model._uuid = readkv("uuid");
    _model._category = ModelCategory.valueOf(readkv("category"));
    _model._supervised = readkv("supervised");
    _model._nfeatures = readkv("n_features");
    _model._nclasses = readkv("n_classes");
    _model._balanceClasses = readkv("balance_classes");
    _model._defaultThreshold = readkv("default_threshold");
    _model._priorClassDistrib = readkv("prior_class_distrib");
    _model._modelClassDistrib = readkv("model_class_distrib");
    _model._offsetColumn = readkv("offset_column");
    String endianness = readkv("endianness");
    if (endianness == null) _model.endianness = ByteOrder.nativeOrder();
    else if (endianness.equals("BIG_ENDIAN")) _model.endianness = ByteOrder.BIG_ENDIAN;
    else if (endianness.equals("LITTLE_ENDIAN")) _model.endianness = ByteOrder.LITTLE_ENDIAN;
    else throw new RuntimeException("Unexpected endianness field: " + endianness);
  }

}
