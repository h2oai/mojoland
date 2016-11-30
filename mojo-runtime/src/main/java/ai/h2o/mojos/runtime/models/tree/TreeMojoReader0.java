package ai.h2o.mojos.runtime.models.tree;

import ai.h2o.mojos.runtime.models.MojoReader0;

import java.io.IOException;

/**
 */
public abstract strictfp class TreeMojoReader0<M extends TreeMojoModel0> extends MojoReader0<M> {

  @Override
  protected void readModelData(ParseSetup ps) throws IOException {
    super.readModelData(ps);
    // In mojos v=0.0 this info wasn't saved.
    Integer tpc = readkv("n_trees_per_class");
    if (tpc == null) {
      Boolean bdt = readkv("binomial_double_trees");  // This flag exists only for DRF models
      tpc = model.nclasses() == 2 && (bdt == null || !bdt)? 1 : model.nclasses();
    }

    model.ntrees = readkv("n_trees");
    model.ntreesPerClass = tpc;
    model.compressedTrees = new byte[model.ntrees * tpc][];

    for (int j = 0; j < model.ntrees; j++)
      for (int i = 0; i < tpc; i++)
        model.compressedTrees[i * model.ntrees + j] = readblob(String.format("trees/t%02d_%03d.bin", i, j));
  }

}