package ai.h2o.mojos.server.core;

import java.util.Arrays;

/**
 * This class is used to represent arguments / return types of some class
 * {@link java.lang.reflect.Method}s. The job of this class is to provide
 * utilities for serialization / deserialization of the parameters of each
 * possible type, so that they can be passed to/from the API layer.
 */
enum MethodParam {
  /**
   * String parameter. No escaping / unescaping is needed since it is already
   * done at the HTTP request level. This means that the output provides no
   * indication that it returns a string, for example if the string being
   * returned is {@code "1"} then it will be returned as simply {@code 1},
   * which is indistinguishable from an integer. Similarly, if a string
   * contains newlines or other special characters, they will be returned to
   * the client as-is. This shouldn't cause any problems since the return
   * value is always used standalone and is never embedded into any other
   * context.
   */
  STR {
    @Override public Object fromString(String s) {
      return s;
    }
    @Override public String toString(Object obj) {
      return (String)obj;
    }
  },

  /**
   * {@code void} type -- may only be used as a return value.
   */
  VOID {
    @Override public String toString(Object o) {
      return "";
    }
  },

  /**
   * Boolean (primitive type).
   * We do not use {@link Boolean#valueOf(String)} because it is too lenient:
   * any string that is not {@code "true"} is converted to {@code false}.
   */
  BOOL {
    @Override public Object fromString(String s) {
      if (s.equalsIgnoreCase("true")) return true;
      if (s.equalsIgnoreCase("false")) return false;
      throw new NumberFormatException("Value " + s + " cannot be converted to boolean.");
    }
  },

  /**
   * Integer (primitive type)
   */
  INT {
    @Override public Object fromString(String s) {
      return Integer.valueOf(s);
    }
    @Override public String toString(Object o) {
      return Integer.toString((int)o);
    }
  },

  /**
   * Long integer (primitive type)
   */
  LONG {
    @Override public Object fromString(String s) {
      return Long.valueOf(s);
    }
    @Override public String toString(Object o) {
      return Long.toString((long)o);
    }
  },

  /**
   * Float (primitive type)
   */
  FLOAT {
    @Override public strictfp Object fromString(String s) {
      return Float.valueOf(s);
    }
    @Override public strictfp String toString(Object o) {
      return Float.toString((float)o);
    }
  },

  /**
   * Double (primitive type)
   */
  DOUBLE {
    @Override public strictfp Object fromString(String s) {
      return Double.valueOf(s);
    }
    @Override public strictfp String toString(Object o) {
      return Double.toString((double)o);
    }
  },

  /**
   * Array of floats ({@code float[]}).
   * <p>
   * If a string {@code "null"} is passed, then a {@code null} object will be
   * returned; otherwise a primitive array of {@code float}s is constructed.
   * Individual elements of this array cannot be {@code null}s.
   */
  AFLOAT {
    @Override public strictfp Object fromString(String s) {
      if (s.equals("null")) return null;
      if (s.length() < 2 || s.charAt(0) != '[' || s.charAt(s.length() - 1) != ']')
        throw new NumberFormatException("Invalid float[] array: " + s);
      String[] parts = s.substring(1, s.length() - 1).split(",\\s*");
      float[] res = new float[parts.length];
      for (int i = 0; i < res.length; i++)
        res[i] = Float.parseFloat(parts[i]);
      return res;
    }
    @Override public String toString(Object src) {
      return Arrays.toString((float[]) src);
    }
  },

  /**
   * Array of doubles ({@code double[]})
   * <p>
   * If a string {@code "null"} is passed, then a {@code null} object will be
   * returned; otherwise a primitive array of {@code double}s is constructed.
   * Individual elements of this array cannot be {@code null}s.
   */
  ADOUBLE {
    @Override public strictfp Object fromString(String s) {
      if (s.equals("null")) return null;
      if (s.length() < 2 || s.charAt(0) != '[' || s.charAt(s.length() - 1) != ']')
        throw new NumberFormatException("Invalid double[] array: " + s);
      String[] parts = s.substring(1, s.length() - 1).split(",\\s*");
      double[] res = new double[parts.length];
      for (int i = 0; i < res.length; i++)
        res[i] = Double.parseDouble(parts[i]);
      return res;
    }
    @Override public String toString(Object src) {
      return Arrays.toString((double[]) src);
    }
  },

  ASTR {
    @Override public Object fromString(String s) {
      throw new UnsupportedOperationException("Parsing of String[] not implemented.");
    }
    @Override public String toString(Object o) {
      if (o == null) return "null";
      StringBuilder sb = new StringBuilder();
      sb.append("[");
      boolean start = true;
      for (String elem : (String[])o) {
        if (start)
          start = false;
        else
          sb.append(", ");
        if (elem.contains("\\") || elem.contains("\"") || elem.contains("\n"))
          elem = elem.replace("\n", "\\n").replace("\"", "\\\"").replace("\\", "\\\\");
        sb.append('"').append(elem).append('"');
      }
      sb.append("]");
      return sb.toString();
    }
  },

  AASTR {
    @Override public Object fromString(String s) {
      throw new UnsupportedOperationException("Parsing of String[][] not implemented.");
    }
    @Override public String toString(Object o) {
      if (o == null) return "null";
      StringBuilder sb = new StringBuilder();
      sb.append("[");
      boolean start = true;
      for (String[] elem : (String[][])o) {
        if (start)
          start = false;
        else
          sb.append(", ");
        sb.append(MethodParam.ASTR.toString(elem));
      }
      sb.append("]");
      return sb.toString();
    }
  },
  /*
  STG {
    @Override public String toString(Object src) {
      ByteArrayOutputStream baos = new ByteArrayOutputStream();
      PrintStream ps = new PrintStream(baos);
      ((SharedTreeGraph)src).printDot(ps, 3, false);
      return new String(baos.toByteArray());
    }
  },
  MODELCATEGORY {
    @Override public Object fromString(String s) { return ModelCategory.valueOf(s); }
  },
  */
  UNKNOWN;


  //--------------------------------------------------------------------------------------------------------------------
  // Public interface
  //--------------------------------------------------------------------------------------------------------------------

  /**
   * Method to instantiate objects of the underlying type from their string
   * representation. For non-primitive types this method should also allow
   * to create {@code null} objects if the passed string is {@code "null"}.
   */
  public Object fromString(String s) {
    return null;
  }


  /**
   * Method to convert objects of the underlying types to strings. This will
   * only be used for the "return" argument. I.e. when a method returns some
   * value, that value has to be converted to a string before being passed to
   * the user as an HTTP response. This method is the one performing such a
   * conversion.
   *
   * @param src An object of the type represented by the MethodParam.
   */
  public String toString(Object src) {
    return src.toString();
  }


  /**
   * Factory method for mapping raw java types into {@link MethodParam}
   * entities.
   *
   * @param type any parameter, represented as its class.
   */
  public static MethodParam paramForType(Class<?> type) {
    String typeName = type.getName();
    switch (typeName) {
      case "void": return VOID;
      case "int": return INT;
      case "long": return LONG;
      case "double": return DOUBLE;
      case "float": return FLOAT;
      case "boolean": return BOOL;
      case "[F": return AFLOAT;
      case "[D": return ADOUBLE;
      case "java.lang.String": return STR;
      case "[Ljava.lang.String;": return ASTR;
      case "[[Ljava.lang.String;": return AASTR;
      // case "ai.h2o.mojos.runtime.shared.ModelCategory": return MODELCATEGORY;
      case "[B":
      case "hex.ModelCategory":
      case "hex.genmodel.algos.tree.SharedTreeGraph":
      case "java.util.Map":
      case "java.util.EnumSet":
      case "java.lang.Object":
      case "biz.k11i.xgboost.util.FVec":
      case "hex.genmodel.algos.tree.SharedTreeMojoModel$LeafNodeAssignments":
      case "hex.genmodel.PredictContributions":
      case "hex.genmodel.PredictContributionsFactory":
      case "hex.genmodel.CategoricalEncoding":
      case "hex.genmodel.algos.tree.ConvertTreeOptions":
      case "hex.genmodel.algos.tree.TreeSHAPPredictor$Workspace":
        return UNKNOWN;
    }
    throw new RuntimeException("Unknown parameter type: " + typeName);
  }
}
