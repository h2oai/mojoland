package ai.h2o.mojos.runtime.models.drf;


import ai.h2o.mojos.runtime.models.tree.TreeMojoModel0;

/**
 * "Distributed Random Forest" MojoModel
 */
public final strictfp class DrfMojoModel0 extends TreeMojoModel0 {
  protected int effectiveNClasses;
  protected boolean binomialDoubleTrees;


  public DrfMojoModel0(String[] columns, String[][] domains) {
    super(columns, domains);
  }

  /** Main scoring function. */
  @SuppressWarnings("unused")
  public final double[] score0(double[] row, double[] preds) {
    super.scoreAllTrees(row, preds, effectiveNClasses);

    // Correct the predictions -- see `DRFModel.toJavaUnifyPreds`
    if (nclasses == 1) {
      // Regression
      preds[0] /= ntrees;
    } else {
      // Classification
      if (nclasses == 2 && !binomialDoubleTrees) {
        // Binomial model
        preds[1] /= ntrees;
        preds[2] = 1.0 - preds[1];
      } else {
        // Multinomial
        double sum = 0;
        for (int i = 1; i <= nclasses; i++) { sum += preds[i]; }
        if (sum > 0)
          for (int i = 1; i <= nclasses; i++) { preds[i] /= sum; }
      }
      if (balanceClasses)
        correctProbabilities(preds, priorClassDistrib, modelClassDistrib);
      preds[0] = getPrediction(preds, priorClassDistrib, row, defaultThreshold);
    }
    return preds;
  }

}
