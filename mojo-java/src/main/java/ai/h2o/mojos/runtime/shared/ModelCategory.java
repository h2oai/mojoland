package ai.h2o.mojos.runtime.shared;

/**
 * Different prediction categories for models.
 *
 * Constants in this enum should never be removed or renamed.
 */
@SuppressWarnings("unused")
public enum ModelCategory {
  Unknown,
  Binomial,
  Multinomial,
  Regression,
  Clustering,
  AutoEncoder,
  DimReduction
}
