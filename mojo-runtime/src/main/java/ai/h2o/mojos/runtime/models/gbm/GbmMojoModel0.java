package ai.h2o.mojos.runtime.models.gbm;


import ai.h2o.mojos.runtime.models.tree.DistributionFamily1;
import ai.h2o.mojos.runtime.models.tree.TreeMojoModel0;

import static ai.h2o.mojos.runtime.models.tree.DistributionFamily1.*;

/**
 * "Gradient Boosting Machine" MojoModel
 */
public final strictfp class GbmMojoModel0 extends TreeMojoModel0 {
  protected DistributionFamily1 family;
  protected double initF;


  /** Main scoring function. */
  public final double[] score0(double[] row, double offset, double[] preds) {
    super.scoreAllTrees(row, preds, ntreesPerClass);
    if (family == bernoulli || family == modified_huber) {
      double f = preds[1] + initF + offset;
      preds[2] = family.linkInv(f);
      preds[1] = 1.0 - preds[2];
    } else if (family == multinomial) {
      if (nclasses == 2) {  // 1-tree optimization for binomial
        preds[1] += initF + offset;  // offset is not yet allowed, but added here to be future-proof
        preds[2] = -preds[1];
      }
      GBM_rescale(preds);
    } else { // Regression
      double f = preds[0] + initF + offset;
      preds[0] = family.linkInv(f);
      return preds;
    }
    if (balanceClasses)
      correctProbabilities(preds, priorClassDistrib, modelClassDistrib);
    preds[0] = getPrediction(preds, priorClassDistrib, row, defaultThreshold);
    return preds;
  }

  public double[] score0(double[] row, double[] preds) {
    return score0(row, 0.0, preds);
  }

}
