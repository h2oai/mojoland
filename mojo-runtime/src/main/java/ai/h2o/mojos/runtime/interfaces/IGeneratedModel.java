package ai.h2o.mojos.runtime.interfaces;


/**
 * Copy of {@code IGeneratedModel} from {@code genmodel-all.jar}.
 */
public interface IGeneratedModel {
  /** Returns model's unique identifier. */
  public String getUUID();

  /** Returns number of columns used as input for training (i.e., exclude response and offset columns). */
  public int getNumCols();

  /** The names of columns used in the model. It contains names of input columns and a name of response column. */
  public String[] getNames();

  /** The name of the response column. */
  @Deprecated
  public String getResponseName();

  /** Returns an index of the response column inside getDomains(). */
  public int getResponseIdx();

  /** Get number of classes in in given column.
   * Return number greater than zero if the column is categorical
   * or -1 if the column is numeric. */
  public int getNumClasses(int i);

  /** Return a number of classes in response column.
   *
   * @return number of response classes
   * @throws java.lang.UnsupportedOperationException if called on a non-classifier model.
   */
  public int getNumResponseClasses();

  /** @return true if this model represents a classifier, else it is used for regression. */
  public boolean isClassifier();

  /** @return true if this model represents an AutoEncoder. */
  public boolean isAutoEncoder();

  /** Gets domain of given column.
   * @param name column name
   * @return return domain for given column or null if column is numeric.
   */
  public String[] getDomainValues(String name);

  /**
   * Returns domain values for i-th column.
   * @param i index of column
   * @return domain for given categorical column or null if columns contains numeric value
   */
  public String[] getDomainValues(int i);

  /** Returns domain values for all columns including response column. */
  public String[][] getDomainValues();

  /** Returns index of column with give name or -1 if column is not found. */
  public int getColIdx(String name);

  /** Maps given column's categorical to integer used by this model.
   * Returns -1 if mapping is not found. */
  public int mapEnum(int colIdx, String categoricalValue);

  /**
   * Returns the expected size of preds array which is passed to `predict(double[], float[])` function.
   * @return expected size of preds array
   */
  public int getPredsSize();

}