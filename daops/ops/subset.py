from daops.processor import process
from daops.utils import consolidate, normalise

from clisops.ops.subset import subset as clisops_subset
from roocs_utils.parameter import parameterise


def subset(
    collection,
    project=None,
    time=None,
    area=None,
    level=None,
    output_dir=None,
    chunk_rules=None,
    filenamer=None,
):
    """
    Example:
        collection: ("cmip6.ukesm1.r1.gn.tasmax.v20200101",)
        time: ("1999-01-01T00:00:00", "2100-12-30T00:00:00")
        area: (-5.,49.,10.,65)
        level: (1000.,)
        output_type: "netcdf"
        output_dir: "/cache/wps/procs/req0111"
        chunk_rules: "time:decade"
        filenamer: "facet_namer"


    :param collection: Collection parameter, sequence or string of comma separated drs ids
    :param project:
    :param time: Time period - Time parameter, sequence of two time values or string of two / separated time values
    :param area: Area parameter, sequence or string of comma separated lat and lon bounds. Must contain 4 values.
    :param level: Level range - Level parameter, sequence of two level values or string of two / separated level values
    :param output_dir:
    :param chunk_rules:
    :param filenamer:
    :return:
    """

    # collection, area, time, level = parameterise.parameterise_daops(
    #     collection=collection, time=time, area=area, level=level
    # )

    parameters = parameterise.parameterise(
        collection=collection, time=time, area=area, level=level
    )

    # Consolidate data inputs so they can be passed to Xarray

    collection = consolidate.consolidate(
        parameters.get('collection'), project=project, time=parameters.get('time')
    )

    # Normalise (i.e. "fix") data inputs based on "character"
    norm_collection = normalise.normalise(collection)

    rs = normalise.ResultSet(vars())
    # change name of data ref here
    for col, norm_collection in norm_collection.items():

        # Process each input dataset (either in series or
        # parallel)
        rs.add(
            col,
            process(
                clisops_subset,
                norm_collection,
                **{
                    "time": parameters.get('time'),
                    "area": parameters.get('area'),
                    "level": parameters.get('level'),
                    "output_type": "netcdf",
                    "output_dir": output_dir,
                    "chunk_rules": chunk_rules,
                    "filenamer": filenamer,
                }
            ),
        )

    return rs
