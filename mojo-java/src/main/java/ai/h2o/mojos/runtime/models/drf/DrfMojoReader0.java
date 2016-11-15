package ai.h2o.mojos.runtime.models.drf;

import ai.h2o.mojos.runtime.models.tree.TreeMojoReader0;

import java.io.IOException;

/**
 */
public class DrfMojoReader0 extends TreeMojoReader0<DrfMojoModel0> {

  @Override
  protected void readModelData() throws IOException {
    super.readModelData();
    _model._binomial_double_trees = readkv("binomial_double_trees");
    _model._effective_n_classes = _model.nclasses() == 2 && !_model._binomial_double_trees ? 1 : _model.nclasses();
  }

  @Override
  protected DrfMojoModel0 makeModel(String[] columns, String[][] domains) {
    return new DrfMojoModel0(columns, domains);
  }
}
