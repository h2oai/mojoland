package ai.h2o.mojos.runtime.models.drf;

import ai.h2o.mojos.runtime.models.tree.TreeMojoReader0;

import java.io.IOException;

/**
 */
public final strictfp class DrfMojoReader0 extends TreeMojoReader0<DrfMojoModel0> {

  @Override protected void makeModel() {
    model = new DrfMojoModel0();
  }

  @Override
  protected void readModelData(ParseSetup ps) throws IOException {
    super.readModelData(ps);
    model.binomialDoubleTrees = readkv("binomial_double_trees");
    model.effectiveNClasses = model.nclasses() == 2 && !model.binomialDoubleTrees ? 1 : model.nclasses();
  }
}
