from .Files import Main_File, Module
import click
import pathlib as pl
from os import getcwd
from .utils import find_files, write_makefile
__version__='0.0.1'

PATH = pl.Path(getcwd())
    


@click.group()
@click.option('--verbose', '-v', 'verbose', is_flag=True)
@click.option('--language', '-l', 'language', type=click.Choice(['c', "cpp"], case_sensitive=False), default='cpp')
@click.pass_context
def cli(ctx, verbose, language):
    
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['SUFFIXES']= {}
    if language == 'c':
        sources_suffix = 'c'
        header_suffix = 'h'
    elif language == 'cpp':
        sources_suffix = 'cpp'
        header_suffix = 'hpp'
    ctx.obj['SUFFIXES'] = {
        "sources_suffix": sources_suffix,
        "header_suffix": header_suffix
    }

@cli.command()
@click.argument('main_name', required=True,)
@click.argument('headers_names', required=False,nargs=-1)
@click.pass_context
def create(ctx, main_name, headers_names):
    with click.progressbar(length=100) as bar:
        # setting suffixes
        sources_suffix = ctx.obj['SUFFIXES']['sources_suffix']
        headers_suffix = ctx.obj['SUFFIXES']['header_suffix']

        # finding files
        sources_paths = find_files(PATH, sources_suffix)
        headers_paths = find_files(PATH, headers_suffix)
        bar.update(20)

        # is main here ? 
        if main_name in [path.stem for path in sources_paths]:
            raise click.BadParameter(f"The file {main_name}.{sources_suffix} already exists and you want to create one more, that's not possible buddy")

        # is there already a header ? 
        for header_name in headers_names:
            filename = header_name.split('::')[0]
            if filename in [path.stem for path in headers_paths]:
                raise click.BadParameter(f"The file {filename}.{headers_suffix} already exists and you want to create one more, that's not possible buddy")

        main = Main_File(main_name, main_suffix=sources_suffix, header_suffix=headers_suffix, )
        bar.update(50)
        modules = []
        for header_name in headers_names:
            module = Module(header_name, module_suffix=headers_suffix, main_suffix=sources_suffix)
            modules.append(module)
            main.add_header_include(module.get_header_include())
            module.deploy(PATH)
        main.deploy_at_init(PATH)
        bar.update(100)
    

@cli.command()
@click.argument('main_name', required=True, nargs=1)
@click.argument('headers_names', required=True,nargs=-1)
@click.pass_context
def add(ctx, main_name, headers_names):
    with click.progressbar(length=100) as bar:
        # setting suffixes
        sources_suffix = ctx.obj['SUFFIXES']['sources_suffix']
        headers_suffix = ctx.obj['SUFFIXES']['header_suffix']

        # finding files
        sources_paths = find_files(PATH, sources_suffix)
        headers_paths = find_files(PATH, headers_suffix)

        # is main here ? (should be...)
        if not main_name in [path.stem for path in sources_paths]:
            raise click.BadParameter(f"The file {main_name}.{sources_suffix} don't exists, it should to use the 'add' mode.")

        for header_name in headers_names:
            filename = header_name.split('::')[0]
            if filename in [path.stem for path in headers_paths]:
                raise click.BadParameter(f"The file {filename}.{headers_suffix} already exists and you want to create one more, that's not possible buddy")
        
        main = Main_File(main_name, main_suffix=sources_suffix, header_suffix=headers_suffix, )
        bar.update(50)
        modules = []
        for header_name in headers_names:
            module = Module(header_name, module_suffix=headers_suffix, main_suffix=sources_suffix)
            modules.append(module)
            main.add_header_include(module.get_header_include())
            module.deploy(PATH)
        main.deploy_at_runtime(PATH)
        bar.update(100)

@cli.command()
@click.pass_context
def makefile(ctx):
    with click.progressbar(length=100) as bar:
        if not 'GNUmakefile' in [PATH.glob("GNUmakefile")]:
            write_makefile(PATH)
        bar.update(100)



    
    



if __name__ == '__main__':
    cli(obj={})