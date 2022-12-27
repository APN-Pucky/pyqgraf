import shutil
import os
import warnings
import re

qgraf_path = shutil.which("qgraf")


def glob_re(pattern, strings):
    return list(filter(re.compile(pattern).match, strings))


def install(version="3.4.2"):
    global qgraf_path
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

        filenames = glob_re(r"qgraf.*\.(f|f08)", os.listdir(tmpdirname))
        if len(filenames) != 1:
            raise RuntimeError(
                "Could not identify qgraf source files: " + str(filenames)
            )
        filename = filenames[0]

        open(tmpdirname + "CMakeLists.txt", "w").write(
            (
                f"""
cmake_minimum_required(VERSION 3.1)
enable_language(Fortran)
project(qgraf)
add_executable(qgraf {filename})
install(TARGETS qgraf)
"""
            )
        )

        maker = cmaker.CMaker()

        maker.configure(["-DCMAKE_INSTALL_PREFIX=" + tmpdirname])

        maker.make()
        qgraf_path = f"~/.local/bin/qgraf-{version}"

        os.makedirs(os.path.expanduser("~/.local/bin"), exist_ok=True)
        shutil.copy(tmpdirname + "/bin/qgraf", os.path.expanduser(qgraf_path))


if qgraf_path is None:
    qgraf_path = "~/.local/bin/qgraf"
    if not os.path.exists(qgraf_path):
        install()


warnings.warn(
    """
	Please cite the following papers if you use this code:

      [1] Automatic Feynman graph generation J. Comput. Phys. 105 (1993) 279--289 https://doi.org/10.1006/jcph.1993.1074

      [2] Abusing Qgraf Nucl. Instrum. Methods Phys. Res. A 559 (2006) 220--223 https://doi.org/10.1016/j.nima.2005.11.151

      [3] Feynman graph generation and propagator mixing, I Comput. Phys. Commun. 269 (2021) 108103 https://doi.org/10.1016/j.cpc.2021.108103

	"""
)

from smpl import io
import shlex
import subprocess


def call(dat="qgraf.dat"):
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
    fdat="tmp.dat",
    foutput="output.out",
    prefix_path=None,
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
    return io.read(foutput)
