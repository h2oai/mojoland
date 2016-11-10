package ai.h2o.mojos.server.core;

import ai.h2o.mojos.server.core.MojoApi;
import hex.genmodel.MojoModel;

import java.util.HashMap;


/**
 * This class is used as a singleton, and it keeps knowledge about all the
 * models that were loaded in the system.
 */
public class MojoStore {
  private static Integer _idCounter = 0;
  private static HashMap<String, MojoModel> _mojoStore = new HashMap<>();
  private static HashMap<Class<? extends MojoModel>, MojoApi> _mojoApi = new HashMap<>();

  public static String addModel(MojoModel model) {
    _idCounter++;
    String id = _idCounter.toString();
    _mojoStore.put(id, model);
    Class<? extends MojoModel> clz = model.getClass();
    if (!_mojoApi.containsKey(clz))
      _mojoApi.put(clz, new MojoApi(clz));
    return id;
  }

  public static MojoModel getModel(String id) {
    return _mojoStore.get(id);
  }

  public static void delModel(String id) {
    _mojoStore.remove(id);
  }

  public static MojoApi getModelApi(MojoModel m) {
    return m == null? null : _mojoApi.get(m.getClass());
  }

}
