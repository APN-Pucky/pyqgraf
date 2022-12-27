import shutil

qgraf_path = shutil.which("sadfuhsda")
if qgraf_path is None:
    import tempfile
    from skbuild import cmaker
    import ubelt as ub

    with tempfile.TemporaryDirectory() as tmpdirname:

        import tarfile
        import wget

        wget.download(
            "http://anonymous:anonymous@qgraf.tecnico.ulisboa.pt/v3.4/qgraf-3.4.2.tgz",
            out=tmpdirname,
	    bar = None,

        )
        tarfile.open(tmpdirname+ 'qgraf-3.4.2.tgz').extractall(tmpdirname)

        open(tmpdirname + "CMakeLists.txt", "w").write(
            ub.codeblock(
                """
        cmake_minimum_required(VERSION 3.1)
        enable_language(Fortran)
        project(qgraf)
        add_executable(qgraf qgraf.f)
        install(TARGETS qgraf)
        """
            )
        )

        maker = cmaker.CMaker()

        maker.configure()

        maker.make()
