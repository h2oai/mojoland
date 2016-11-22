package ai.h2o.mojos.server.core;

import hex.genmodel.MojoModel;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.*;

/**
 * This class "knows" about the public API of a particular
 * {@code {Algo}MojoModel{N}} class. In particular we use reflection to
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
    private MethodParam[] args;
    private MethodParam ret;
    String apiName;

    //---- Public ------------------------------------------------------------------------------------------------------

    /** Number of arguments required for this method */
    public int numArgs() {
      return method.getParameterTypes().length;
    }

    /** Human-readable signature of the method */
    public String signature() {
      int n = numArgs();
      Class<?>[] parameterTypes = method.getParameterTypes();
      StringBuilder sb = new StringBuilder();
      sb.append(apiName);
      sb.append('(');
      for (int i = 0; i < n; i++) {
        if (i > 0) sb.append(", ");
        sb.append(parameterTypes[i].getSimpleName());
      }
      sb.append(") -> ");
      sb.append(method.getReturnType().getSimpleName());
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
      Class<?>[] parameterTypes = method.getParameterTypes();
      args = new MethodParam[parameterTypes.length];
      for (int i = 0; i < args.length; i++) {
        args[i] = MethodParam.paramForType(parameterTypes[i]);
        if (args[i] == null)
          throw new RuntimeException("No definition for parameter type " + parameterTypes[i].getName());
      }
      ret = MethodParam.paramForType(method.getReturnType());
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

  public int numMethods() {
    return methods.size();
  }


  //--------------------------------------------------------------------------------------------------------------------
  // Private
  //--------------------------------------------------------------------------------------------------------------------

  private void buildApi() {
    Method[] methodsArr = clz.getMethods();
    HashMap<String, Integer> methodNameCounts = new HashMap<>();
    for (Method method : methodsArr) {
      if (method.getDeclaringClass() == Object.class) continue;
      if (method.getName().startsWith("_")) continue;
      int mods = method.getModifiers();
      if (Modifier.isPublic(mods) && !Modifier.isStatic(mods)) {
        String name = method.getName();
        methodNameCounts.put(name, (methodNameCounts.containsKey(name)? methodNameCounts.get(name) : 0) + 1);
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
