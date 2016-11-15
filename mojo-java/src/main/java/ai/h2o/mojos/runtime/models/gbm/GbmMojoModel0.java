package ai.h2o.mojos.runtime.models.gbm;


import ai.h2o.mojos.runtime.models.tree.DistributionFamily1;
import ai.h2o.mojos.runtime.models.tree.TreeMojoModel0;

import static ai.h2o.mojos.runtime.models.tree.DistributionFamily1.*;

/**
 * "Gradient Boosting Machine" MojoModel
 */
public final class GbmMojoModel0 extends TreeMojoModel0 {
  public DistributionFamily1 _family;
  public double _init_f;


  public GbmMojoModel0(String[] columns, String[][] domains) {
    super(columns, domains);
  }

  /** Main scoring function. */
  public final double[] score0(double[] row, double offset, double[] preds) {
    super.scoreAllTrees(row, preds, _ntrees_per_class);
    if (_family == bernoulli || _family == modified_huber) {
      double f = preds[1] + _init_f + offset;
      preds[2] = _family.linkInv(f);
      preds[1] = 1.0 - preds[2];
    } else if (_family == multinomial) {
      if (_nclasses == 2) {  // 1-tree optimization for binomial
        preds[1] += _init_f + offset;  // offset is not yet allowed, but added here to be future-proof
        preds[2] = -preds[1];
      }
      GBM_rescale(preds);
    } else { // Regression
      double f = preds[0] + _init_f + offset;
      preds[0] = _family.linkInv(f);
      return preds;
    }
    if (_balanceClasses)
      correctProbabilities(preds, _priorClassDistrib, _modelClassDistrib);
    preds[0] = getPrediction(preds, _priorClassDistrib, row, _defaultThreshold);
    return preds;
  }

  public double[] score0(double[] row, double[] preds) {
    return score0(row, 0.0, preds);
  }

}
