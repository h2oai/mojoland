package ai.h2o.mojos.runtime.models.tree;

import ai.h2o.mojos.runtime.readers.MojoReader;

import java.io.IOException;

/**
 */
public abstract class TreeMojoReader0<M extends TreeMojoModel0> extends MojoReader<M> {

  @Override
  protected void readModelData() throws IOException {
    // In mojos v=0.0 this info wasn't saved.
    Integer tpc = readkv("n_trees_per_class");
    if (tpc == null) {
      Boolean bdt = readkv("binomial_double_trees");  // This flag exists only for DRF models
      tpc = _model._nclasses == 2 && (bdt == null || bdt)? 1 : _model._nclasses;
    }

    _model._ntrees = readkv("n_trees");
    _model._ntrees_per_class = tpc;
    _model._compressed_trees = new byte[_model._ntrees * tpc][];

    for (int j = 0; j < _model._ntrees; j++)
      for (int i = 0; i < tpc; i++)
        _model._compressed_trees[i * _model._ntrees + j] = readblob(String.format("trees/t%02d_%03d.bin", i, j));
  }

}
