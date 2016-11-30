package ai.h2o.mojos.runtime.models;

import ai.h2o.mojos.runtime.MojoModel;
import ai.h2o.mojos.runtime.interfaces.IGenModel;
import ai.h2o.mojos.runtime.interfaces.IGeneratedModel;
import ai.h2o.mojos.runtime.shared.ModelCategory;

import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;


/**
 *
 */
@SuppressWarnings("unused")
public abstract strictfp class MojoModel0 extends MojoModel implements IGenModel, IGeneratedModel {

  /** Column names; last is response for supervised models */
  protected String[] names;

  /** Categorical (factor/enum) mappings, per column.  Null for non-enum cols.
   *  Columns match the post-init cleanup columns.  The last column holds the
   *  response col enums for SupervisedModels.  */
  protected String[][] domains;

  /** Name of the column with offsets (used for certain types of models). */
  protected String offsetColumn;

  protected ModelCategory category;
  protected String uuid;
  protected boolean supervised;
  protected int nfeatures;
  protected int nclasses;
  protected boolean balanceClasses;
  protected double defaultThreshold;
  protected double[] priorClassDistrib;
  protected double[] modelClassDistrib;
  protected ByteOrder endianness;


  //------------------------------------------------------------------------------------------------------------------
  // IGenModel interface
  //------------------------------------------------------------------------------------------------------------------

  public boolean isSupervised() { return supervised; }
  public int nfeatures() { return nfeatures; }
  public int nclasses() { return nclasses; }
  public ModelCategory getModelCategory() { return category; }


  //--------------------------------------------------------------------------------------------------------------------
  // IGeneratedModel interface
  //--------------------------------------------------------------------------------------------------------------------

  public String getUUID() { return uuid; }

  /** Returns number of columns used as input for training (i.e., exclude response and offset columns). */
  @Override public int getNumCols() {
    return nfeatures();
  }

  /** The names of all columns used, including response and offset columns. */
  @Override public String[] getNames() {
    return names;
  }

  /** The name of the response column. */
  @Override public String getResponseName() {
    return names[getResponseIdx()];
  }

  /** Returns the index of the response column inside getDomains(). */
  @Override public int getResponseIdx() {
    if (!isSupervised())
      throw new UnsupportedOperationException("Cannot provide response index for unsupervised models.");
    return domains.length - 1;
  }

  /** Get number of classes in the given column.
   * Return number greater than zero if the column is categorical or -1 if the column is numeric. */
  @Override public int getNumClasses(int colIdx) {
    String[] domval = getDomainValues(colIdx);
    return domval != null? domval.length : -1;
  }

  /** Return a number of classes in response column. */
  @Override public int getNumResponseClasses() {
    if (!isClassifier())
      throw new UnsupportedOperationException("Cannot provide number of response classes for non-classifiers.");
    return nclasses();
  }

  /** Returns true if this model represents a classifier, else it is used for regression. */
  @Override public boolean isClassifier() {
    ModelCategory cat = getModelCategory();
    return cat == ModelCategory.Binomial || cat == ModelCategory.Multinomial;
  }

  /** Returns true if this model represents an AutoEncoder. */
  @Override public boolean isAutoEncoder() {
    return getModelCategory() == ModelCategory.AutoEncoder;
  }

  /** Gets domain of the given column. */
  @Override public String[] getDomainValues(String name) {
    int colIdx = getColIdx(name);
    return colIdx != -1 ? getDomainValues(colIdx) : null;
  }

  /** Returns domain values for the i-th column. */
  @Override public String[] getDomainValues(int i) {
    return getDomainValues()[i];
  }

  /** Returns domain values for all columns, including the response column. */
  @Override public String[][] getDomainValues() {
    return domains;
  }

  /** Returns index of a column with given name, or -1 if the column is not found. */
  @Override public int getColIdx(String name) {
    String[] names = getNames();
    for (int i = 0; i < names.length; i++) if (names[i].equals(name)) return i;
    return -1;
  }

  /** Maps given column's categorical to the integer used by this model (returns -1 if mapping not found). */
  @Override public int mapEnum(int colIdx, String enumValue) {
    String[] domain = getDomainValues(colIdx);
    if (domain != null)
      for (int i = 0; i < domain.length; i++)
        if (enumValue.equals(domain[i]))
          return i;
    return -1;
  }

  /** Returns the expected size of preds array which is passed to `predict(double[], double[])` function. */
  @Override public int getPredsSize() {
    return isClassifier()? 1 + getNumResponseClasses() : 2;
  }

  public int getPredsSize(ModelCategory mc) {
    return (mc == ModelCategory.DimReduction)? nclasses() :
        (mc == ModelCategory.AutoEncoder)? nfeatures() : getPredsSize();
  }


  //--------------------------------------------------------------------------------------------------------------------
  // Static helpers
  //--------------------------------------------------------------------------------------------------------------------

  /**
   * Correct a given list of class probabilities produced as a prediction by a model back to prior class distribution
   *
   * <p>The implementation is based on Eq. (27) in  <a href="http://gking.harvard.edu/files/0s.pdf">the paper</a>.
   *
   * @param scored list of class probabilities beginning at index 1
   * @param priorClassDist original class distribution
   * @param modelClassDist class distribution used for model building (e.g., data was oversampled)
   * @return corrected list of probabilities
   */
  protected static double[] correctProbabilities(double[] scored, double[] priorClassDist, double[] modelClassDist) {
    double probsum=0;
    for( int c=1; c<scored.length; c++ ) {
      final double original_fraction = priorClassDist[c-1];
      final double oversampled_fraction = modelClassDist[c-1];
      assert(!Double.isNaN(scored[c])) : "Predicted NaN class probability";
      if (original_fraction != 0 && oversampled_fraction != 0) scored[c] *= original_fraction / oversampled_fraction;
      probsum += scored[c];
    }
    if (probsum>0) for (int i=1;i<scored.length;++i) scored[i] /= probsum;
    return scored;
  }


  /** Utility function to get a best prediction from an array of class
   *  prediction distribution.  It returns the index of the max. probability (if that exists).
   *  In the case of ties, it samples from the tied classes with the likelihood given by the prior probabilities.
   *  @param preds an array of prediction distribution.  Length of arrays is equal to a number of classes+1.
   *  @param priorClassDist prior class probabilities (used to break ties)
   *  @param data Test data
   *  @param threshold threshold for binary classifier
   * @return the best prediction (index of class, zero-based)
   */
  protected static int getPrediction(double[] preds, double[] priorClassDist, double data[], double threshold) {
    if (preds.length == 3) {
      return (preds[2] >= threshold) ? 1 : 0; //no tie-breaking
    }
    List<Integer> ties = new ArrayList<>();
    ties.add(0);
    int best=1, tieCnt=0;   // Best class; count of ties
    for( int c=2; c<preds.length; c++) {
      if( preds[best] < preds[c] ) {
        best = c;               // take the max index
        tieCnt=0;               // No ties
      } else if (preds[best] == preds[c]) {
        tieCnt++;               // Ties
        ties.add(c-1);
      }
    }
    if( tieCnt==0 ) return best-1; // Return zero-based best class

    long hash = 0;              // hash for tie-breaking
    if( data != null )
      for( double d : data ) hash ^= Double.doubleToRawLongBits(d) >> 6; // drop 6 least significants bits of mantissa (layout of long is: 1b sign, 11b exp, 52b mantisa)

    if (priorClassDist!=null) {
      assert(preds.length==priorClassDist.length+1);
      // Tie-breaking based on prior probabilities
      // Example: probabilities are 0.4, 0.2, 0.4 for a 3-class problem with priors 0.7, 0.1, 0.2
      // Probability of predicting class 1 should be higher than for class 3 based on the priors
      double sum = 0;
      for (Integer i : ties) { //ties = [0, 2]
        sum += priorClassDist[i]; //0.7 + 0.2
      }
      // sum is now 0.9
      Random rng = new Random(hash);
      double tie = rng.nextDouble(); //for example 0.4135 -> should pick the first of the ties, since it occupies 0.7777 = 0.7/0.9 of the 0...1 range, and 0.4135 < 0.7777
      double partialSum = 0;
      for (Integer i : ties) {
        partialSum += priorClassDist[i] / sum; //0.7777 at first iteration, 1.0000 at second iteration
        if (tie <= partialSum)
          return i;
      }
    }

    // Tie-breaking logic (should really never be triggered anymore)
    double res = preds[best];    // One of the tied best results
    int idx = (int)hash%(tieCnt+1);  // Which of the ties we'd like to keep
    for( best=1; best<preds.length; best++)
      if( res == preds[best] && --idx < 0 )
        return best-1;          // Return best
    throw new RuntimeException("Should Not Reach Here");
  }

}