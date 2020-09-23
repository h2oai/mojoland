Mojo-land
=========

This is the testing ground to ensure mojos backward compatibility. The goal of this project is to collect
pre-trained mojo models (for different mojo versions and various datasets) and their expected scoring results. Then
we will routinely test that for each new version of the genmodel runtime all saved mojo models still produce the same
results as originally. This will enable us to have full backward compatibility of mojos: old models are guaranteed
to be invariant with respect to the updates of the runtime.


Contract
--------

When speaking about backward compatibility, it is essential to understand which things are, and which are not expected
to be stable over time.

  * Data -> H2O Model (training) : not stable over time. Given same data and same input parameters (including the
    seed), it is entirely possible that future versions of H2O may build a slightly different model. Hopefully, a
    better one.

  * H2O Model -> Mojo : not stable over time. For the same model we may produce a different mojo in a future
    version of H2O. This will always be accompanied by mojo version increase.

  * Mojo -> MojoModel -> results : stable. This is the contract that is being tested here, so it deserves a thorough
    explanation. A mojo is a binary file, which cannot be run by itself. It requires the mojo-runtime.jar for it to run
    (in the future we will be adding runtimes for other languages as well). This runtime instantiates a MojoModel object
    from the mojo file. Public API of this object is what is being tested.

    The stability property guarantees that given the same input data, the MojoModel will produce identical results
    even when instantiated in runtimes of future versions. More specifically, the mojo is guaranteed to produce
    identical results with any runtime which is current or newer than was at the time of mojo's creation. At the same
    time instantiating a mojo against an older version of the runtime should produce an error.

  * MojoModels' public API : not stable. This means that mojos of different versions are allowed to have different
    APIs. Such changes should be infrequent. However if API changes do occur, they do not apply retroactively:
    new API functions should not be made available for old mojos.

    In practice we will maintain the following hierarchy: all mojos are instances of the base `MojoModel` class. This
    class only has factory methods for instantiating mojos (`public static MojoModel load(? source)`). The `MojoModel`
    class is subclassed by `MojoModel1` (or `MojoModel2`, etc) which is further subclassed by `GbmMojoModel1`,
    `DrfMojoModel2`, etc. The public interface of each `<Algo>MojoModel<N>` never changes. However different versions
    of mojos may produce instances of `<Algo>MojoModel<N>` with different `N`s.

    It is expected that concrete versions of the algo-specific interfaces may differ from the versions of `MojoModel`.
    For example, we may have `DrfMojoModel3` extending `MojoModel1`.



Mojo versioning
---------------

Each mojo file carries an internal version, which is a decimal number for example 1.00 or 2.03. Mojos for different
algorithms can have different versions. The minor version (after the decimal dot) should be a 2-digit number, to ensure 
proper sorting both numerically and lexicographically. The major version must coincide with the version of the 
`MojoModel` being created.

Thus, mojo's major version is bumped whenever the `MojoModel`s interface needs to be changed, and the minor version is
increased when any internal mojo change occurs.

To summarize:

  * Change in `<Algo>MojoModel<N>`s API (i.e. addition or removal of methods, change in methods' parameters or return
    types) -- bump mojo's version to (N+1).00 and create new `<Algo>MojoModel<N+1>`. Note that **any API change**, 
     including adding new functions, warrants creating new API class.
  * Change in `<Algo>MojoModel<N>`s private/protected API -- no need to change mojo's version.
  * Change in what is being stored inside a mojo -- increase its minor version.
  * Change to the underlying algorithm that affects scoring or other public functions -- increase mojo's minor version.


Runtime hierarchy
-----------------

At the top level of the runtime's hierarchy is the `MojoModel` class, which has only minimal amount of functionality 
(few static functions). This class is extended by `MojoModel1`, `MojoModel2`, etc -- each class providing bare-bones
functionality for their descendants. Each `MojoModel{N}` class should have only protected or private methods. These 
classes can then be extended by `{Algo}BaseModel{N}` classes carrying algo-specific functionality shared by the apis
of different versions. Again, these classes must not expose any public methods. Finally, at the last level of the
hierarchy live classes `{Algo}MojoModel{N}`. These are the concrete classes that get instantiated when a mojo is loaded,
and they define the API of each mojo: a mojo's API is the set of declared public methods of the corresponding 
`{Algo}MojoModel{N}` class.

Separate from this, there is a collection of (versioned) interfaces, each covering some part of the functionality of
each `{Algo}MojoModel{N}`. These interfaces are expected to be more stable over time than the concrete classes, and
they can extend each other (for example an interface of version `n` may extend an interface of version `n - 1`). The
interfaces don't have any predefined naming pattern.

If a mojo model class uses an externally visible class or enum, it should be properly versioned too. For example,
consider the "GlrmLoss" enum. "Proper versioning" requires that the enum was called `GlrmLoss1`, anticipating that
there will be future versions `GlrmLoss2`, `GlrmLoss3`, etc. Each specific algo then specifies which version of the
enum it expects.


Project building
----------------

To build the project, please use the provided `gradlew` command:

    ./gradlew build
