package ai.h2o.mojos.runtime.models.drf;


import ai.h2o.mojos.runtime.models.tree.TreeMojoModel0;

/**
 * "Distributed Random Forest" MojoModel
 */
public final class DrfMojoModel0 extends TreeMojoModel0 {
  public int _effective_n_classes;
  public boolean _binomial_double_trees;


  public DrfMojoModel0(String[] columns, String[][] domains) {
    super(columns, domains);
  }

  /** Main scoring function. */
  @SuppressWarnings("unused")
  public final double[] score0(double[] row, double[] preds) {
    super.scoreAllTrees(row, preds, _effective_n_classes);

    // Correct the predictions -- see `DRFModel.toJavaUnifyPreds`
    if (_nclasses == 1) {
      // Regression
      preds[0] /= _ntrees;
    } else {
      // Classification
      if (_nclasses == 2 && !_binomial_double_trees) {
        // Binomial model
        preds[1] /= _ntrees;
        preds[2] = 1.0 - preds[1];
      } else {
        // Multinomial
        double sum = 0;
        for (int i = 1; i <= _nclasses; i++) { sum += preds[i]; }
        if (sum > 0)
          for (int i = 1; i <= _nclasses; i++) { preds[i] /= sum; }
      }
      if (_balanceClasses)
        correctProbabilities(preds, _priorClassDistrib, _modelClassDistrib);
      preds[0] = getPrediction(preds, _priorClassDistrib, row, _defaultThreshold);
    }
    return preds;
  }

}
