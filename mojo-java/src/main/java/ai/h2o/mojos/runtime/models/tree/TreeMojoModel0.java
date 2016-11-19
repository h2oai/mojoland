package ai.h2o.mojos.runtime.models.tree;

import ai.h2o.mojos.runtime.models.MojoModel0;
import ai.h2o.mojos.runtime.models.gbm.GbmMojoModel0;
import ai.h2o.mojos.runtime.utils.BitSetWrapper;
import ai.h2o.mojos.runtime.utils.ByteBufferWrapper;

import java.util.Arrays;

/**
 * Common ancestor for {link DrfMojoModel} and {@link GbmMojoModel0}.
 * See also: `hex.tree.SharedTreeModel` and `hex.tree.TreeVisitor` classes.
 */
public abstract strictfp class TreeMojoModel0 extends MojoModel0 {
  // private static final int NsdNone = 0;
  private static final int NsdNaVsRest = 1;
  private static final int NsdNaLeft = 2;
  // private static final int NsdNaRight = 3;
  private static final int NsdLeft = 4;
  // private static final int NsdRight = 5;

  protected int ntrees;
  protected int ntreesPerClass;
  protected byte[][] compressedTrees;


  /**
   * Highly efficient (critical path) tree scoring
   *
   * Given a tree (in the form of a byte array) and the row of input data, compute either this tree's
   * predicted value when `computeLeafAssignment` is false, or the the decision path within the tree (but no more
   * than 64 levels) when `computeLeafAssignment` is true.
   *
   * Note: this function is also used from the `hex.tree.CompressedTree` class in `h2o-algos` project.
   */
  private double scoreTree(byte[] tree, double[] row) {
    ByteBufferWrapper ab = new ByteBufferWrapper(tree, endianness);
    BitSetWrapper bs = null;  // Lazily set on hitting first group test
    while (true) {
      int nodeType = ab.get1U();
      int colId = ab.get2();
      if (colId == 65535) return ab.get4f();
      int naSplitDir = ab.get1U();
      boolean naVsRest = naSplitDir == NsdNaVsRest;
      boolean leftward = naSplitDir == NsdNaLeft || naSplitDir == NsdLeft;
      int lmask = (nodeType & 51);
      int equal = (nodeType & 12);  // Can be one of 0, 8, 12
      assert equal != 4;  // no longer supported

      float splitVal = -1;
      if (!naVsRest) {
        // Extract value or group to split on
        if (equal == 0) {
          // Standard float-compare test (either < or ==)
          splitVal = ab.get4f();  // Get the float to compare
        } else {
          // Bitset test
          if (bs == null) bs = new BitSetWrapper(0);
          if (equal == 8)
            bs.fill2(tree, ab);
          else
            bs.fill3(tree, ab);
        }
      }

      double d = row[colId];
      if (Double.isNaN(d)? !leftward : !naVsRest && (equal == 0? d >= splitVal : bs.contains((int)d))) {
        // go RIGHT
        switch (lmask) {
          case 0:  ab.skip(ab.get1U());  break;
          case 1:  ab.skip(ab.get2());  break;
          case 2:  ab.skip(ab.get3());  break;
          case 3:  ab.skip(ab.get4());  break;
          case 16: ab.skip(nclasses < 256? 1 : 2);  break;  // Small leaf
          case 48: ab.skip(4);  break;  // skip the prediction
          default:
            assert false : "illegal lmask value " + lmask + " in tree " + Arrays.toString(tree);
        }
        lmask = (nodeType & 0xC0) >> 2;  // Replace leftmask with the rightmask
      } else {
        // go LEFT
        if (lmask <= 3)
          ab.skip(lmask + 1);
      }

      if ((lmask & 16) != 0) {
        return ab.get4f();
      }
    }
  }


  //------------------------------------------------------------------------------------------------------------------
  // Private
  //------------------------------------------------------------------------------------------------------------------

  protected TreeMojoModel0(String[] columns, String[][] domains) {
    super(columns, domains);
  }

  /**
   * Score all trees and fill in the `preds` array.
   */
  protected void scoreAllTrees(double[] row, double[] preds, int nClassesToScore) {
    java.util.Arrays.fill(preds, 0);
    for (int i = 0; i < nClassesToScore; i++) {
      int k = nclasses == 1? 0 : i + 1;
      for (int j = 0; j < ntrees; j++) {
        int itree = i * ntrees + j;
        preds[k] += scoreTree(compressedTrees[itree], row);
      }
    }
  }

  // Build a class distribution from a log scale.
  // Because we call Math.exp, we have to be numerically stable or else we get
  // Infinities, and then shortly NaN's.  Rescale the data so the largest value
  // is +/-1 and the other values are smaller.  See notes here:
  // http://www.hongliangjie.com/2011/01/07/logsum/
  private static double log_rescale(double[] preds) {
    // Find a max
    double maxval=Double.NEGATIVE_INFINITY;
    for( int k=1; k<preds.length; k++) maxval = Math.max(maxval,preds[k]);
    assert !Double.isInfinite(maxval) : "Something is wrong with GBM trees since returned prediction is " + Arrays.toString(preds);
    // exponentiate the scaled predictions; keep a rolling sum
    double dsum=0;
    for( int k=1; k<preds.length; k++ )
      dsum += (preds[k]=Math.exp(preds[k]-maxval));
    return dsum;                // Return rolling sum; predictions are log-scaled
  }

  // Build a class distribution from a log scale; find the top prediction
  protected static void GBM_rescale(double[] preds) {
    double sum = log_rescale(preds);
    for (int k = 1; k < preds.length; k++)
      preds[k] /= sum;
  }

}
