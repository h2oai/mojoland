package ai.h2o.mojos.runtime.models.gbm;

import ai.h2o.mojos.runtime.models.tree.DistributionFamily1;
import ai.h2o.mojos.runtime.models.tree.TreeMojoReader0;

import java.io.IOException;

/**
 */
public final strictfp class GbmMojoReader0 extends TreeMojoReader0<GbmMojoModel0> {

  @Override
  protected void readModelData() throws IOException {
    super.readModelData();
    _model._family = DistributionFamily1.valueOf(readkv("distribution"));
    _model._init_f = readkv("init_f");
  }

  @Override
  protected GbmMojoModel0 makeModel(String[] columns, String[][] domains) {
    return new GbmMojoModel0(columns, domains);
  }

}
