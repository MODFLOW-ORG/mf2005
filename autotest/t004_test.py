import os
from pathlib import Path
from shutil import copytree, rmtree
import pytest
import flopy
from flopy.utils.compare import compare, compare_swrbudget, compare_stages
from modflow_devtools.misc import get_namefile_paths
import config


def run_mf2005(namefile, comparison=None):
    """
    Run the simulation.

    """

    # Enable comparison testing if release executable exists
    if comparison is None:
        comparison = Path(config.target_dict["release"]).exists()

    # Set root as the directory name where namefile is located
    # Get test name from namefile path (parent dir name + namefile stem)
    namefile_path = Path(namefile)
    testname = f"{namefile_path.parent.name}_{namefile_path.stem}"

    # if "VCatch" not in testname:
    #     return

    # set htol
    htol = config.get_htol(testname)

    # set percent discrepancy
    pdtol = config.get_pdtol(testname)

    # Set nam as namefile name without path
    nam = os.path.basename(namefile)

    # Setup - copy model files to test directory
    testpth = Path(config.testdir) / testname
    model_ws = Path(namefile).parent
    if testpth.exists():
        rmtree(testpth)
    copytree(model_ws, testpth)

    # run test models
    print("running model...{}".format(testname))
    exe_name = config.target_dict[config.program]
    success, buff = flopy.run_model(
        exe_name,
        nam,
        model_ws=str(testpth),
        silent=False,
    )

    # If it is a comparison, then look for files in the comparison
    # folder (.cmp)
    if success and comparison:
        testname_reg = Path(config.target_release).name
        testpth_reg = testpth / testname_reg
        model_ws = Path(namefile).parent
        if testpth_reg.exists():
            rmtree(testpth_reg)
        copytree(model_ws, testpth_reg)
        print("running regression model...{}".format(testname_reg))
        exe_name = config.target_dict["release"]
        success, buff = flopy.run_model(
            exe_name,
            nam,
            model_ws=str(testpth_reg),
            silent=False,
        )

        if success:
            namefile1 = str(testpth / nam)
            namefile2 = str(testpth_reg / nam)
            outfile1 = str(testpth / "bud.cmp")
            outfile2 = str(testpth / "hds.cmp")
            success_cmp = compare(
                namefile1,
                namefile2,
                precision="single",
                max_cumpd=pdtol,
                max_incpd=pdtol,
                htol=htol,
                outfile1=outfile1,
                outfile2=outfile2,
            )
            if not success_cmp:
                print("{} comparison failed".format(testname))

            outfile3 = str(testpth / "swr.bud.cmp")
            success_swr = compare_swrbudget(
                namefile1,
                namefile2,
                max_cumpd=pdtol,
                max_incpd=pdtol,
                outfile=outfile3,
            )
            if not success_swr:
                print("{} swr budget comparison failed".format(testname))

            # stage comparison
            outfile4 = str(testpth / "swr.stage.cmp")
            success_stg = compare_stages(
                namefile1=namefile1,
                namefile2=namefile2,
                htol=htol,
                outfile=outfile4,
            )
            if not success_stg:
                print("{} swr stage comparison failed".format(testname))

            if success_cmp and success_swr and success_stg:
                success = True
            else:
                success = False

    # Clean things up
    config.teardown(success, testpth)

    return


def pytest_generate_tests(metafunc):
    """Dynamically parametrize tests based on available namefiles."""
    if "namefile" in metafunc.fixturenames:
        test_path = Path(config.testpaths[3])
        excluded = list(config.exclude) if config.exclude else []
        if not test_path.exists():
            metafunc.parametrize("namefile", [], ids=[])
        else:
            namefiles = get_namefile_paths(
                config.testpaths[3],
                namefile="*.nam",
                excluded=excluded
            )
            metafunc.parametrize(
                "namefile",
                namefiles,
                ids=[p.name for p in namefiles]
            )


def test_mf2005(namefile):
    run_mf2005(namefile)


if __name__ == "__main__":
    excluded = list(config.exclude) if config.exclude else []
    namefiles = get_namefile_paths(
        config.testpaths[3],
        namefile="*.nam",
        excluded=excluded
    )
    for namefile in namefiles:
        run_mf2005(namefile)
