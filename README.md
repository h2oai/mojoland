Mojo-land
=========

This is the testing ground to ensure mojos backward compatibility. The goal of this project is to collect
pre-trained mojo models (for different mojo versions and various datasets) and their expected scoring results. Then
we will routinely test that for each new version of the genmodel runtime all saved mojo models still produce the same
results as originally. This will enable us to have full backward compatibility of mojos: old models are guaranteed
to be invariant with respect to the updates of the runtime.


Contract
--------

When speaking about backward compatibility, it is essential to understand which things are and which are not expected
to be stable over time.

  * Data -> H2O Model (training) : not stable over time. Given same data and same input parameters (including the
    seed), it is entirely possible that future versions of H2O may build a slightly different model. Hopefully, a
    better one.

  * H2O Model -> Mojo : not stable over time. For the same model we may produce a different mojo in a future
    version of H2O.

  * H2O Model -> versioned Mojo : stable. This means that given the same model on the server, the mojos produced
    ought to be identical provided their version number is the same.

    Unfortunately, we don't have a good way of testing this right now, since there is no reliable way of transferring
    a model across H2O versions. On the other hand, this stability requirement doesn't seem to be that important.

  * Mojo -> MojoModel -> results : stable. This is the contract that is being tested here, so it deserves a thorough
    explanation. A mojo is a binary file, which cannot be run by itself. It requires the genmodel.jar runtime in order
    to run (in the future we will be adding runtimes for other languages as well). This runtime instantiates a
    MojoModel object from the mojo file. Public API of this object is the contract being tested.

    The stability property guarantees that given the same input data, the MojoModel will produce identical results
    even when instantiated in genmodel runtimes of different versions. More specifically, the mojo is guaranteed to
    produce identical results with any genmodel which is current or newer than was at the time of mojo's creation.
    At the same time instantiating a mojo against an older version of the runtime should produce an error.

    As for the notion of "public API", it is somewhat vague. We will assume that only those methods that are being
    tested in the test suite are considered "the public API". Any method that was once declared public, will continue
    to be so (unless it is removed). The public API should be rich enough to allow day-to-day work with mojos. Methods
    that are part of the public API should be clearly annotated as such.

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

  * Test harness -> IPC : not stable. In order to be able to test the mojos, we need a way to communicate with the
    java process from the python process. This will be achieved via the IPC protocol (or some other eventually). The
    exact details of this communication protocol are subject to change.


Mojo versioning
---------------

Each mojo file carries a mojo version internally. This version is a decimal number, for example 1.0 or 2.03. Mojos for
different algorithms can have separate versions. The minor version should be a 2-digit number, to ensure proper sorting
in both numeric and lexicographic cases. The major version must coincide with the version of the `MojoModel` being
created.

Thus, mojo's major version is bumped whenever the `MojoModel`s interface needs to be changed, and the minor version is
increased when any internal mojo change occurs.

To summarize:
  * Change in `<Algo>MojoModel<N>`s API (i.e. addition or removal of methods, change in methods' parameters or return
    types) -- bump mojo's version to (N+1).0 and create new `<Algo>MojoModel<N+1>`.
  * Change in `<Algo>MojoModel<N>`s private/protected API -- no need to change mojo's version.
  * Change in what is being stored inside a mojo -- increase its minor version.
  * Change to the underlying algorithm that affects scoring or other public functions -- increase mojo's minor version.


Structure
---------

    datasets         : collection of sample datasets for training / testing.
    src              : scripts to create and later to test the mojos.
      algos
        ...
        gbm          : algo-specific recipes for creating each particular test example.
    mojos            : stored mojo files and their outputs.
      ...
      drf            : algo-specific folders,
        ...
        v2.00        : further grouped by mojo versions,
          iris       : finally grouped by the dataset.
          aerolines  : Each folder contains the mojo and the output files.
          prostate


