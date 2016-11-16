package ai.h2o.mojos.server.core;

import ai.h2o.mojos.runtime.shared.ModelCategory;
import hex.genmodel.MojoModel;
import hex.genmodel.algos.tree.SharedTreeGraph;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.*;

/**
 * This class "knows" about the public API of a particular
 * <code>{Algo}MojoModel{N}</code> class. In particular we use reflection to
 * scan the class, and then represent the api as a collection of
 * {@link ApiMethod} instances.
 */
public class MojoApi {
  private Class<? extends MojoModel> clz;
  private Map<String, ApiMethod> methods;
  private Set<String> originalMethodNames;


  //--------------------------------------------------------------------------------------------------------------------
  // ApiMethod class
  //--------------------------------------------------------------------------------------------------------------------

  public static class ApiMethod {
    private Method method;
    private Param[] args;
    private Param ret;
    String apiName;

    //---- Public ------------------------------------------------------------------------------------------------------

    /** Number of arguments required for this method */
    public int numArgs() {
      return method.getParameterCount();
    }

    /** Human-readable signature of the method */
    public String signature() {
      int n = numArgs();
      Class<?>[] parameterTypes = method.getParameterTypes();
      StringBuilder sb = new StringBuilder();
      sb.append(method.getReturnType().getSimpleName());
      sb.append(' ');
      sb.append(apiName);
      sb.append('(');
      for (int i = 0; i < n; i++) {
        if (i > 0) sb.append(", ");
        sb.append(parameterTypes[i].getSimpleName());
      }
      sb.append(");");
      return sb.toString();
    }

    /**
     * Call the method, passing the provided arguments list (this method will
     * parse the arguments from strings), and then return the result which was
     * serialized back into a string.
     */
    public String invoke(Object target, String[] strArgs) throws Exception {
      Object retVal = method.invoke(target, parseArgs(strArgs));
      return ret.toString(retVal);
    }


    //---- Private -----------------------------------------------------------------------------------------------------

    ApiMethod(Method m) {
      method = m;
      apiName = m.getName();
      args = new Param[m.getParameterCount()];
      Class<?>[] parameterTypes = method.getParameterTypes();
      for (int i = 0; i < args.length; i++) {
        args[i] = paramForType(parameterTypes[i]);
        if (args[i] == null)
          throw new RuntimeException("No definition for parameter type " + parameterTypes[i].getName());
      }
      ret = paramForType(method.getReturnType());
    }

    String uniqueName() {
      StringBuilder res = new StringBuilder(method.getName()).append("~");
      for (Class<?> ptype : method.getParameterTypes()) {
        String typeName = ptype.getSimpleName();
        res.append(typeName.substring(0, 1).toLowerCase());
        if (typeName.endsWith("[]")) res.append("a");
      }
      return res.toString();
    }

    private Object[] parseArgs(String[] strargs) {
      int n = strargs.length;
      assert n == numArgs();
      Object[] res = new Object[n];
      for (int i = 0; i < n; i++)
        res[i] = args[i].fromString(strargs[i]);
      return res;
    }

    private enum Param {
      STR {
        @Override public Object fromString(String s) { return s; }
        @Override public String toString(Object obj) { return '"' + ((String) obj) + '"'; }
      },
      VOID { @Override public String toString(Object o) { return "void"; } },
      INT { @Override public Object fromString(String s) { return Integer.parseInt(s); } },
      LONG { @Override public Object fromString(String s) { return Long.parseLong(s); } },
      FLOAT { @Override public Object fromString(String s) { return Float.parseFloat(s); } },
      DOUBLE { @Override public Object fromString(String s) { return Double.parseDouble(s); } },
      ADOUBLE {
        @Override public Object fromString(String s) {
          assert s.charAt(0) == '[' && s.charAt(s.length() - 1) == ']';
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
      BOOL { @Override public Object fromString(String s) { return Boolean.parseBoolean(s); } },
      STG {  // this is temporary...
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
      UNKNOWN;
      public Object fromString(String s) {
        return null;
      }
      public String toString(Object src) {
        return src.toString();
      }
    }

    private Param paramForType(Class<?> type) {
      String typeName = type.getName();
      switch (typeName) {
        case "void": return Param.VOID;
        case "int": return Param.INT;
        case "long": return Param.LONG;
        case "double": return Param.DOUBLE;
        case "float": return Param.FLOAT;
        case "boolean": return Param.BOOL;
        case "[D": return Param.ADOUBLE;
        case "java.lang.String": return Param.STR;
        case "hex.ModelCategory": return Param.MODELCATEGORY;
        case "hex.genmodel.algos.tree.SharedTreeGraph": return Param.STG;
        case "[F":
        case "java.util.Map":
        case "java.util.EnumSet":
        case "java.lang.Class":
        case "java.lang.Object":
        case "[Ljava.lang.String;":
        case "[[Ljava.lang.String;":
          return Param.UNKNOWN;
      }
      throw new RuntimeException("Unknown parameter type: " + typeName);
    }
  }


  //--------------------------------------------------------------------------------------------------------------------
  // Public interface of MojoApi
  //--------------------------------------------------------------------------------------------------------------------

  MojoApi(Class<? extends MojoModel> clazz) {
    clz = clazz;
    methods = new LinkedHashMap<>(5);
    originalMethodNames = new HashSet<>(5);
    buildApi();
  }

  /** Name of the class whose API is reflected by this object. */
  public String name() {
    return clz.getSimpleName();
  }

  /** Return true if the API contains method with the given name. */
  public boolean hasMethodWithName(String name) {
    return originalMethodNames.contains(name);
  }

  /** Return true if the API contains methods with the given uniquified name. */
  public boolean hasMethodWithUniqueName(String uname) {
    return methods.containsKey(uname);
  }

  /** Return {@link ApiMethod} corresponding to the given uniquified name. */
  public ApiMethod getMethodByUniqueName(String uname) {
    return methods.get(uname);
  }

  public Iterable<ApiMethod> listMethods() {
    return methods.values();
  }


  //--------------------------------------------------------------------------------------------------------------------
  // Private
  //--------------------------------------------------------------------------------------------------------------------

  private void buildApi() {
    Method[] methodsArr = clz.getMethods();
    HashMap<String, Integer> methodNameCounts = new HashMap<>();
    for (Method method : methodsArr) {
      if (method.getDeclaringClass() == java.lang.Object.class) continue;
      int mods = method.getModifiers();
      if (Modifier.isPublic(mods) && !Modifier.isStatic(mods)) {
        String name = method.getName();
        methodNameCounts.put(name, methodNameCounts.getOrDefault(name, 0) + 1);
        originalMethodNames.add(name);
      }
    }
    for (Method method : methodsArr) {
      String name = method.getName();
      if (!originalMethodNames.contains(name)) continue;
      ApiMethod apiMethod = new ApiMethod(method);
      if (methodNameCounts.get(name) == 1) {
        assert !methods.containsKey(name);
        methods.put(name, apiMethod);
        apiMethod.apiName = name;
      } else {
        String uniqName = apiMethod.uniqueName();
        if (methods.containsKey(uniqName))
          throw new RuntimeException(
              "Method " + method + " cannot be distinguished from '" + methods.get(uniqName).signature() + "'");
        methods.put(uniqName, apiMethod);
        apiMethod.apiName = uniqName;
      }
    }
  }
}
