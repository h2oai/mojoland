package ai.h2o.mojos.runtime.interfaces;

import ai.h2o.mojos.runtime.shared.ModelCategory;


/**
 * Copy of {@code IGenModel} from {@code genmodel-all.jar}.
 */
public interface IGenModel {

  /**
   * Returns true for supervised models.
   * @return true if this class represents supervised model.
   */
  boolean isSupervised();

  /**
   * Returns number of input features.
   * @return number of input features used for training.
   */
  int nfeatures();

  /**
   * Returns number of output classes for classifiers or 1 for regression models. For unsupervised models returns 0.
   */
  int nclasses();


  /** Returns this model category.
   *
   * @return model category
   */
  ModelCategory getModelCategory();

}
