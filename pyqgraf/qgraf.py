import shutil
import os
import warnings
import re

from smpl_io import io
import shlex
import subprocess

from pyqgraf.wrap import dewrap_all, wrap_model

qgraf_path = shutil.which("qgraf")


def install(version="3.6.5", reinstall=False):
    """Install qgraf locally if not already installed."""
    global qgraf_path
    qgraf_path = os.path.expanduser(f"~/.local/bin/qgraf-{version}")
    if not reinstall and os.path.exists(qgraf_path):
        return

    import tempfile
    from skbuild import cmaker

    with tempfile.TemporaryDirectory() as tmpdirname:

        import tarfile
        import requests

        sub_ver = ".".join(version.split(".")[0:2])

        r = requests.get(
            f"http://anonymous:anonymous@qgraf.tecnico.ulisboa.pt/v{sub_ver}/qgraf-{version}.tgz",
            allow_redirects=True,
        )
        open(tmpdirname + "qgraf.tgz", "wb").write(r.content)
        tarfile.open(tmpdirname + "qgraf.tgz").extractall(tmpdirname)

        filenames = io.glob_re(r"qgraf.*\.(f|f08)", tmpdirname)
        if len(filenames) != 1:
            raise RuntimeError(
                "Could not identify qgraf source files: " + str(filenames)
            )
        filename = filenames[0]
        # shutil.copy(tmpdirname + "/" + filename, tmpdirname + "/qgraf.f")

        open(tmpdirname + "/CMakeLists.txt", "w").write(
            (
                f"""
cmake_minimum_required(VERSION 3.1)
enable_language(Fortran)
project(qgraf)
set_source_files_properties({filename} PROPERTIES LANGUAGE Fortran)
add_executable(qgraf {filename})
install(TARGETS qgraf)
"""
            )
        )
        with io.pushd(tmpdirname):
            maker = cmaker.CMaker()

            maker.configure(
                ["-DCMAKE_INSTALL_PREFIX=" + tmpdirname],
            )

            maker.make()
        qgraf_path = os.path.expanduser(f"~/.local/bin/qgraf-{version}")

        os.makedirs(os.path.expanduser("~/.local/bin"), exist_ok=True)
        shutil.copy(tmpdirname + "/bin/qgraf", qgraf_path)


if qgraf_path is None:
    install()


warnings.warn(
    """
	Please cite the following papers if you use this code:

      [1] Automatic Feynman graph generation J. Comput. Phys. 105 (1993) 279--289 https://doi.org/10.1006/jcph.1993.1074

      [2] Abusing Qgraf Nucl. Instrum. Methods Phys. Res. A 559 (2006) 220--223 https://doi.org/10.1016/j.nima.2005.11.151

      [3] Feynman graph generation and propagator mixing, I Comput. Phys. Commun. 269 (2021) 108103 https://doi.org/10.1016/j.cpc.2021.108103

	"""
)


def call(dat="qgraf.dat"):
    """Call qgraf with the given dat file."""
    global qgraf_path
    print(f"{qgraf_path} {dat}")
    subprocess.call(shlex.split(f"{qgraf_path} {dat}"))


def run(
    in_,
    out,
    loops,
    loop_momentum,
    options="notadpole,onshell",
    style=None,
    model=None,
    output=None,
    fstyle="tmp.sty",
    fmodel="tmp.model",
    fdat="qgraf.dat",
    foutput="output.out",
    prefix_path=None,
    wrap=True,
    **kwargs,
):
    """
    Run qgraf with the given parameters.

    Args:
        in_ (str): list of incoming particles
        out (str): list of outgoing particles
        loops (int): number of loops
        loop_momementum (str): loop momentum
        model (str): model file
        style (str): style file
        output (str): output file, unused
        options (str): options
        fstyle (str): style file
        fmodel (str): model file
        fdat (str): dat file
        foutput (str): output file


    """
    if prefix_path is not None:
        fstyle = prefix_path + style
        fmodel = prefix_path + model
        fdat = prefix_path + fdat
        foutput = prefix_path + foutput
    if model is not None:
        if wrap:
            model,wrapd = wrap_model(model)
            for k,v in wrapd.items():
                in_.replace(k,v)
                out.replace(k,v)
        io.write(fmodel, model, create_dir=False)
    if style is not None:
        io.write(fstyle, style, create_dir=False)
    args = ""
    for k, v in kwargs.items():
        args = args + f" {k} = {v};\n"
    io.write(
        fdat,
        f"""
 output= '{foutput}' ;
 style= '{fstyle}' ;
 model = '{fmodel}';
 in= {in_};
 out= {out};
 loops= {loops};
 loop_momentum= {loop_momentum};
 options= {options};
     """
        + args,
        create_dir=False,
    )
    # remove output file if it exists
    io.remove(foutput)
    call(fdat)
    ret = io.read(foutput)
    if wrap and model is not None:
        ret = dewrap_all(ret)
    return ret
