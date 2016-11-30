package ai.h2o.mojos.runtime.models.gbm;

import ai.h2o.mojos.runtime.models.tree.DistributionFamily1;
import ai.h2o.mojos.runtime.models.tree.TreeMojoReader0;

import java.io.IOException;

/**
 */
public final strictfp class GbmMojoReader0 extends TreeMojoReader0<GbmMojoModel0> {

  @Override protected void makeModel() {
    model = new GbmMojoModel0();
  }

  @Override
  protected void readModelData(ParseSetup ps) throws IOException {
    super.readModelData(ps);
    model.family = readEnum(DistributionFamily1.class, "distribution");
    model.initF = readkv("init_f");
  }

}